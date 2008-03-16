# -*- coding: utf-8 -*-
import os
import sys
import time
import socket
import datetime
import feedparser

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.template.defaultfilters import striptags, yesno
from django.core.mail import mail_admins

from django_de.apps.aggregator.models import Feed, Item

socket.setdefaulttimeout(5) #FIXME PLEASE

class Command(NoArgsCommand):
    help = 'Used to update the feeds of the aggregator app.'

    def handle_noargs(self, **options):
        feeds = Feed.objects.public()
        sys.stdout.write('%s Feeds werden überprüft\n' % len(feeds))

        for feed in feeds:
            sys.stdout.write('\nDoing %s (Keyword-Check: %s):\n' % (feed.feed_url,
                                                                    yesno(feed.keyword_check, "Ja,Nein")))
            # Prüfe ob die maximale Error-Anzahl erreicht ist,
            # dann deaktviere den Feed
            if feed.errors >= getattr(settings, "AGGREGATOR_MAX_ERRORS", 0):
                sys.stderr.write("Disabled! Zu viele Fehler, Feed wurde gesperrt. (%s)\n" % feed.title.encode('utf-8'))
                feed.public = False
                feed.save()

                # Nachricht an den Admin
                message = 'Wegen zu vieler Fehler wurde der Feed deaktiviert: %s' % feed.feed_url
                mail_admins('Community: Feed wurde deaktiviert', message, True)

                continue

            # Feed parsen
            parsed_feed = feedparser.parse(feed.feed_url)

            # Prüfe, ob die Feed-URL einen echten Feed zurück gibt, sonst
            # erhöhe den Error-Zähler um 1
            if not parsed_feed.version:
                sys.stderr.write("Broken! (%s)\n" % feed.title.encode('utf-8'))
                feed.errors += 1
                feed.save()
                continue
            # Erfolgreicher echter schöner Feed -> Fehler auf 0 setzen
            else:
                feed.errors = 0
                feed.save()

            new_item_counter = 0

            for entry in parsed_feed.entries:

                guid = entry.get("id", entry.link).encode(parsed_feed.encoding,
                    "xmlcharrefreplace")
                link = entry.link.encode(parsed_feed.encoding,
                    "xmlcharrefreplace")

                if not guid:
                    guid = link

                # ############################################################
                # Titel parsen und strippen
                # ############################################################
                title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
                title = striptags(title)
                title = " ".join(title.split())


                # ############################################################
                # Content ausfindig machen, ein Hoch auf Standards
                # ############################################################
                if hasattr(entry, "summary"):
                    content = entry.summary
                elif hasattr(entry, "content"):
                    content = entry.content[0].value
                elif hasattr(entry, "description"):
                    content = entry.description
                else:
                    content = u""

                content = content.encode(parsed_feed.encoding, "xmlcharrefreplace")

                # Tags und Whitespace-Zeichen aus dem Content enfernen
                content = striptags(content)
                content = " ".join(content.split())

                # ############################################################
                # Keyword Check
                # ############################################################
                keyword_check_passed = False
                if feed.keyword_check:
                    for keyword in feed.keywords.split():
                        if keyword in content.lower() or keyword in title.lower():
                            keyword_check_passed = True
                            sys.stdout.write('  + Beitrag gefunden: %s\n' % title.encode('utf-8'))
                            break
                        else:
                            sys.stdout.write('  - Beitrag ohne Keyword: %s\n' % title.encode('utf-8'))
                            continue
                else:
                    keyword_check_passed = True
                    sys.stdout.write('  o Beitrag gefunden: %s\n' % title.encode('utf-8'))

                # Kein Keyword gefunden: Weg damit
                if not keyword_check_passed:
                    continue

                # ############################################################
                # Datumskram
                # ############################################################
                try:
                    if entry.has_key('modified_parsed'):
                        published_original = datetime.datetime.fromtimestamp(
                            time.mktime(entry.modified_parsed))
                    elif parsed_feed.feed.has_key('modified_parsed'):
                        published_original = datetime.datetime.fromtimestamp(
                            time.mktime(parsed_feed.feed.modified_parsed))
                    elif parsed_feed.has_key('modified'):
                        published_original = datetime.datetime.fromtimestamp(
                            time.mktime(parsed_feed.modified))
                    else:
                        published_original = datetime.datetime.now()
                except TypeError:
                    published_original = datetime.datetime.now()

                # ############################################################
                # Feed speichern, wenn er nicht schon existiert
                # ############################################################
                try:
                    feed.item_set.get(guid=guid)
                except Item.DoesNotExist:
                    new_item_counter += 1
                    # TODO: hier noch die unmöglichsten Fehler abfangen
                    feed.item_set.create(title=title, url=link, summary=content,
                        guid=guid, published_original=published_original)

            sys.stdout.write("OK! (%s neue Beiträge hinzugefügt)\n" % new_item_counter)

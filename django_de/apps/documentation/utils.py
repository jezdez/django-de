"""
From djangoproject.com generator:
django_website/apps/docs/parts/build_documentation.py
"""
from django.conf import settings
from docutils import nodes, utils
from docutils.core import publish_parts
from docutils.writers import html4css1

SETTINGS = {
    'initial_header_level': 2,
    'input_encoding': 'unicode'
}

def restify(content):
    parts = publish_parts(
        content,
        writer=DjangoHTMLWriter(),
        settings_overrides=SETTINGS,
    )
    return parts['toc'], parts['html_body']

class DjangoHTMLWriter(html4css1.Writer):
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = DjangoHTMLTranslator

    def translate(self):
        # build the document
        html4css1.Writer.translate(self)

        # build the contents
        contents = self.build_contents(self.document)
        contents_doc = self.document.copy()
        contents_doc.children = contents
        contents_visitor = self.translator_class(contents_doc)
        contents_doc.walkabout(contents_visitor)
        self.parts['toc'] = "<ul class='toc'>%s</ul>" % ''.join(contents_visitor.fragment)

    def build_contents(self, node, level=0):
        level += 1
        sections = []
        i = len(node) - 1
        while i >= 0 and isinstance(node[i], nodes.section):
            sections.append(node[i])
            i -= 1
        sections.reverse()
        entries = []
        autonum = 0
        depth = 4   # XXX FIXME
        for section in sections:
            title = section[0]
            entrytext = title
            try:
                reference = nodes.reference('', '', refid=section['ids'][0], *entrytext)
            except IndexError:
                continue
            ref_id = self.document.set_id(reference)
            entry = nodes.paragraph('', '', reference)
            item = nodes.list_item('', entry)
            if level < depth:
                subsects = self.build_contents(section, level)
                item += subsects
            entries.append(item)
        if entries:
            contents = nodes.bullet_list('', *entries)
            return contents
        else:
            return []

class DjangoHTMLTranslator(html4css1.HTMLTranslator):
    def visit_table(self, node):
        """Remove the damn border=1 from the standard HTML writer"""
        self.body.append(self.starttag(node, 'table', CLASS='docutils'))

    def visit_title(self, node):
        """Coppied from html4css1.Writer wholesale just to get rid of the <a name=> crap.  Fun, eh?"""
        check_id = 0
        close_tag = '</p>\n'
        if isinstance(node.parent, nodes.topic):
            self.body.append(
                  self.starttag(node, 'p', '', CLASS='topic-title first'))
            check_id = 1
        elif isinstance(node.parent, nodes.sidebar):
            self.body.append(
                  self.starttag(node, 'p', '', CLASS='sidebar-title'))
            check_id = 1
        elif isinstance(node.parent, nodes.Admonition):
            self.body.append(
                  self.starttag(node, 'p', '', CLASS='admonition-title'))
            check_id = 1
        elif isinstance(node.parent, nodes.table):
            self.body.append(
                  self.starttag(node, 'caption', ''))
            check_id = 1
            close_tag = '</caption>\n'
        elif isinstance(node.parent, nodes.document):
            self.body.append(self.starttag(node, 'h1', '', CLASS='title'))
            self.context.append('</h1>\n') # remove acces to all doc versions
            self.in_document_title = len(self.body)
        else:
            assert isinstance(node.parent, nodes.section)
            h_level = self.section_level + self.initial_header_level - 1
            atts = {}
            if (len(node.parent) >= 2 and
                isinstance(node.parent[1], nodes.subtitle)):
                atts['CLASS'] = 'with-subtitle'
            node.ids = node.parent['ids']
            self.body.append(self.starttag(node, 'h%s' % h_level, '', **atts))
            self.context.append('</h%s>\n' % (h_level))
        if check_id:
            if node.parent['ids']:
                self.body.append(
                    self.starttag({}, 'a', '', name=node.parent['ids'][0]))
                self.context.append('</a>' + close_tag)
            else:
                self.context.append(close_tag)

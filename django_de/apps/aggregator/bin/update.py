#!/usr/bin/env python

"""Updates newsfeeds of the aggregator app."""

from django.core import management

if __name__ == "__main__":
    management.call_command('updatefeeds')

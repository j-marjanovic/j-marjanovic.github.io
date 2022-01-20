#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jan Marjanovic'
SITENAME = u'j-marjanovic.io'
SITEURL = 'j-marjanovic.io'

PATH = 'content'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = u'en'
LOCALE = ('en_US.UTF-8')

PLUGIN_PATHS = ['../pelican-plugins', "../pelican-embed-tweet"]
PLUGINS = ["render_math", "pelican.plugins.embed_tweet"]

# Feed generation is usually not desired when developing
#FEED_ALL_ATOM = None
FEED_ALL_ATOM = 'feeds/all.atom.xml'
#CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
"""LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)"""

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/janmarjanovic'),
          ('LinkedIn', 'https://www.linkedin.com/in/janmarjanovic/'),
	       )

TWITTER_USERNAME = 'janmarjanovic'

DEFAULT_PAGINATION = 10


# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

#THEME = 'Subtle'
THEME = 'theme-jan'

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

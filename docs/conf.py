# -*- coding: utf-8 -*-
# http://www.sphinx-doc.org/en/master/config

import os, sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Abalone BoAI'
copyright = '2018 Scriptim (MIT)'
author = 'Scriptim'

version = '2.1.0'
release = '2.1.0'

extensions = ['sphinx.ext.autodoc', 'm2r']

source_suffix = '.rst'
master_doc = 'index'

language = 'en'
today_fmt = '%d.%m.%Y'

html_theme = 'haiku'
man_pages = [(master_doc, 'abaloneboai', 'Abalone BoAI Documentation',
[author], 1)]

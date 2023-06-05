# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../src/spellchecker/'))
sys.path.insert(1, os.path.abspath('../src/app/'))
sys.path.insert(2, os.path.abspath('../src/search_index/'))
sys.path.insert(3, os.path.abspath('../src/parser/'))
sys.path.insert(4, os.path.abspath('../.'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Slack ds search system'
copyright = '2023, Denis Rogozhin, Aleksej Zubaryov, Dmitriy Motrichenko, Alexander Vorontsov'
author = 'Denis Rogozhin, Aleksej Zubaryov, Dmitriy Motrichenko, Alexander Vorontsov'
release = '0.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

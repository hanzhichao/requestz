import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
from requestz import __copyright__, __author__, __version__
# pip install sphinx-rtd-theme
import sphinx_rtd_theme

project = 'requestz'
copyright = __copyright__
author = __author__
release = __version__

print(project)
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

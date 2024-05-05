#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Configuration file for the Sphinx documentation builder."""

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "co2calculator"
copyright = (
    "2024, Christina Ludwig, Veit Ulrich, Hannah Weiser, Sarah Lohr, Fabian Kneissl"
)
author = "Christina Ludwig, Veit Ulrich, Hannah Weiser, Sarah Lohr, Fabian Kneissl"

# The full version, including alpha/beta/rc tags
release = "0.1.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.viewcode",
    "myst_parser",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

html_theme_options = {
    "body_max_width": "none",
    "page_width": "80%",
    "sidebar_width": "350px",
    "fixed_sidebar": "true",
    "github_button": "true",
    "github_user": "pledge4future",
    "github_repo": "co2calculator",
    "show_powered_by": "true",
    "sidebar_header": "#FFA500",
    "narrow_sidebar_bg": "#FFA500",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = [
    "css-style.css",
]
html_logo = "Final logo.svg"

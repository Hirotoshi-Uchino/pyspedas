# -*- coding: utf-8 -*-
"""
File:
    version.py

Desrciption:
    Pyspedas version number.

Returns:
    The version number for the current installation.
"""
import pyspedas

def version():
    import os.path
    dir_path = os.path.abspath(os.path.dirname(__file__))
    # fname = os.path.join(dir_path, 'spd_prefs_txt.py')
    print("Preferences file: " + pyspedas.Config().get_filepath())

    import pkg_resources
    ver = pkg_resources.get_distribution("pyspedas").version
    print("pyspedas version: " + ver)

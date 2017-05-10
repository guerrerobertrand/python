#! /usr/bin/env python
# -*- coding:Utf8 -*-

# Démo. du sélecteur de couleurs de Tkinter

try:
    from tkinter import colorchooser           # module Tkinter pour Python 3
except:
    import tkColorChooser as colorchooser      # module Tkinter pour Python 2

couleur = colorchooser.askcolor()

print("couleur choisie", couleur)

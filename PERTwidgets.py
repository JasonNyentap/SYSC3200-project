"""
An improvement on the tkinter Checkbar example,
available from http://www.python-course.eu/tkinter_checkboxes.php

Author: Matt Woodhead (GitHub community member)


"""

import tkinter as tk
from tkinter import ttk
from tkinter import *

'''
https://gist.github.com/MattWoodhead/82796750990e4b7741afeeb2c0dff491
'''
class Checkbar(ttk.Frame):
    """
    Creates the checkbar class, which defines a set of checkboxes using a list.
    Can both return and set the states of individual checkboxes
    """
    def __init__(self, parent=None, picks=[], side=tk.LEFT, anchor=tk.W):
        ttk.Frame.__init__(self, parent)
        self.vars = {}
        self.barbuttons = []
        
        for pick in picks:
            var = tk.IntVar()
            chk = ttk.Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=1)
            
            #DEFAULTS to checked ON
            chk.invoke()
            self.barbuttons.append(chk)

            self.vars[pick] = var  # Add the pick to the dictionary


    def getvar(self):
        """ returns the checkbox values """
        return [var.get() for picks, var in self.vars.items()]

    def setvar(self, pick, value):
        """ sets the value for a specific checkbox in the checkbar """
        if pick in self.vars.keys():
            self.vars[pick].set(value)
        else:
            print("incorrect checkbox name")


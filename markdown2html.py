#!/usr/bin/python3

"""
Script converts markdown to HTML.
"""

from html_builder import HTML

if __name__ == '__main__':

    html = HTML()
    html.process().build().substitute().write()
    exit(0)

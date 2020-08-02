#!/usr/bin/python3

"""
Markdown HTML builder class.
"""

from os import path
from search_replace import SearchandReplace
import sys
from typing import List


class HTML:
    def __init__(self):
        """
        HTML constructor.
        """
        self.data = ""
        self.task_queue = []
        self.readme = None
        self.html = None
        self.open()

    def open(self):
        """
        Reads command line arguments and opens file in argv[1].
        Will exit if there are less than 3 arguments or
        readme filename does not exist.
        """
        if len(sys.argv) < 3:
            sys.stderr.write(
                "Usage: ./markdown2html.py README.md README.html\n")
            exit(1)
        self.readme = sys.argv[1]
        self.html = sys.argv[2]
        if not path.exists(self.readme):
            sys.stderr.write(f"Missing {self.readme}\n")
            exit(1)
        with open(self.readme) as f:
            lines = f.readlines()
            self.lines = lines
        return self

    def process(self):
        """
        Processes readme file and groups adjacent markdowns.
        """
        queue = []
        while len(self.lines):
            line = self.lines.pop(0).rstrip()
            md = self.get_markdown(line)
            args = self.get_args(md, line)
            if md in {"ol", "ul", "p"}:
                args = self.add_siblings(self.lines, args, md)
            elif md == "x":
                continue
            queue.append([md, args])
        self.task_queue = queue
        return self

    def get_markdown(self, line: str) -> str:
        """
        Matches string with corresponding markdown tag.
        """
        markdown = ""
        markdown_map = {
            "#": "h1",
            "##": "h2",
            "###": "h3",
            "####": "h4",
            "#####": "h5",
            "######": "h6",
            "-": "ul",
            "*": "ol",
        }
        if not len(line):
            markdown = "x"
        else:
            markdown = markdown_map.get(line.split(" ")[0]) or "p"
        return markdown

    def get_args(self, md: str, line: str) -> str:
        """
        Parses arguments from markdown string.
        """
        args = ""
        if md in {"p", "x"}:
            args = line
        else:
            args = " ".join(line.split(" ")[1:])
        return args

    def add_siblings(self, queue: List[str],
                     args: List or str, md: str) -> List or str:
        """
        Combine sibling markdown arguments into one list.
        """
        while queue and self.get_markdown(queue[0].rstrip()) == md:
            _next = queue.pop(0).rstrip()
            _next = self.get_args(md, _next)
            if type(args) == list:
                args.append(_next)
            else:
                args = [args, _next]
        return args

    def build(self):
        """
        Builds HTML string out of task queue.
        """
        res = ""
        for (md, args) in self.task_queue:
            res += f"<{md}>"
            if md in {"ul", "ol"}:
                res += self.build_list(args)
            elif md == "p":
                res += self.build_paragraph(args)
            else:
                res += args
            res += f"</{md}>\n"
        self.data += res.rstrip()
        return self

    def build_list(self, args: List or str) -> str:
        """
        Builds HTML list tags.
        """
        res = ""
        if type(args) == list:
            while len(args):
                res += f"\n<li>{args.pop(0)}</li>"
        else:
            res += f"\n<li>{args}</li>"
        res += "\n"
        return res

    def build_paragraph(self, args: List or str) -> str:
        """
        Builds HTML paragraph tags.
        """
        res = ""
        if type(args) == list:
            while len(args):
                res += f"\n{args.pop(0)}"
                if len(args):
                    res += "\n<br/>"
        else:
            res += f"\n{args}"
        res += "\n"
        return res

    def substitute(self):
        """
        Parses HTML string and replaces special symbols.
        """
        sr = SearchandReplace()
        self.data = sr.sub_bold(sr.sub_emphasis(
            sr.sub_c(sr.sub_md5(self.data))))
        return self

    def write(self):
        """
        Writes HTML string to HTML file.
        """
        with open(self.html, "w") as f:
            f.write(self.data)

#!/usr/bin/python3

import hashlib
import re

"""
Search and Replace class.
"""


class SearchandReplace:

    def sub_c(self, s: str) -> str:
        """
        Removes all c's from double parens tags.
        """
        return re.sub(r"\(\([\w\s]+\)\)",
                      lambda x: self._remove_paren(
                          self._remove_c(x.group())), s)

    def sub_bold(self, s: str) -> str:
        """
        Replaces all double asterisk tags with <bold> tags.
        """
        return re.sub(r"\*\*([\<\>\/\*\w\s]+)\*\*",
                      r"<b>\1</b>", s)

    def sub_emphasis(self, s: str) -> str:
        """
        Replaces all dunder tags with <em> tags.
        """
        return re.sub(r"\_\_([\<\>\/\*\w\s]+)\_\_",
                      r"<em>\1</em>", s)

    def sub_md5(self, s: str) -> str:
        """
        Replaces all double bracket tags with md5 encryption.
        """
        return re.sub(r"\[\[([\/\w\s]+)\]\]",
                      lambda x: self._encrypt_md5(x.group()), s)

    def _remove_c(self, s: str) -> str:
        """
        Removes all c's from a string.
        """
        return "".join(c for c in s if c not in {"c", "C"})

    def _remove_paren(self, s: str) -> str:
        """
        Removes all parentheses from a string.
        """
        return "".join(c for c in s if c not in {"(", ")"})

    def _remove_bracket(self, s: str) -> str:
        """
        Removes all brackets from a string.
        """
        return "".join(c for c in s if c not in {"[", "]"})

    def _encrypt_md5(self, s: str) -> str:
        """
        Encrypts a string with md5.
        """
        return hashlib.md5(self._remove_bracket(s).encode()).hexdigest()

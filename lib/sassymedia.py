#!/usr/bin/python

"""
Sassy Media re-factors media queries within the CSS outputted by SASS to enhance
compression and readability.

Usage: python sassymedia.py style.css, ...
"""
import sys
import re
from collections import OrderedDict


RE_HAS_MEDIA = re.compile("@media")
RE_FIND_MEDIA = re.compile("(@media.+?)(\{)", re.DOTALL | re.MULTILINE)


class SassyMedia:
    """
    Sassy Media re-factors media queries within the CSS outputted by SASS to
    enhance compression and readability.
    """

    def __init__(self):
        self._reset()

    def run(self):
        # Make sure it has media queries
        if not RE_HAS_MEDIA.search(self.contents):
            return

        # Find all of the unique media queries
        # Issue #1: Media query orders can get mixed up
        self.queries = [(m.group(1).strip(), m) for m in RE_FIND_MEDIA.finditer(self.contents)]

        # Consolidate the media queries
        for (query, m) in self.queries:
            if not query in self.query_contents:
                self.query_contents[query] = []
            self.query_contents[query].append(self._get_contents(m))

        # Remove the media queries
        for contents in self.query_contents.itervalues():
            for (_, content) in contents:
                self.contents = self.contents.replace(content, "")

        # Add the consolidated media queries
        for (query, contents) in self.query_contents.iteritems():
            self.contents += query + " {\n"
            for (content, _) in contents:
                self.contents += content + "\n"
            self.contents += "}\n"

    def fix(self, filename):
        self._reset()
        self._get_file_contents(filename)
        self.run()
        self._put_file_contents(filename)

    def _get_file_contents(self, filename):
        fh = open(filename, "r")
        self.contents = fh.read()
        fh.close()

    def _put_file_contents(self, filename):
        fh = open(filename, "w")
        print >> fh, self.contents
        fh.close()

    def _reset(self):
        self.queries = []
        self.query_contents = OrderedDict()
        self.contents = ""

    def _get_contents(self, match):
        open_braces = 1  # we are starting the character after the first opening brace
        position = match.end()
        content = ""
        while open_braces > 0:
            c = self.contents[position]
            if c == "{":
                open_braces += 1
            if c == "}":
                open_braces -= 1
            content += c
            position += 1
        return (content[:-1].strip(), self.contents[match.start():position])  # the last closing brace gets captured, drop it


def help():
    print """
Sassy Media re-factors media queries within the CSS outputted by SASS to enhance
compression and readability.

Usage: %s style.css, ...
""" % sys.argv[0]


def main():
    if len(sys.argv) > 1:
        m = SassyMedia()
        for style in sys.argv[1::]:
            m.fix(style)
    else:
        help()


if __name__ == "__main__":
    main()

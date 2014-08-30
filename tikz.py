#! /usr/bin/env python

import hashlib
import re
import os
import sys
import shutil
from pandocfilters import toJSONFilter, Para, Image
from subprocess import Popen, PIPE, call
from tempfile import mkdtemp

imagedir = "assets/images"

def sha1(x):
    return hashlib.sha1(x).hexdigest()

def tikz2svg(tikz, filetype, outfile):
    tmpdir = mkdtemp()
    olddir = os.getcwd()
    os.chdir(tmpdir)
    f = open('tikz.tex', 'w')
    f.write("""\\documentclass{standalone}
               \\usepackage{tikz}
               \\begin{document}
            """)
    f.write(tikz)
    f.write("\n\\end{document}\n")
    f.close()
    p = call(["pdflatex", 'tikz.tex'])
    os.chdir(olddir)
    if filetype == 'pdf':
        shutil.copyfile(tmpdir + '/tikz.pdf', outfile + '.pdf')
    else:
        call(["pdf2svg", tmpdir + '/tikz.pdf', outfile + '.svg'])
    shutil.rmtree(tmpdir)

def tikz(key, value, format, meta):
    if key == 'RawBlock':
        [fmt, code] = value
        if fmt == "latex" and re.match("\\\\begin{tikzpicture}", code):
            outfile = imagedir + '/' + sha1(code)
            if format == "latex":
                filetype = "pdf"
            else:
                filetype = "svg"
            src = outfile + '.' + filetype
            if not os.path.isfile(src):
                try:
                    os.mkdir(imagedir)
                except OSError:
                    pass
                tikz2svg(code, filetype, outfile)
            return Para([Image([], ['/'+src, ""])])

if __name__ == "__main__":
  toJSONFilter(tikz)


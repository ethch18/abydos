#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from os import listdir
from os.path import isfile
import codecs, chardet
import re
import sys

lang_tuple = ('any', 'arabic', 'cyrillic', 'czech', 'dutch', 'english', 'french', 'german', 'greek', 'greeklatin', 'hebrew', 'hungarian', 'italian', 'polish', 'portuguese', 'romanian', 'russian', 'spanish', 'turkish')
lang_dict = dict()
for i,l in enumerate(lang_tuple):
    lang_dict[l] = 2**i
lang_dict['common'] = "'common'"

nl = False
array_seen = False

tail_text = ''

def c2u(name):
    """Src:
    http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return s1


def pythonize(line, fn='', subdir='gen'):
    global nl, array_seen

    if '$all' in line:
        return ''
    if 'make the sum of all languages be visible in the function' in line:
        return ''

    line = line.strip()

    if 'array' in line and not line.startswith('//'):
        array_seen = True

    line = re.sub('//+', '#', line)
    #line = re.sub('"\.\((\$.+?)\)\."', r'\1', line)
    if line and re.search('array\("[^"]+?"\)', line):
        #print "### " + line
        line = ''
    line = line.replace('array', '')
    line = re.sub('^\s*', '', line)
    line = re.sub(';$', '', line)
    line = re.sub('^include_.+', '', line)

    line = re.sub(
        '\$(approx|rules|exact)\[LanguageIndex\("([^"]+)", \$languages\)\] = \$([a-zA-Z]+)',
        lambda m: "BMDATA['" + subdir + "']['" + m.group(1) + "'][L_" + m.group(2).upper() + "] = _" + subdir.upper() + '_' + c2u(m.group(3)).upper(),
        line)

    line = re.sub(
        '\$(approx|rules|exact|hebrew)([A-Za-z]+) = _merge\(\$([a-zA-Z]+), \$([a-zA-Z]+)\)',
        lambda m: "BMDATA['" + subdir + "']['" + m.group(1) + "'][L_" + c2u(m.group(2)).upper() + "] = _" + subdir.upper() + '_' + c2u(m.group(3)).upper() + ' + _' + subdir.upper() + '_' + c2u(m.group(4)).upper(),
        line)

    line = re.sub(
        '\$(approx|rules|exact)\[LanguageIndex\("([^"]+)", \$languages\)\] = _merge\(\$([a-zA-Z]+), \$([a-zA-Z]+)\)',
        lambda m: "BMDATA['" + subdir + "']['" + m.group(1) + "'][L_" + c2u(m.group(2)).upper() + "] = _" + subdir.upper() + '_' + c2u(m.group(3)).upper() + ' + _' + subdir.upper() + '_' + c2u(m.group(4)).upper(),
        line)

    line = re.sub('^\$([a-zA-Z]+)',  lambda m: '_' + s.upper() + '_' + c2u(m.group(1)).upper(), line)

    for _ in range(len(lang_tuple)):
        line = re.sub('($[a-zA-Z]+) *\+ *($[a-zA-Z]+)', r'\1\+\2', line)

    line = re.sub('\$([a-zA-Z]+)', lambda m: 'L_'+m.group(1).upper() if m.group(1) in lang_dict else '$'+m.group(1), line)
    line = re.sub('\[\"\.\((L_[A-Z_\+]+)\)\.\"\]', r'[\1]', line)

    line = re.sub('L_([A-Z]+)', lambda m: str(lang_dict[m.group(1).lower()]), line)
    for i in range(4):
        line = re.sub('([0-9]+) *\+ *([0-9]+)', lambda m: str(int(m.group(1))+int(m.group(2))), line)

    if fn == 'lang':
        if len(line.split(',')) >= 3:
            parts = line.split(',')
            parts[0] = re.sub("/(.+?)/", r"\1", parts[0])
            #parts[1] = re.sub('\$', 'L_', parts[1])
            #parts[1] = re.sub(' *\+ *', '|', parts[1])
            parts[2] = parts[2].title()
            line = ','.join(parts)

    if fn == 'languagenames':
        line = line.replace('"', "'")
        line = line.replace("','", "', '")

    line = line.replace('ë', 'ü')

    code = ''
    comment = ''
    if '#' in line:
        hashsign = line.find('#')
        comment = line[hashsign:]
        code = line[:hashsign]
    else:
        code = line

    if '(' in code and ')' in code:
        prefix = code[:code.find('(')+1]
        suffix = code[code.rfind(')'):]
        tuplecontent = code[len(prefix):len(code)-len(suffix)]

        elts = tuplecontent.split(',')
        for i in range(len(elts)):
            elts[i] = elts[i].strip()
            if elts[i][0] == '"' and elts[i][-1] == '"':
                elts[i] = "'" + elts[i][1:-1].replace("'", "\\'") + "'"
        tuplecontent = ', '.join(elts)

        code = prefix+tuplecontent+suffix

    line = code + comment

    if line:
        nl = False
        if array_seen and not (line[0] == '_' or line.startswith('BMDATA')):
            line = ' '*5 + line
        return line + '\n'
    elif nl == False:
        nl = True
        return '\n'
    else:
        return ''

bmdir = sys.argv[1].rstrip('/') + '/'

outfilename = '../abydos/_bmdata.py'
outfile = codecs.open(outfilename, 'w', 'utf-8')
outfile.write('# -*- coding: utf-8 -*-\n\"\"\"abydos.bmdata\n\nCopyright 2014 by Christopher C. Little.\nThis file is part of Abydos.\n\nThis file is derived from PHP code by Alexander Beider and Stephen P. Morse that\nis part of the Beider-Morse Phonetic Matching (BMPM) System, available at\nhttp://stevemorse.org/phonetics/bmpm.htm.\n\nAbydos is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nAbydos is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with Abydos. If not, see <http://www.gnu.org/licenses/>.\n\"\"\"\n# pylint: disable=line-too-long\n\nfrom __future__ import unicode_literals\n\n')

outfile.write('L_NONE = 0\n')
for i,l in enumerate(lang_tuple):
    outfile.write('L_' + l.upper() + ' = 2**' + str(i) + '\n')
outfile.write('\n\n')

tail_text += '\nBMDATA = dict()\n'

subdirs = ('gen', 'sep', 'ash')

for s in subdirs:
    tail_text += '\nBMDATA[\''+s+'\'] = dict()\n'
    tail_text += 'BMDATA[\''+s+'\'][\'approx\'] = dict()\n'
    tail_text += 'BMDATA[\''+s+'\'][\'exact\'] = dict()\n'
    tail_text += 'BMDATA[\''+s+'\'][\'rules\'] = dict()\n'
    tail_text += 'BMDATA[\''+s+'\'][\'hebrew\'] = dict()\n\n'
    tail_text += 'BMDATA[\''+s+'\'][\'language_rules\'] = _'+s.upper()+'_LANGUAGE_RULES\n'
    tail_text += 'BMDATA[\''+s+'\'][\'languages\'] = _'+s.upper()+'_LANGUAGES\n'

    phps = [f for f in sorted(listdir(bmdir + s + '/')) if (isfile(bmdir + s + '/' + f) and f.endswith('.php'))]
    for infilename in phps:
        for pfx in ('rules', 'approx', 'exact', 'hebrew', 'language', 'lang'):
            if infilename.startswith(pfx):
                array_seen = False
                infilepath = bmdir + s + '/' + infilename
                infileenc = chardet.detect(open(infilepath).read())['encoding']
                print s+'/'+infilename
                infile = codecs.open(infilepath, 'r', infileenc)
                if infilename.startswith('lang'):
                    tuplename = infilename[:-4]
                else:
                    tuplename = pfx + '_' + infilename[len(pfx):-4]
                # indent = len(tuplename) + 21

                outfile.write('# ' + s + '/' + infilename + '\n')

                ignore = True
                for line in infile:
                    if 'function Language' in line:
                        break
                    if not ignore:
                        if re.search(r'\?>', line):
                            ignore = True
                        else:
                            line = pythonize(line, infilename[:-4], s)
                            if line.startswith('BMDATA'):
                                tail_text += line
                            else:
                                outfile.write(line)
                    if '*/' in line:
                        ignore = False

                outfile.write('\n\n')
                break

outfile.write(tail_text)

outfile.close()
outfilelines = codecs.open(outfilename, 'r', 'utf-8').readlines()
outfile = codecs.open(outfilename, 'w', 'utf-8')
nl = False
fixlanguagesarray = False
for line in outfilelines:
    line = line.rstrip()
    if line:
        if fixlanguagesarray:
            line = ' '+line.strip()
            fixlanguagesarray = False
        outfile.write(line)
        if not line.endswith('='):
            outfile.write('\n')
        else:
            fixlanguagesarray = True
        nl = False
    else:
        if not nl:
            outfile.write('\n')
        nl = True


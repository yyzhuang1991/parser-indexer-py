#!/usr/bin/env python
# json2brat.py
# Convert JSON output (from CoreNLP) to brat (.ann) format.
# Brat format: http://brat.nlplab.org/standoff.html 
#
# Kiri Wagstaff
# July 31, 2017

import sys, os, shutil, io
import json
from ioutils import read_jsonlines

def usage():
    print './json2brat.py <JSON file> <output dir>'
    print ' Note: all documents in the JSON file will be'
    print ' saved out to individual files in the output directory.'
    sys.exit(1)


def convert_json_to_brat(jsonfile, outdir):
    # Read in the JSON file
    docs = read_jsonlines(jsonfile)

    # Iterate over documents
    for d in docs:
        res_name = d['metadata']['resourceName']
        if type(res_name) == list:
            # Sometimes Tika returns this as something like
            # "resourceName": ["2005_1725.pdf", "High Quality.joboptions"]
            res_name = res_name[0]

        # Output text into a .txt file
        text = d['content_ann_s']
        outfn = os.path.join(outdir, res_name[:-4] + '.txt')
        with io.open(outfn, 'w', encoding='utf8') as outf:
            print('Writing text to %s' % outfn)
            outf.write(text + '\n')

        if 'ner' not in d['metadata']:
            print('No named entities found for %s' % d['file'])
            continue

        # Output relevant annotations into a brat .ann file
        ners = d['metadata']['ner']
        outfn = os.path.join(outdir, res_name[:-4] + '.ann')
        outf = io.open(outfn, 'w', encoding='utf8')
        print('Writing annotations to %s' % outfn)
        for (t, n) in enumerate(ners):
            outf.write('T%d\t%s %s %s\t%s\n' % \
                       (t+1, n['label'], n['begin'], n['end'], n['text']))
        outf.close()


def main():
    if len(sys.argv) != 3:
        usage()

    if not os.path.exists(sys.argv[1]):
        print 'Error: could not find JSON input file %s.' % sys.argv[1]
        usage()

    if not os.path.exists(sys.argv[2]):
        print 'Creating output directory %s.' % sys.argv[2]
        os.mkdir(sys.argv[2])
    else:
        print 'Removing prior output in %s.' % sys.argv[2]
        shutil.rmtree(sys.argv[2])
        os.mkdir(sys.argv[2])

    convert_json_to_brat(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()

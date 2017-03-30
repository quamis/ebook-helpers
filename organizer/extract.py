# -** coding: utf-8 -*-
import os, sys, re
import logging
import argparse

import Reader.EpubReader
import Reader.FilenameReader
import Reader.GoogleReader
import Reader.StatisticsReader

## export PYTHONIOENCODING="utf-8"
# pip install guess_language-spirit
# rm dump*.html; py ./extract.py --path=/d/nextcloud/EBooks/
# rm *.json;  py ./extract.py --path=/d/nextcloud/EBooks/testing-ebook-organizer/


"""
pip install epubzilla
pip install chartdet
pip install guess_language-spirit
"""

class FSWalker(object):
    def __init__(self, path):
        self.path = path
        self.namefilters = []
        
    def addNameFilter(self, regex):
        self.namefilters.append({
            'type': 'regex',
            'value': regex,
        })
        
        return self
        
    def walk(self, callback):
        for root, dirs, files in os.walk(self.path, topdown=True):
            files.sort()
            #for name in files:
            #for name in [f for f in files if f.search()]
            for name in files:
                doCall = True
                for nf in self.namefilters:
                    if nf['type']=='regex' and re.search(nf['value'], name, re.IGNORECASE) is None:
                        doCall = False
                        break
                
                if doCall:
                    callback(os.path.join(root, name))

        
        

def handle_file(path):
    print(path)
    
    book1 = Reader.FilenameReader.FilenameReader(path).process()
    print("    FilenameReader: [%2s] %s - %s    [%s lines, %s words]" %(book1.language, book1.author, book1.title, book1.lines, book1.words))
    
    book2 = Reader.EpubReader.EpubReader(path).process()
    print("    EpubReader:     [%2s] %s - %s    [%s lines, %s words]" %(book2.language, book2.author, book2.title, book2.lines, book2.words))
    
    #book3 = Reader.GoogleReader.GoogleReader(path).attachParsedData('FilenameReader', book1).attachParsedData('EpubReader', book2).process()
    #print("    GoogleReader  : [%2s] %s - %s    [%s lines, %s words]" %(book3.language, book3.author, book3.title, book3.lines, book3.words))
    
    
    book4 = Reader.StatisticsReader.StatisticsReader(path)\
        .attachParsedData('FilenameReader', book1)\
        .attachParsedData('EpubReader', book2)\
        .process()
        
    print("    StatisticsReader  : [%2s] %s - %s    [%s lines, %s words]" %(book4.language, book4.author, book4.title, book4.lines, book4.words))
    
   
    #print("-"*50)
    #exit()

if __name__ == '__main__':
    # handle args
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--path',  '-p',  dest='path',   action='store', type=str, default=None,  help='TODO')
    args = vars(parser.parse_args())
    
    #logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(name)s %(levelname)s %(message)s')
    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(message)s')
    
    fsw = FSWalker(args['path'])
    fsw.addNameFilter(r'\.epub$').walk(handle_file)
    
    print("=" * 50)

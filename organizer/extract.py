# -*- coding: utf-8 -*-
import os, sys, re
import logging
import argparse
import functools

import Reader.EpubReader
import Reader.FilenameReader
import Reader.GoogleReader
import Reader.StatisticsReader

## export PYTHONIOENCODING="utf-8"
# rm dump*.html; py ./extract.py --path=/d/nextcloud/EBooks/
# rm *.json;  py ./extract.py --updateStatistics=0 --reader=EpubReader --regexPattern='\.epub$' --db=stats.json --path=/d/nextcloud/EBooks/testing-ebook-organizer/
# rm *.json;  py ./extract.py --updateStatistics=0 --reader=EpubReader --regexPattern='\.epub$' --db=stats.json --path=/media/BIG/books/ro/

# rebuild db:
"""
rm *.json; py ./extract.py --updateStatistics=1 --reader=EpubReader --regexPattern='\.epub$' --db=stats.json --path=/d/nextcloud/EBooks/testing-ebook-organizer/; py ./extract.py --updateStatistics=1 --reader=FilenameReader --regexPattern='\.epub$' --db=stats.json --path=/d/nextcloud/EBooks/testing-ebook-organizer/;
py ./statistics.py --db=stats.json

"""


"""
pip install ebooklib
pip install guess_language-spirit
pip install google
pip install requests
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

        
        
class FileHandler(object):
    def __init__(self, reader, updateStatistics, db):
        self.reader = reader
        self.updateStatistics = updateStatistics
        self.db = db
        
        self.dirname = None
        
    def handle_file(self, path):
        dirname = os.path.dirname(path)
        if dirname!=self.dirname:
            print("%s" % (dirname))
            self.dirname = dirname
    
        print("    %s" % (os.path.basename(path)))
        
        book = None
        
        if self.reader=="FilenameReader":
            book = Reader.FilenameReader.FilenameReader(path).process()
        elif self.reader=="EpubReader":
            book = Reader.EpubReader.EpubReader(path).process()
        else:
            raise Exception("Unknown eader specified: %s" % (self.reader))
        
        #book = Reader.GoogleReader.GoogleReader(path).attachParsedData('FilenameReader', book1).attachParsedData('EpubReader', book2).process()
        
        print("      <%10s>: [%2s] %s - %s    [%s lines, %s words]" %(self.reader, book.language, book.author, book.title, book.lines, book.words))
        
        if self.updateStatistics:
            Reader.StatisticsReader.StatisticsReader(self.db)\
                .attachParsedData(self.reader, path, book)\
                .loadCache()\
                .deduplicate()\
                .saveCache()
            
        #print("-"*50)
        #exit()

if __name__ == '__main__':
    # handle args
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--path',  dest='path',   action='store', type=str, default=None,  help='TODO')
    parser.add_argument('--updateStatistics',  dest='updateStatistics',   action='store', type=int, default=0,  help='TODO')
    parser.add_argument('--reader',  dest='reader',   action='store', type=str, default=None,  help='TODO')
    parser.add_argument('--regexPattern',  dest='regexPattern',   action='store', type=str, default='\.epub$',  help='TODO')
    parser.add_argument('--db',  dest='db',   action='store', type=str, default=None,  help='TODO')
    args = vars(parser.parse_args())
    
    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(message)s')
    
    fsw = FSWalker(args['path'])
    fsh = FileHandler(args['reader'], args['updateStatistics'], args['db'])
    fsw.addNameFilter(args['regexPattern']).walk(fsh.handle_file)
    
    print("=" * 50)

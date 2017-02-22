# -** coding: utf-8 -*-
import os, sys, re
import logging
import argparse

import ebooklib
from ebooklib import epub

import chardet
import guess_language

import lxml.html

# pip install guess_language-spirit

# rm dump*.html; py ./extract.py --path=/d/nextcloud/EBooks/


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

        print("="*50)
    
def handle_epub(path):
    book = epub.read_epub(path)
    print(path)
    #print(dir(book))
    #print(book.title)
    print(book.language)
    print(book.get_metadata('DC', 'creator')[0][0])
    print(book.get_metadata('DC', 'title')[0][0])
    print(book.get_metadata('DC', 'subject')[0][0])
    print(book.get_metadata('DC', 'language')[0][0])
    print(book.metadata)
    #print(book.properties)
    
    """
        Items can be of type:
          - ITEM_UNKNOWN = 0
          - ITEM_IMAGE = 1
          - ITEM_STYLE = 2
          - ITEM_SCRIPT = 3
          - ITEM_NAVIGATION = 4
          - ITEM_VECTOR = 5
          - ITEM_FONT = 6
          - ITEM_VIDEO = 7
          - ITEM_AUDIO = 8
          - ITEM_DOCUMENT = 9
    """
    for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        print(item)
        
    itemidx=0
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        itemidx+=1
        #print(dir(item))
        #print(item.get_language())
        #print(item.lang)
        print(item.properties)
        #print(item.get_content())
        with open('dump1-%05d.html' % (itemidx), 'wb') as f:
            f.write(item.get_content())
        
        document = lxml.html.document_fromstring(item.get_content())
        #internally does: etree.XPath("string()")(document)
        #print(document.text_content().encode("utf-8"))
        with open('dump2-%05d.html' % (itemidx), 'wb') as f:
            #print(chardet.detect(document.text_content().encode('utf8')))
            print(guess_language.guess_language(document.text_content().encode('utf8').decode()))
            #print(document.text_content().encode('utf8'))
            f.write(document.text_content().encode('utf8'))
            
        
            
   
    print("-"*50)
    exit()

if __name__ == '__main__':
    # handle args
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--path',  '-p',  dest='path',   action='store', type=str, default=None,  help='TODO')
    args = vars(parser.parse_args())
    
    fsw = FSWalker(args['path'])
    fsw.addNameFilter(r'\.epub$').walk(handle_epub)

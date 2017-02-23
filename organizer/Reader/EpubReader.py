# -** coding: utf-8 -*-
import os, sys, re
import logging
import ebooklib
from ebooklib import epub
import chardet
import guess_language
import lxml.html


class EpubReader(object):
    def __init__(self, path):
        self.path = path
        
        self.author = None
        self.language = None
        self.title = None
        
        self.lines = None
        self.words = None
        
    def process(self):
        try:
            book = epub.read_epub(self.path)
        except:
            return self
    
        authors = []
        languages = []
        titles = []
        
        titles.append(book.title)
        languages.append(book.language)
        authors.append(self.getBookMetadata(book, 'DC', 'creator'))
        titles.append(self.getBookMetadata(book, 'DC', 'title'))
        languages.append(self.getBookMetadata(book, 'DC', 'subject'))
        languages.append(self.getBookMetadata(book, 'DC', 'language'))
        #print(book.metadata)
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
        #for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        #    print(item)
        
        content = b""
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            languages.append(item.get_language())
            languages.append(item.lang)
            #print(item.properties)
            #print(item.get_content())
            #with open('dump1-%05d.html' % (itemidx), 'wb') as f:
            #    f.write(item.get_content())
            
            document = lxml.html.document_fromstring(item.get_content())
            #print(document.text_content().encode("utf-8"))
            #with open('dump2-%05d.html' % (itemidx), 'wb') as f:
            #    f.write(document.text_content().encode('utf8'))
            
            content+= document.text_content().encode('utf8')
            languages.append(guess_language.guess_language(document.text_content().encode('utf8').decode()))
                
        lst = [l for l in languages if not l in (None, 'UNKNOWN', 'UND', )]
        if lst:
            self.language = max(set(lst), key=lst.count)
        
        lst = [l for l in authors if not l in (None, )]
        if lst:
            self.author = max(set(lst), key=lst.count)
        
        lst = [l for l in titles if not l in (None, )]
        if lst:
            self.title = max(set(lst), key=lst.count)
        
        content = content.decode('utf8')
        
        content = re.sub(r"[\r\n]+", '\n', content)
        content = re.sub(r"[-*]+", '', content)
        self.lines = len(content.split("\n"))
        
        content = re.sub(r"[\s\W]+", ' ', content)
        self.words = len([w for w in content.split(" ") if len(w)>3])
        
        return self
        
    def getBookMetadata(self, book, namespace, name):
        try:
            return book.get_metadata(namespace, name)[0][0]
        except:
            return None
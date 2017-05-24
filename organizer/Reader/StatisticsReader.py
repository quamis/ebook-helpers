# -** coding: utf-8 -*-
import os, sys, re, time
import logging
import json
from collections import OrderedDict

class StatisticsReader(object):
    def __init__(self, path, db):
        self.path = path
        self.db = db
        
        self.author = None
        self.language = None
        self.title = None
        
        self.lines = None
        self.words = None
        
        self.attachedData = {}
        
        self.list = []
        
    def attachParsedData(self, extractor, data):
        self.attachedData[extractor] = data
        return self
        
    def has_book(self, author, title, extractor):
        for b in self.list:
            if b['author']==author and b['title']==title and b['extractor']==extractor:
                return True
        return False
        
    def append_book(self, author, title, extractor):
        self.list.append({
            'author':       author,
            'title':        title,
            'extractor':    extractor,
        })
        
    def groupedByAuthorAndTitle(self):
        tree = {}
        for b in self.list:
            if not b['author'] in tree:
                tree[b['author']] = {}
                
            if not b['title'] in tree[b['author']]:
                tree[b['author']][b['title']] = []
                
            tree[b['author']][b['title']].append(b['extractor'])
        
        return tree
        
    def groupedByTitleAndAuthor(self):
        tree = {}
        for b in self.list:
            if not b['title'] in tree:
                tree[b['title']] = {}
                
            if not b['author'] in tree[b['title']]:
                tree[b['title']][b['author']] = []
                
            tree[b['title']][b['author']].append(b['extractor'])
        
        tree_ordered = [OrderedDict(sorted(tree.items(), key=lambda item: ('' if item[0] is None else item[0]))) for item in tree]
        
        return tree_ordered
        
    def loadCache(self):
        if os.path.exists(self.db):
            with open(self.db, 'rb') as f:
                self.list = json.loads(f.read().decode('utf-8'))
                
    def saveCache(self):
        with open(self.db, 'wt') as f:
            json.dump(self.list, f, indent=4, sort_keys=True)
            
    def process(self):
        self.loadCache()
        
        for extractor in self.attachedData:
            author = self.attachedData[extractor].author
            title = self.attachedData[extractor].title
            
            if author:
                author = author.strip()
                
            if title:
                title = title.strip()
            
            if not self.has_book(author, title, extractor):
                self.append_book(author, title, extractor)
                
        
        self.saveCache()
        #print(json.dumps(self.groupedByAuthorAndTitle(), indent=4, sort_keys=True))
        #print(json.dumps(self.groupedByTitleAndAuthor(), indent=4, sort_keys=True))
        
        return self

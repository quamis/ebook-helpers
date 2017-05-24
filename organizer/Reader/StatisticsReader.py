# -** coding: utf-8 -*-
import os, sys, re, time
import logging
import json
from collections import OrderedDict

class StatisticsReader(object):
    def __init__(self, db):
        self.db = db
        
        self.author = None
        self.language = None
        self.title = None
        
        self.lines = None
        self.words = None
        
        self.attachedData = []
        
        self.list = []
        
    def attachParsedData(self, reader, path, book):
        self.attachedData.append({ 'reader':reader, 'path':path, 'book':book })
        return self
        
    def has_book(self, data):
        for b in self.list:
            if b['author']==data['book'].author and b['title']==data['book'].title and b['reader']==data['reader'] and b['path']==data['path']:
                return True
        return False
        
    def append_book(self, data):
        self.list.append({
            'path':         data['path'],
            'reader':       data['reader'],
            'author':       data['book'].author,
            'title':        data['book'].title,
        })
        
    def groupedByAuthorAndTitle(self):
        tree = {}
        for b in self.list:
            if not b['author'] in tree:
                tree[b['author']] = {}
                
            if not b['title'] in tree[b['author']]:
                tree[b['author']][b['title']] = []
                
            tree[b['author']][b['title']].append(b['reader'])
        
        return tree
        
    def groupedByTitleAndAuthor(self):
        tree = {}
        for b in self.list:
            if not b['title'] in tree:
                tree[b['title']] = {}
                
            if not b['author'] in tree[b['title']]:
                tree[b['title']][b['author']] = []
                
            tree[b['title']][b['author']].append(b['reader'])
        
        tree_ordered = [OrderedDict(sorted(tree.items(), key=lambda item: ('' if item[0] is None else item[0]))) for item in tree]
        
        return tree_ordered
        
    def loadCache(self):
        if os.path.exists(self.db):
            with open(self.db, 'rb') as f:
                self.list = json.loads(f.read().decode('utf-8'))
        return self
                
    def saveCache(self):
        with open(self.db, 'wt') as f:
            json.dump(self.list, f, indent=4, sort_keys=True)
        return self
            
    def deduplicate(self):
        for data in self.attachedData:
            path = data['path']
            author = data['book'].author
            title = data['book'].title
            
            if author:
                author = author.strip()
                
            if title:
                title = title.strip()
            
            if not self.has_book(data):
                self.append_book(data)
                
        
        return self

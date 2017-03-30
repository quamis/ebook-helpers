# -** coding: utf-8 -*-
import os, sys, re
import logging


class FilenameReader(object):
    def __init__(self, path):
        self.path = path
        
        self.author = None
        self.language = None
        self.title = None
        
        self.lines = None
        self.words = None
        
    def process(self):
        print(os.path.basename(self.path))
        m = re.search(r"^[\s]*(?P<author>.+)[\s]*-[\s]*(?P<title>.+?)[\s]*(\((?P<language>(EN|FR|RO))\))?[\s]*\.(?P<extension>epub|pdf|rtf)$", os.path.basename(self.path), re.IGNORECASE)
        if m:
            self.author = m.group('author')
            self.title = m.group('title')
            
            if m.group('language'):
                self.language = m.group('language').lower()
            
            return self
                
        m = re.search(r"^[\s]*(?P<title>.+)(\((?P<language>(EN|FR|RO))\))?[\s]*\.(?P<extension>epub|pdf|rtf)$", os.path.basename(self.path), re.IGNORECASE)
        if m:
            self.title = m.group('title')
            
            return self
    
        return self

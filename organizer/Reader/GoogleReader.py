# -** coding: utf-8 -*-
import os, sys, re
import logging
import google


class GoogleReader(object):
    def __init__(self, path):
        self.path = path
        
        self.author = None
        self.language = None
        self.title = None
        
        self.lines = None
        self.words = None
        
    def process(self):
        q = os.path.basename(self.path)
        q = re.sub(r"(epub|pdf|rtf)$", '', q, re.IGNORECASE)
        q = re.sub(r"(ro|en|fr)", '', q, re.IGNORECASE)
        q = re.sub(r"[\(\)\.\,\-]", '', q, re.IGNORECASE)
        q = re.sub(r"[\s]+", ' ', q, re.IGNORECASE)
        print(q)
        
        for url in google.search(q+" wikipedia", tld='ro', stop=5):
            print(url)
            
        print("-"*50)
        for url in google.search(q+" amazon", stop=5):
            print(url)
            
        exit()
        m = re.search(r"^[\s]*(?P<author>.+)[\s]*-[\s]*(?P<title>.+)[\s]*\.(?P<extension>epub|pdf|rtf)$", os.path.basename(self.path), re.IGNORECASE)
        if m:
            self.author = m.group('author')
            self.title = m.group('title')
    
        return self

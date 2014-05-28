# -** coding: utf-8 -*-
import os, sys
import logging
import re

class authorWalker(object):
    def __init__(self, path):
        self.path = path
        
    def run(self):
        self.listAuthors()
        
    def listAuthors(self):
        for author in os.listdir(self.path):
            self._authorFound(self.path, author)
    
    def _authorFound(self, path, author):
        pass
    
class authorFolderFormatValidator(authorWalker):
    def _authorFound(self, path, author):
        return self.checkAuthorName(author)
    
    def checkAuthorName(self, author):
        m = re.match("^([\w\s\.]+|[A-Z]\.), ([\w\s\.]+|[A-Z]\.)$", author, re.UNICODE)
        if m:
            return True
        
        print "'%s' has an invalid format. Please fix it" % (author)
        return False


if __name__ == '__main__':
    wlk = authorFolderFormatValidator(u'/media/BIG/owncloud/lucian.sirbu/files/books/all-01/')
    wlk.run()


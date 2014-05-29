# -** coding: utf-8 -*-
import os, sys
import logging
import re
import collections

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

class AuthorInfoException(Exception):
    pass
    
class AuthorInfo(object):        
    def __init__(self, author):
        self.raw = author
        self.firstName = None
        self.lastName = None
        
    def extract(self):
        m = re.match("^(?P<firstName>[\w\s\.]+|[A-Z]\.), (?P<lastName>[\w\s\.]+|[A-Z]\.)$", self.raw, re.UNICODE)
        if m is None:
            raise AuthorInfoException("Invalid author name")
        
        self.firstName = m.group('firstName')
        self.lastName = m.group('lastName')
        
class authorFolderFormatValidator(authorWalker):
    def _authorFound(self, path, author):
        try:
            a = AuthorInfo(author)
            a.extract()
        except AuthorInfoException, e:
            print "'%s' has an invalid format. Please fix it" % (author)
            return False
        
        self.checkFolderStructure(a, author)
        
    def reformatFilename(self, authorInfo, path, el, depth):
        #print "      %s%s" % ("    "*depth, el)
        
        """
            exp: Authorf, Authorl - Book Name.ext
        """
        
        authorAssoc = collections.OrderedDict()  # front-replacements
        authorAssoc['Caragiale, Ion Luca'] = ['I.L.Caragiale', 'I L Caragiale']
        
        frepl = collections.OrderedDict()  # front-replacements
        brepl = collections.OrderedDict()  # back-replacements
        crepl = collections.OrderedDict()  # custom-replacements, VERY dangerous
        
        #######################################################
        # front-replacements
        # remove Authorf, Authorl
        frepl['%s, %s'%(authorInfo.firstName, authorInfo.lastName)] = '' 
        frepl['%s, %s'%(authorInfo.lastName, authorInfo.firstName)] = '' 
        frepl['%s %s'%(authorInfo.firstName, authorInfo.lastName)] = '' 
        frepl['%s %s'%(authorInfo.lastName, authorInfo.firstName)] = '' 
        frepl['%s'%(authorInfo.lastName)] = '' 
        frepl['%s'%(authorInfo.firstName)] = '' 
        
        if authorInfo.raw in authorAssoc:
            for r in authorAssoc[authorInfo.raw]:
                frepl[r] = ''
                brepl[r] = ''
        
        # remove delimiter between "Authorf, Authorl" and "Book Name"
        frepl['[\s]+\-[\s]+'] = ''
        frepl['\-[\s]+'] = ''
        frepl['\-'] = ''
        
        #######################################################
        # back-replacements
        brepl['%s, %s'%(authorInfo.firstName, authorInfo.lastName)] = '' 
        brepl['%s, %s'%(authorInfo.lastName, authorInfo.firstName)] = '' 
        brepl['%s %s'%(authorInfo.firstName, authorInfo.lastName)] = '' 
        brepl['%s %s'%(authorInfo.lastName, authorInfo.firstName)] = '' 
        
        brepl['[\s]+\-[\s]+'] = ''
        brepl['[\s]+\-'] = ''
        brepl['\-[\s]+'] = ''
        brepl['\-'] = ''
        
        #######################################################
        # custom-replacements, VERY dangerous
        crepl['\_'] = ' '
        crepl['\(BookZa.org\)'] = ''
        crepl['\(Bookos.org\)'] = ''
        crepl['\(Cartea\)'] = ''
        
        
        # do the actual replacements
        eln = el
        for r in frepl:
            eln = re.sub("^"+r, frepl[r], eln, re.UNICODE)
            
        for r in brepl:
            eln = re.sub(r+"(?P<ext>\.[a-zA-Z]{3,4})$", brepl[r]+"\g<ext>", eln, re.UNICODE)
            
        for r in crepl:
            eln = re.sub(r, crepl[r], eln, re.UNICODE)
            
        eln = re.sub("[\s]*(?P<ext>\.[a-zA-Z]{3,4})$", "\g<ext>", eln, re.UNICODE)
            
        print "'%s' --> '%s'" % (el, eln)

        
    def checkFolderStructure(self, authorInfo, path, depth=0):
        print "  %s%s" % ("  "*depth, path)
        p = self.path+path+'/'
        for el in os.listdir(p):
            if os.path.isdir(p+el):
                self.checkFolderStructure(authorInfo, path+'/'+el, depth+1)
            else:
                self.reformatFilename(authorInfo, path+'/'+el, el, depth)

                

class authorFolderStats(authorWalker):
    def __init__(self, path):
        super(type(self), self).__init__(path)

    def reset(self):
        self.stats = {
            'files': 0,
            'fileTypes': {},
        }
        
    def run(self):
        super(type(self), self).run()
        
    def _authorFound(self, path, author):
        self.reset()
        self.gatherAuthorInfo(author)
        print self.stats
        return True
    
    def gatherAuthorInfo(self, path, depth=0):
        print "  %s%s" % ("  "*depth, path)
        p = self.path+path+'/'
        for el in os.listdir(p):
            if os.path.isdir(p+el):
                print "      %s%s/" % ("    "*depth, el)
                self.gatherAuthorInfo(path+'/'+el, depth+1)
            else:
                print "      %s%s" % ("    "*depth, el)
                self.stats['files']+=1
                
                ext = os.path.splitext(el)[1]
                if ext not in self.stats['fileTypes']:
                    self.stats['fileTypes'][ext] = 0
                self.stats['fileTypes'][ext]+=1
        
        
if __name__ == '__main__':
    ## first run "export PYTHONIOENCODING=utf-8"
    
    wlk = authorFolderFormatValidator(u'/media/BIG/owncloud/lucian.sirbu/files/books/all-01/')
    wlk.run()
    
    #wlk = authorFolderStats(u'/media/BIG/owncloud/lucian.sirbu/files/books/all-01/')
    #wlk.run()


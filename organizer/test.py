# -** coding: utf-8 -*-
import os, sys
import logging
import re
import collections
import argparse
import requests

class authorWalker(object):
    def __init__(self, path):
        self.path = path
        
    def run(self):
        self.listAuthors()
        
    def listAuthors(self):
        authors = os.listdir(self.path)
        authors.sort()
        for author in authors:
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
        self.associates = []
        self.authors = 0
        
    def extract(self):
        if self.raw in ('Stendhal', 'Tobias', 'Homer', 'Perpessicius', 'Platon'):
            self.firstName =  self.raw
            self.lastName = ''
            return
        
        found = True
        if not found:
            m = re.search('^(?P<firstName>[\w\s\.\-]+|[A-Z]\.), (?P<lastName>[\w\s\.]+|[A-Z]\.)$', self.raw.decode('utf-8'), re.UNICODE)
            if m is None:
                found = false
            else:
                self.authors = 1
                self.firstName = m.group('firstName')
                self.lastName = m.group('lastName')
        
        # lookup 2 authors
        if not found:
            m = re.search('^(?P<firstName1>[\w\s\.\-]+|[A-Z]\.), (?P<lastName1>[\w\s\.]+|[A-Z]\.) \& (?P<firstName2>[\w\s\.\-]+|[A-Z]\.), (?P<lastName2>[\w\s\.]+|[A-Z]\.)$', self.raw.decode('utf-8'), re.UNICODE)
            if m is None:
                found = false
            else:
                self.authors = 2
                self.firstName = m.group('firstName1')
                self.lastName = m.group('lastName1')
                
                a = AuthorInfo()
                a.firstName = m.group('firstName2')
                a.lastName = m.group('lastName2')
                self.associates.append(a)
                
        if not found:
            raise AuthorInfoException("Invalid author name")
        
        
        
class authorFolderFormatValidator(authorWalker):
    def _authorFound(self, path, author):
        try:
            a = AuthorInfo(author)
            a.extract()
        except AuthorInfoException, e:
            print "'%s' has an invalid format. Please fix it(%s)" % (author, e)
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
            
        #if el!=eln:
        #    print "'%s' --> '%s'" % (el, eln)

        
    def checkFolderStructure(self, authorInfo, path, depth=0):
        #print "  %s%s" % ("  "*depth, path)
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
        #print "%s: %s" % (author, self.stats)
        
        authorInfo = authorFolderInfo_Wikipedia(author)
        authorInfo.getInfo()
        #print authorInfo.hits
        #print authorInfo.suggestions
        
        print "%s: %d files (%s)" % (author, self.stats['files'], ",".join(self.stats['fileTypes'].keys()).replace(".", ""))
        if authorInfo.hits==0:
            print "    got no hits on wikipedia. This author name might be misspelled"
        elif authorInfo.hits<2:
            print "    got too few hits on wikipedia(%d ). This author name might be misspelled" % (authorInfo.hits)
        elif authorInfo.hits>700:
            print "    got many hits on wikipedia(%d). He should be an interesting read" % (authorInfo.hits)
            
        if len(authorInfo.suggestions):
            print "    got suggestions: %s. You may have mispelled his name" % (authorInfo.suggestions)
        
        return True
    
    def gatherAuthorInfo(self, path, depth=0):
        #print "  %s%s" % ("  "*depth, path)
        p = self.path+path+'/'
        for el in os.listdir(p):
            if os.path.isdir(p+el):
                #print "      %s%s/" % ("    "*depth, el)
                self.gatherAuthorInfo(path+'/'+el, depth+1)
            else:
                #print "      %s%s" % ("    "*depth, el)
                self.stats['files']+=1
                
                ext = os.path.splitext(el)[1]
                if ext not in self.stats['fileTypes']:
                    self.stats['fileTypes'][ext] = 0
                self.stats['fileTypes'][ext]+=1

class authorFolderInfo_Wikipedia(object):
    def __init__(self, author):
        self.author = author
        self.suggestions = []
        self.hits = 0
        self.description = ""
        
    def getInfo(self):
        params = {
            'action':'query',
            'list':'search',
            'format':'json',
            'srlimit':'10',
            'srwhat':'text',
            'srprop':'score',
            'srprop':'size',
            'srsearch':self.author,
        }
        r = requests.get("http://en.wikipedia.org/w/api.php", params=params)

        json = r.json()
        self.hits = json['query']['searchinfo']['totalhits']
        
        if u'suggestion' in json['query']['searchinfo']:
            self.suggestions.append(json['query']['searchinfo'][u'suggestion'])
        
        
if __name__ == '__main__':
    # handle args
    parser = argparse.ArgumentParser(description='Check the specified path and report invalid files')
    parser.add_argument('--path',  '-p',  dest='path',   action='store', type=str, default=None,  help='TODO')
    args = vars(parser.parse_args())

    ## first run "export PYTHONIOENCODING=utf-8"
    
    #wlk = authorFolderFormatValidator(args['path'])
    #wlk.run()
    
    wlk = authorFolderStats(args['path'])
    wlk.run()


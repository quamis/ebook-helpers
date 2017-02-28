# -** coding: utf-8 -*-
import os, sys, re, time
import logging
import google, requests
import lxml.html

class GoogleReader(object):
    def __init__(self, path):
        self.path = path
        
        self.author = None
        self.language = None
        self.title = None
        
        self.lines = None
        self.words = None
        
        self.attachedData = {}
        
    def attachParsedData(self, extractor, data):
        self.attachedData[extractor] = data
        return self
        
    def search_ro_wikipedia_org(self, query):
        authors = []
        titles = []
        logging.getLogger('reader').debug("Try ro.wikipedia.org")
        for url in google.search(query+" carte site:ro.wikipedia.org", tld='ro', num=5, stop=1):
            logging.getLogger('reader').debug("    %s", url)
            page = requests.get(url)
            
            xmldocument = lxml.html.document_fromstring(page.text)
            text = " ".join(xmldocument.xpath("//*[@id='mw-content-text']//text()"))
            
            matches = re.finditer("(scris de|autor|autorul)[\s]+(?P<author>[^\.\,\n]+)", text, re.IGNORECASE)
            for m in matches:
                authors.append(m.group('author'))
                
            time.sleep(0.75)
                
        ret = {
            'author': None,
            'authors': [],
            'title': None,
            'titles': [],
        }
        
        lst = [l for l in authors if not l in (None, '', )]
        if lst:
            ret['author'] = max(set(lst), key=lst.count)
            ret['authors'] = lst
        
        if ret['author']:
            title = re.sub("|".join(ret['author'].split()), '', query, re.IGNORECASE)
            ret['title'] = title
            ret['titles'].append(ret['title'])
        
        return ret
            
    def search_en_wikipedia_org(self, query):
        """ DELETE ALL THIS CODE
        authors = []
        titles = []
        logging.getLogger('reader').debug("Try en.wikipedia.org")
        for url in google.search(query+" book site:en.wikipedia.org", num=5, stop=1):
            logging.getLogger('reader').debug("    %s", url)
            page = requests.get(url)
            
            xmldocument = lxml.html.document_fromstring(page.text)
            text = " ".join(xmldocument.xpath("//*[@id='mw-content-text']//text()"))

            matches = re.finditer("(scris de|autor|autorul)[\s]+(?P<author>[^\.\,\n]+)", text, re.IGNORECASE)
            for m in matches:
                authors.append(m.group('author'))
        """
        ret = {
            'author': None,
            'authors': [],
            'title': None,
            'titles': [],
        }
        
        return ret
        
    def search_amazon_com(self, query):
        authors = []
        titles = []
        logging.getLogger('reader').debug("Try amazon.com")
        for url in google.search(query+" book site:amazon.com", num=5, stop=1):
            logging.getLogger('reader').debug("    %s", url)
            page = requests.get(url)
            
            xmldocument = lxml.html.document_fromstring(page.text)
            text = " ".join(xmldocument.xpath("//*[contains(@class, 'contributorNameID')]//text()"))

            authors.append(text)
            
            time.sleep(2)
                
        ret = {
            'author': None,
            'authors': [],
            'title': None,
            'titles': [],
        }
        
        lst = [l for l in authors if not l in (None, '', )]
        print(lst)
        if lst:
            ret['author'] = max(set(lst), key=lst.count)
            ret['authors'] = lst
        
        if ret['author']:
            title = re.sub("|".join(ret['author'].split()), '', query, re.IGNORECASE)
            ret['title'] = title
            ret['titles'].append(ret['title'])
        
        return ret
        
    def process(self):
        q = os.path.basename(self.path)
        q = re.sub(r"(epub|pdf|rtf)$", '', q, re.IGNORECASE)
        q = re.sub(r"(ro|en|fr)", '', q, re.IGNORECASE)
        q = re.sub(r"[\(\)\.\,\-]", '', q, re.IGNORECASE)
        q = re.sub(r"[\s]+", ' ', q, re.IGNORECASE)
        print(q)

        collectedData = []
        collectedData.append(self.search_ro_wikipedia_org(q))
        collectedData.append(self.search_en_wikipedia_org(q))
        collectedData.append(self.search_amazon_com(q))
        
        print(collectedData)
        
        exit()
        m = re.search(r"^[\s]*(?P<author>.+)[\s]*-[\s]*(?P<title>.+)[\s]*\.(?P<extension>epub|pdf|rtf)$", os.path.basename(self.path), re.IGNORECASE)
        if m:
            self.author = m.group('author')
            self.title = m.group('title')
    
        return self

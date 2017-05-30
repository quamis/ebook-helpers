# -** coding: utf-8 -*-
import os, sys, re, json
import logging
import argparse

import Reader.EpubReader
import Reader.FilenameReader
import Reader.GoogleReader
import Reader.StatisticsReader

## export PYTHONIOENCODING="utf-8"
# py ./statistics.py --db=StatisticsReader.tree.json


if __name__ == '__main__':
    # handle args
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('--db',  '-db',  dest='db',   action='store', type=str, default=None,  help='TODO')
    args = vars(parser.parse_args())
    
    #logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(name)s %(levelname)s %(message)s')
    logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(message)s')
    
    stats = Reader.StatisticsReader.StatisticsReader(args['db'])
        
    stats.loadCache()
    
    authors = []
    for (author, books) in stats.groupedByAuthorAndTitle().items():
        authors.append(author)
        #print(books)
        
    for (author, books) in stats.groupedByAuthorAndTitle().items():
        for (book, d) in books.items():
            if not (book in authors):
                #print("    this book might be an author: %s" % (book))
                print("    author: %s" % (author))
        
    #print(json.dumps(stats.groupedByAuthorAndTitle(), indent=4))
    

    """
    for fixing author/titles, there some cases:
        - titles are slightly different, the longer one might contain more details
        - author and title are reversed between readers
        
        
    we should: 
        - build a list of validated authors, with possible aliases
        - from this, we might get more certain about what the book title actually is
    """
    
    print("=" * 50)

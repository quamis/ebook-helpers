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
    
    stats = Reader.StatisticsReader.StatisticsReader(None, args['db'])
        
    stats.loadCache()
    #stats.groupedByAuthorAndTitle()
    print(json.dumps(stats.groupedByAuthorAndTitle(), indent=4))
    
    
    print("=" * 50)

# -** coding: utf-8 -*-
import os, sys, re, time
import logging

class StatisticsReader(object):
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
        
    def process(self):
        return self

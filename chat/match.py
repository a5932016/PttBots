import json
import os
import random

from .Matcher.bm25Matcher import bestMatchingMatcher

from .Matcher.matcher import Matcher

def getMatcher(matcherType,removeStopWords=False):
    """
    回傳初始完畢的 Matcher

    Args:
        - matcherType:要使用哪種字串匹配方式
            - Fuzzy
            - WordWeight
        - sort:
            - a boolean value for fuzzy sorting match.
    """

    if matcherType == "bm25":
        return bm25()
    else:
        print("[Error]: Invailded type.")
        exit()

def bm25():
    bm25Matcher = bestMatchingMatcher()
    bm25Matcher.loadTitles(path="chat/data/Titles.txt")
    bm25Matcher.initialize()
    return bm25Matcher

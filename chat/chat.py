import json
import os
import random
import logging

import chat.match as match
from .responsesEvaluate import Evaluator

def testSegment(matcher):
    logging.info("測試斷詞模塊中")
    try:
        matcher.wordSegmentation("測試一下斷詞")
        logging.info("測試成功")
    except Exception as e:
        logging.info(repr(e))
        logging.info("模塊載入失敗，請確認data與字典齊全")

def getResponse(query,matcher,evaluator,threshold=5):
    title,index = matcher.match(query)
    sim = matcher.getSimilarity()
    if sim < threshold:#sim < threshold
        return "超出我的理解能力了"
    else:
        res = json.load(open(os.path.join("chat/data/processed_seged/reply/",str(int(index/1000))+'.json'),'r',encoding='utf-8'))
        targetId = index % 1000
        candiates = evaluator.getBestResponse(res[targetId],topk=3)
        reply = randomPick(candiates)
        return reply

def randomPick(answers):
    try:
        answer = answers[random.randrange(0,len(answers))][0]
    except:
        answer = "沒有資料"
    return answer


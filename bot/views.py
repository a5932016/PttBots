from django.shortcuts import render

# Create your views here.

# import 必要的函式庫
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

import manage
import chat.chat as ChatRespon
import chat.match as match
from chat.responsesEvaluate import Evaluator

# 這邊是Linebot的授權TOKEN(等等註冊LineDeveloper帳號會取得)，我們為DEMO方便暫時存在settings裡面存取，實際上使用的時候記得設成環境變數，不要公開在程式碼裡喔！
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        # GB = GossipBot()

        # if cache.get('matcher'):
        #     matcher = cache.get('matcher')
        # else:
        #     matcher = match.getMatcher('bm25')
        #     cache_key = 'matcher'
        #     cache_time = None
        #     data = matcher
        #     cache.set(cache_key, data, cache_time)
        #
        # if cache.get('evaluator'):
        #     evaluator=cache.get('evaluator')
        # else:
        #     evaluator = Evaluator()
        #     cache_key = 'evaluator'
        #     cache_time = None
        #     data = evaluator
        #     cache.set(cache_key, data, cache_time)

        matcher = manage.matcher
        evaluator = manage.evaluator

        for event in events:
            if isinstance(event, MessageEvent):
                chattext = ChatRespon.getResponse(event.message.text,matcher,evaluator)
                # chattext='test'
                line_bot_api.reply_message(
                    event.reply_token,
                   TextSendMessage(text=chattext)
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

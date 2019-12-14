from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, PostbackEvent, BeaconEvent
)

from .models import User
from .serializers import UserSerializer

bot = LineBotApi(
    'Wi0UaiRY4OA/CzhJxRf7E+wIapbEUfawu9YDyz3O3bxQK3nsOiR+gIbMXrQxjEmM4RIiOps56z/c9+BjSAdHbO0fqHVdLbF+eKaewPQV5TwnXKZOa7eL/z254NpTLBhco3u8zTMpscnjmvqNG3FGjgdB04t89/1O/w1cDnyilFU='
)
handler = WebhookHandler('edd35e8453bd3b9715cb6e30941c196a')


# Create your views here.
@api_view(['GET', 'POST'])
def webhook(request):
    # signature = request.headers['X-Line-Signature']
    #
    # body = request.get_data(as_text=True)
    # try:
    #     handler.handle(body, signature)
    # except InvalidSignatureError:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse("OK")


@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.data
    data = data.split('&')
    dict = {}

    for item in data:
        temp = item.split('=')
        dict[temp[0]] = temp[1]

    dict["userID"] = event.source.userId
    bot.reply_message(event.replyToken, TextSendMessage(text="Confirmed"))
    confirm_attendance(dict["classID"], dict["sessionID"], dict["userID"])


@handler.add(BeaconEvent)
def handle_beacon(event):
    time = event.timestamp
    userID = event.source.userId
    verifyUserID(userID)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    bot.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


# verify that user is registered
def verifyUserID(userID):
    # send confirmation flex message if user is verified
    pass


def sendConfirmation(classID, sessionID, userID):
    dataString = "classID=" + classID + "&sessionID=" + sessionID
    try:
        bot.push_message(userID, FlexSendMessage(alt_text="Confirm your attendance", contents={
            "type": "bubble",
            "direction": "ltr",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ]
            },
            "hero": {
                "type": "image",
                "url": "https://i.imgur.com/EP3JNSS.png",
                "align": "center",
                "gravity": "center",
                "size": "4xl",
                "aspectRatio": "1.51:1",
                "aspectMode": "fit",
                "backgroundColor": "#FFFFFF"
            },
            "footer": {
                "type": "box",
                "layout": "horizontal",
                "backgroundColor": "#464F69",
                "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "Confirm Attendance",
                                    "text": "Confirm Attendance",
                                    "data": dataString
                                },
                                "color": "#ffffff"
                            }
                        ]
                    }
                ]
            }
        }
                                                 ))
    except LineBotApiError as e:
        return


# confirm attendance after user clicks confirm in line bot
def confirm_attendance(classID, sessionID, userID):
    pass


@api_view(['GET', 'POST'])
def user_test(request):
    if request.method == 'GET':
        qs = User.objects.all()
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class list_user(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from django.http import HttpResponse
from django.shortcuts import render

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from django.http import HttpRequest

from .models import User
from .serializers import UserSerializer
import service


from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, PostbackEvent, BeaconEvent
)
from linebot import (
    LineBotApi, WebhookHandler
)

handler = WebhookHandler('edd35e8453bd3b9715cb6e30941c196a')


# Create your views here.
@api_view(['GET', 'POST'])
def webhook(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse("OK")


@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    data = data.split('&')
    dict = {}

    for item in data:
        temp = item.split('=')
        dict[temp[0]] = temp[1]

    dict["userID"] = event.source.user_id
    service.sendTextBroadcast(data)
    service.confirm_attendance(
        dict["classID"], dict["sessionID"], dict["userID"])


@handler.add(BeaconEvent)
def handle_beacon(event):
    time = event.timestamp
    userID = event.source.user_id
    service.verifyUserID(userID)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = "from token: {} message: {}".format(
        event.reply_token, event.message.text)
    service.sendtextMessage(event.reply_token, msg)


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

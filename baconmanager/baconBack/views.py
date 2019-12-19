from django.http import HttpResponse, Http404
from django.shortcuts import render

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from django.http import HttpRequest
from datetime import datetime


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, PostbackEvent, BeaconEvent
)

from .models import *
from .serializers import *


bot = LineBotApi(
    'Wi0UaiRY4OA/CzhJxRf7E+wIapbEUfawu9YDyz3O3bxQK3nsOiR+gIbMXrQxjEmM4RIiOps56z/c9+BjSAdHbO0fqHVdLbF+eKaewPQV5TwnXKZOa7eL/z254NpTLBhco3u8zTMpscnjmvqNG3FGjgdB04t89/1O/w1cDnyilFU='
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
    data_dict = {}

    for item in data:
        temp = item.split('=')
        data_dict[temp[0]] = temp[1]

    data_dict["userID"] = event.source.user_id
    bot.reply_message(event.reply_token, TextSendMessage(text="Confirmed"))
    print("From postback",data_dict["classID"], data_dict["sessionID"], data_dict["userID"])
    confirm_attendance(data_dict["classID"], data_dict["sessionID"], data_dict["userID"])


@handler.add(BeaconEvent)
def handle_beacon(event):
    time = event.timestamp
    userID = event.source.user_id
    if event.beacon.type == "enter":
        handleBeaconActivity(userID, event.beacon.hwid, time)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "attend":
        r = message_confirm()
        bot.reply_message(
            event.reply_token,
            TextSendMessage(text=r))

    # verify that user is registered and has not confirmed attendance yet


def handleBeaconActivity(userID, hwid, timestamp):
    print(timestamp)
    print("user in db = {} and member is db = {}". format(User.objects.filter(ID=userID).exists(), Member.objects.filter(classID=hwid).exists()))
    if User.objects.filter(ID=userID).exists() and Member.objects.filter(classID=hwid).exists():
        print("sending confirmation")
        # and Session.objects.filter(ClassID=hwid).exists()
        sendConfirmation(hwid, 1234, userID)

        return "Sended"

    return None


def sendConfirmation(classID, sessionID, userID):
    dataString = "classID=" + str(classID) + "&sessionID=" + str(sessionID)
    print("Pusing confirmation"+dataString)
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


# confirm attendance after user clicks confirm in flex message
def confirm_attendance(classID, sessionID, userID):
    print("Confirm")
    data = {"ClassID": classID, "SessionID": 1234, "UserID": userID}
    serializer = AttendanceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

def message_confirm():
    print("message Confirm")
    data = {"classID": "0136a2e901", "sessionID": 1234, "userID": "Ue83f590e1d7f1125364d32ae8091a2e7"}
    serializer = AttendanceSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return "success"

class UserList(APIView):

    def get(self, request, format=None):
        qs = User.objects.all()
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        qs = self.get_object(pk)
        serializer = UserSerializer(qs)
        return Response(serializer.data)

class AttendanceList(APIView):

    def get(self, request, format=None):
        qs = Attendance.objects.all()
        serializer = AttendanceSerializer(qs, many=True)
        for i in serializer.data:
            u = User.objects.get(pk=i['userID'])
            i['userInfo'] = UserSerializer(u).data
        response = Response(serializer.data)
        return response

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = AttendanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttendanceDetail(APIView):

    def get_object(self, pk):
        try:
            return Attendance.objects.get(pk=pk)
        except Attendance.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        qs = self.get_object(pk)
        serializer = AttendanceSerializer(qs)
        return Response(serializer.data)

"""
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
"""
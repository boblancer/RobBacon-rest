from .models import *

# verify that user is registered
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, PostbackEvent, BeaconEvent
)

bot = LineBotApi(
    'Wi0UaiRY4OA/CzhJxRf7E+wIapbEUfawu9YDyz3O3bxQK3nsOiR+gIbMXrQxjEmM4RIiOps56z/c9+BjSAdHbO0fqHVdLbF+eKaewPQV5TwnXKZOa7eL/z254NpTLBhco3u8zTMpscnjmvqNG3FGjgdB04t89/1O/w1cDnyilFU='
)


def verifyUserID(userID):
    if User.objects.filter(id=userID).exists():

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


def sendtextMessage(token, msg):
    bot.reply_message(token, TextSendMessage(text=msg))


def sendTextBroadcast(msg):
    bot.broadcast(TextSendMessage(text=msg))

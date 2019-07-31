from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import sys
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET       = os.environ.get("LINE_CHANNEL_SECRET")

if LINE_CHANNEL_ACCESS_TOKEN is None:
    sys.stderr.write("$LINE_CHANNEL_ACCESS_TOKEN must be set.")
if LINE_CHANNEL_SECRET is None:
    sys.stderr.write("$LINE_CHANNEL_SECRET must be set.")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler      = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback() -> str:
    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def response_message(event):
    line_bot_api.TextSendMessage(text="ほまれ is tinko")

if __name__ == "__main__":
    app.run()
import requests

myToken = "xoxb-2052522591507-2052320543234-gy74xwsRWRPYEp3j8voVGQM5"


def post_message(token, channel, text):
    """slack api에 메세지를 보내달라고 요청"""
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer " + token},
        data={"channel": channel, "text": text},
    )
    print(response)


# if __name__ == "__main__":
#     post_message(myToken, "#auto_bot", "테스트 메세지")

#############################  twilio api 본인한테만 문자 가능한듯(무료버젼이라) ####

# pip install twilio <- 이거 해야합니다!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# twilio 문자보내기
import os
from twilio.rest import Client
# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "ACa0a888268f1ccccc271e417826c74886"
auth_token = "18d1c29db7eec5b093ee24bd6069e2f7"
client = Client(account_sid, auth_token)
message = client.messages.create(
  body="Hello from Twilio",
  from_="+13613154870",
  to="+821020631392"
)

############################### 네이버 클라우드 api 웹에서 가능 but api 호출시 오류 ###################################

import hmac, hashlib, base64
import time, requests, json

def make_signature(secret_key, access_key, timestamp, uri):
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    message = method + " "  + uri + "\\n" + timestamp + "\\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signingKey

access_key = "03xzavED0IId4gmqeMju"
secret_key = "KJhb3vcSnS7vlKrf5qERDHn3SPfANk6kpfoQcwMQ"
service_key = "ncp:sms:kr:309790154571:ktaivlep"

# <https://api.ncloud-docs.com/docs/ko/ai-application-service-sens-smsv2>
url = "https://sens.apigw.ntruss.com"
uri = f"/sms/v2/services/{service_key}/messages"

timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

# 받는 상대방
number = "01012347895"

# message 내용
contents = "문자 테스트"

header = {
    "Content-Type": "application/json; charset=utf-8",
    "x-ncp-apigw-timestamp": timestamp,
    "x-ncp-iam-access-key": access_key,
    "x-ncp-apigw-signature-v2": make_signature(secret_key, access_key, timestamp, uri)
}

# from : SMS 인증한 사용자만 가능
data = {
    "type":"SMS",
    "from":"01012349546",
    "content":contents,
    "subject":"SENS",
    "messages":[
        {
            "to":number,
        }
    ]
}

res = requests.post(url+uri,headers=header,data=json.dumps(data))
datas = json.loads(res.text)
print(datas)
reid = datas['requestId']

print("메시지 전송 상태")
print(res.text+"\\n")
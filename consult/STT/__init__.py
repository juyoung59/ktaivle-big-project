# Imports the Google Cloud client library
from google.cloud import speech

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

audio = speech.RecognitionAudio(uri=gcs_uri)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
)

# Detects speech in the audio file
response = client.recognize(config=config, audio=audio)

for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))

# 아래 부분이 어디에 들어가야 할지는 모르겠음.

# 오디오 이쪽에 연결 (오디오 파일 로드)

# import io
# from google.oauth2 import service_account
# from google.cloud import speech

# client_file = 'norse-strata-389807-390985395ee0.json'
# credentials = service_account.Credentials.from_service_account_file(client_file)
# client = speech.SpeechClient(credentials=credentials)

#  gcs_uri = 'gcs:<uri link>'   <-- 구글 저장소 UI로 가는 것
# audio_file = 'audio sample'
# with io.open(audio_file, 'rb') as f:
#     content = f.read()
#     audio = speech.RecognitionAudio(content=content)  저장소 사용할 경우 괄호안을 uri = gcs_uri 입력하면 됨.
# 저장소 사용할 경우 operation = client.long_running_recognize(config = config, audio = audio) 넣으면 됨.

# config = speech.RecognitionConfig(
#     encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz = 44100, (어떤 파일이냐에 따라 해당 파일에 맞는 헤르츠를 맞춰야 함.)
#     Language_code = 'en-US',
#     model = 'phone_call',
# )

# response = client.recognize(config = config, audio = audio)
# for result in response.results:
#     save(result.alternatives[0].transcript) 가장 높게 나온 결과 저장

# 구글 저장소 이용할 경우 # 1분 이상의 파일일 경우 Google Cloud Storage에 업로드 해야 함.

# from google.oauth2 import service_account
# from google.cloud import speech

# client_file = 'norse-strata-389807-390985395ee0.json'
# credentials = service_account.Credentials.from_service_account_file(client_file)
# client = speech.SpeechClient(credentials=credentials)

# gcs_uri = 'gcs:<uri link>'
# config = speech.RecognitionConfig(
#     encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz = 44100, (어떤 파일이냐에 따라 해당 파일에 맞는 헤르츠를 맞춰야 함.)
#     Language_code = 'en-US',
#     model = 'phone_call',
# )
# audio = speech.RecognitionAudio(uri = gcs_uri)
# operation = client.long_running_recognize(config = config, audio = audio)

# print("Waiting for operation to complete...")
# response = operation.result(timeout = 90)
# for result in response.results:
#     save(result.alternatives[0].transcript) 가장 높게 나온 결과 저장
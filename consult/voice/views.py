from django.shortcuts import render,redirect,HttpResponse
from accounts.models import User
from django.utils import timezone
from .models import Voice
# from . import slang_mic

# from __future__ import division

import re
import sys
# from google.cloud import speech
import pyaudio
from six.moves import queue

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


def test(request):
    username = None
    counselor_list = User.objects.filter(member_type='Counselor')
    if request.user.is_authenticated:  # 사용자가 인증된 경우에만 사용자 이름 가져오기
        username = request.user.username
    #     counselor_list = User.objects.all()
    
    context = {
        'username': username,
        'counselor_list': counselor_list
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        counselor_username = request.POST.get('counselor')
        
        if action == 'start':
            # 전화 시작 시간을 저장
            request.session['start_time'] = timezone.now()
            main()
        elif action == 'stop':
            # 전화 종료 시간을 저장
            start_time = request.session.pop('start_time', None)
            
            if start_time:
                end_time = timezone.now()
                duration = (end_time - start_time).total_seconds() / 60
                
                # 시작 시간과 종료 시간을 DB에 저장
                call = Voice(caller=username, receiver=counselor_username, start_time=start_time, end_time=end_time, duration=duration)
                call.save()
    
    return render(request, 'voice.html', context)

class MicrophoneStream(object):

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,

            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,

            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True

        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:

            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

def listen_print_loop(responses):
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)

            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            num_chars_printed = 0

def main():
    # http://g.co/cloud/speech/docs/languages
    language_code = "zh(cmn-Hans-CN)"  # 위에 링크 가서 언어 코드 확인해보고 테스트 해보세영

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        profanity_filter = True
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        listen_print_loop(responses)

if __name__ == "__main__":
    main()



def test1(request):
    username = None
    counselor_list = User.objects.filter(member_type='Counselor')
    if request.user.is_authenticated:  # 사용자가 인증된 경우에만 사용자 이름 가져오기
        username = request.user.username
    #     counselor_list = User.objects.all()
    
    context = {
        'username': username,
        'counselor_list': counselor_list
    }
    return render(request, 'voice_test.html', context)

def counselor(request):
    username = None
    counselor_list = User.objects.filter(member_type='Counselor')
    if request.user.is_authenticated:  # 사용자가 인증된 경우에만 사용자 이름 가져오기
        username = request.user.username
    #     counselor_list = User.objects.all()
    
    context = {
        'username': username,
        'counselor_list': counselor_list
    }
    return render(request, 'voice_counselor.html', context)

def client(request):
    username = None
    counselor_list = User.objects.filter(member_type='Counselor')
    if request.user.is_authenticated:  # 사용자가 인증된 경우에만 사용자 이름 가져오기
        username = request.user.username
    #     counselor_list = User.objects.all()
    
    context = {
        'username': username,
        'counselor_list': counselor_list
    }
    return render(request, 'voice_client.html', context)

def voice_en(request):
    return render(request, 'voice_en.html')

def voice_ja(request):
    return render(request, 'voice_ja.html')

def voice_ch(request):
    return render(request, 'voice_ch.html')

def voice_vi(request):
    return render(request, 'voice_vi.html')

def voice_th(request):
    return render(request, 'voice_th.html')

def account(request):
    return render(request, 'account.html')

def summary(request):
    return render(request, 'summary.html')

def history(request):
    return render(request, 'history.html')


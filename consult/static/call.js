'use strict';

const baseURL = "/"

// Google Cloud STT 설정
const speech = require('@google-cloud/speech');
const client = new speech.SpeechClient({
    keyFilename: '/path/to/service-account-key.json' // 서비스 계정 키 파일 경로
});
const encoding = 'LINEAR16';
const sampleRateHertz = 16000;
const languageCode = 'en-US';  // 추후 드롭다운 옵션 선택된걸로 자동으로 연결되도록 함수화 할 예정.

// STT 관련 변수
let recognizeStream = null;
let audioInterval = null;

// HTML 출력을 위한 요소
let transcriptionElement = document.getElementById("transcription");

let localAudio = document.querySelector('#localAudio');
let remoteAudio = document.querySelector('#remoteAudio');

let otherUser;
let remoteRTCMessage;

let iceCandidatesFromCaller = [];
let peerConnection;
let remoteStream;
let localStream;

let callInProgress = false;

//event from html
function call() {
    let userToCall = document.getElementById("callName").value;
    otherUser = userToCall;

    beReady()
        .then(bool => {
            processCall(userToCall)
        })
}

//event from html
function answer() {
    //do the event firing

    beReady()
        .then(bool => {
            processAccept();
        })

    document.getElementById("answer").style.display = "none";
}

let pcConfig = {
    "iceServers":
        [
            { "url": "stun:stun.jap.bloggernepal.com:5349" },
            {
                "url": "turn:turn.jap.bloggernepal.com:5349",
                "username": "guest",
                "credential": "somepassword"
            },
            {"url": "stun:stun.l.google.com:19302"}
        ]
};

// Set up audio and video regardless of what devices are present.
let sdpConstraints = {
    offerToReceiveAudio: true,
    // offerToReceiveVideo: true
};

/////////////////////////////////////////////

let socket;
let callSocket;
function connectSocket() {
    let ws_scheme = window.location.protocol == "https:" ? "wss://" : "ws://";
    console.log(ws_scheme);

    callSocket = new WebSocket(
        ws_scheme
        + window.location.host
        + '/ws/call/'
    );

    callSocket.onopen = event =>{
    //let's send myName to the socket
        callSocket.send(JSON.stringify({
            type: 'login',
            data: {
                name: myName
            }
        }));
    }

    callSocket.onmessage = (e) =>{
        let response = JSON.parse(e.data);

        // console.log(response);

        let type = response.type;

        if(type == 'connection') {
            console.log(response.data.message)
        }

        if(type == 'call_received') {
            // console.log(response);
            onNewCall(response.data)
        }

        if(type == 'call_answered') {
            onCallAnswered(response.data);
        }

        if(type == 'ICEcandidate') {
            onICECandidate(response.data);
        }
    }

    const onNewCall = (data) =>{
        //when other called you
        //show answer button

        otherUser = data.caller;
        remoteRTCMessage = data.rtcMessage

        // document.getElementById("profileImageA").src = baseURL + callerProfile.image;
        document.getElementById("callerName").innerHTML = otherUser;
        document.getElementById("call").style.display = "none";
        document.getElementById("answer").style.display = "block";
    }

    const onCallAnswered = (data) =>{
        //when other accept our call
        remoteRTCMessage = data.rtcMessage
        peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));

        document.getElementById("calling").style.display = "none";

        console.log("Call Started. They Answered");
        // console.log(pc);

        callProgress()
    }

    const onICECandidate = (data) =>{
        // console.log(data);
        console.log("GOT ICE candidate");

        let message = data.rtcMessage

        let candidate = new RTCIceCandidate({
            sdpMLineIndex: message.label,
            candidate: message.candidate
        });

        if (peerConnection) {
            console.log("ICE candidate Added");
            peerConnection.addIceCandidate(candidate);
        } else {
            console.log("ICE candidate Pushed");
            iceCandidatesFromCaller.push(candidate);
        }

    }

}

/**
 * 
 * @param {Object} data 
 * @param {number} data.name - the name of the user to call
 * @param {Object} data.rtcMessage - the rtc create offer object
 */
function sendCall(data) {
    //to send a call
    console.log("Send Call");

    // socket.emit("call", data);
    callSocket.send(JSON.stringify({
        type: 'call',
        data
    }));

    document.getElementById("call").style.display = "none";
    // document.getElementById("profileImageCA").src = baseURL + otherUserProfile.image;
    document.getElementById("otherUserNameCA").innerHTML = otherUser;
    document.getElementById("calling").style.display = "block";
}



/**
 * 
 * @param {Object} data 
 * @param {number} data.caller - the caller name
 * @param {Object} data.rtcMessage - answer rtc sessionDescription object
 */
function answerCall(data) {
    //to answer a call
    // socket.emit("answerCall", data);
    callSocket.send(JSON.stringify({
        type: 'answer_call',
        data
    }));
    callProgress();
}

/**
 * 
 * @param {Object} data 
 * @param {number} data.user - the other user //either callee or caller 
 * @param {Object} data.rtcMessage - iceCandidate data 
 */
function sendICEcandidate(data) {
    //send only if we have caller, else no need to
    console.log("Send ICE candidate");
    // socket.emit("ICEcandidate", data)
    callSocket.send(JSON.stringify({
        type: 'ICEcandidate',
        data
    }));

}

function beReady() {
    return navigator.mediaDevices.getUserMedia({
        audio: true,
        // video: true
    })
        .then(stream => {
            localStream = stream;
            localAudio.srcObject = stream;

            return createConnectionAndAddStream()
        })
        .catch(function (e) {
            alert('getUserMedia() error: ' + e.name);
        });
}

function createConnectionAndAddStream() {
    createPeerConnection();
    peerConnection.addStream(localStream);
    return true;
}

function processCall(userName) {
    peerConnection.createOffer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);
        sendCall({
            name: userName,
            rtcMessage: sessionDescription
        })
    }, (error) => {
        console.log("Error");
    });
}

function processAccept() {

    peerConnection.setRemoteDescription(new RTCSessionDescription(remoteRTCMessage));
    peerConnection.createAnswer((sessionDescription) => {
        peerConnection.setLocalDescription(sessionDescription);

        if (iceCandidatesFromCaller.length > 0) {
            //I am having issues with call not being processed in real world (internet, not local)
            //so I will push iceCandidates I received after the call arrived, push it and, once we accept
            //add it as ice candidate
            //if the offer rtc message contains all thes ICE candidates we can ingore this.
            for (let i = 0; i < iceCandidatesFromCaller.length; i++) {
                //
                let candidate = iceCandidatesFromCaller[i];
                console.log("ICE candidate Added From queue");
                try {
                    peerConnection.addIceCandidate(candidate).then(done => {
                        console.log(done);
                    }).catch(error => {
                        console.log(error);
                    })
                } catch (error) {
                    console.log(error);
                }
            }
            iceCandidatesFromCaller = [];
            console.log("ICE candidate queue cleared");
        } else {
            console.log("NO Ice candidate in queue");
        }

        answerCall({
            caller: otherUser,
            rtcMessage: sessionDescription
        })

    }, (error) => {
        console.log("Error");
    })
}

/////////////////////////////////////////////////////////

function createPeerConnection() {
    try {
        peerConnection = new RTCPeerConnection(pcConfig);
        // peerConnection = new RTCPeerConnection();
        peerConnection.onicecandidate = handleIceCandidate;
        peerConnection.onaddstream = handleRemoteStreamAdded;
        peerConnection.onremovestream = handleRemoteStreamRemoved;
        console.log('Created RTCPeerConnnection');
        return;
    } catch (e) {
        console.log('Failed to create PeerConnection, exception: ' + e.message);
        alert('Cannot create RTCPeerConnection object.');
        return;
    }
}

function handleIceCandidate(event) {
    // console.log('icecandidate event: ', event);
    if (event.candidate) {
        console.log("Local ICE candidate");
        // console.log(event.candidate.candidate);

        sendICEcandidate({
            user: otherUser,
            rtcMessage: {
                label: event.candidate.sdpMLineIndex,
                id: event.candidate.sdpMid,
                candidate: event.candidate.candidate
            }
        })

    } else {
        console.log('End of candidates.');
    }
}

function handleRemoteStreamAdded(event) {
    console.log('Remote stream added.');
    remoteStream = event.stream;
    // 원격 오디오 요소에 연결
  const remoteAudio = document.getElementById('remoteAudio');
  remoteAudio.srcObject = remoteStream;

  // 원격 스트림에서 오디오 트랙 가져오기
  const audioTrack = remoteStream.getAudioTracks()[0];

  // STT 작업 시작
  startSpeechToText(audioTrack);
}

// 팝업창 관리를 위한 변수
let popupContainer = null;

// 팝업창 생성 함수
function createPopupContainer() {
  // 이미 생성된 팝업창이 있다면 제거
  if (popupContainer) {
    document.body.removeChild(popupContainer);
  }

  // 팝업창 컨테이너 생성
  popupContainer = document.createElement("div");
  popupContainer.classList.add("popup-container");
  document.body.appendChild(popupContainer);
}

// 팝업창에 텍스트 출력 함수
function appendTranscriptionToPopup(text) {
  const p = document.createElement('p');
  p.innerText = text;
  popupContainer.appendChild(p);
}

// 번역된 텍스트를 받아서 처리하는 함수
function processTranslatedText(text, isSelf) {
  // 팝업창에 번역된 텍스트 추가
  appendTranscriptionToPopup(text);

  // 여기서 chat GPT API로 입력을 전달하고 처리하는 로직을 추가하면 됩니다.
  // 예시로는 콘솔에 번역된 텍스트와 대상을 출력하는 것으로 대체합니다.
  const target = isSelf ? "본인" : "상대방";
  console.log(`${target}이(가) 말한 내용:`, text);
}

// 번역 함수
async function translateTextAndProcess(sourceText, sourceLanguage, targetLanguage, isSelf) {
  // 번역 API를 사용하여 텍스트를 번역
  const translatedText = await translateText(sourceText, sourceLanguage, targetLanguage);

  // 번역된 텍스트를 처리
  processTranslatedText(translatedText, isSelf);
}

// 전화를 건 사람의 언어 감지 함수
function detectLanguageAndTranslate(sourceText, isSelf) {
  const sourceLanguage = detectLanguage(sourceText);
  const targetLanguage = isSelf ? '본인의 언어 코드' : '상대방의 언어 코드';

  if (isSelf) {
    // 본인이 말한 경우 번역할 필요 없이 그대로 출력
    appendTranscriptionToPopup(sourceText);
  } else {
    // 상대방이 말한 경우 번역 수행
    translateTextAndProcess(sourceText, sourceLanguage, targetLanguage, isSelf);
  }
}

// Google Cloud STT 시작
function startSpeechToText(audioTrack) {
  // STT 작업을 위해 오디오 트랙을 스트림으로 변환
  const audioStream = new MediaStream();
  audioStream.addTrack(audioTrack);

  // STT 리스너 생성
  recognizeStream = client
    .streamingRecognize({
      config: {
        encoding: encoding,
        sampleRateHertz: sampleRateHertz,
        languageCode: languageCode,
      },
      interimResults: true,
    })
    .on('error', console.error)
    .on('data', (data) => {
      if (data.results[0] && data.results[0].alternatives[0]) {
        const transcript = data.results[0].alternatives[0].transcript;
        // 텍스트를 팝업창에 출력
        detectLanguageAndTranslate(transcript, isSelf);
      }
    });

  // STT 작업을 위한 오디오 스트림 전달
  const audioOptions = {
    mimeType: 'audio/webm',
    audioBitsPerSecond: 16000,
  };
  const mediaRecorder = new MediaRecorder(audioStream, audioOptions);
  mediaRecorder.ondataavailable = (event) => {
    if (event.data.size > 0) {
      recognizeStream.write(event.data);
    }
  };
  mediaRecorder.start();

  // 오디오 스트림 전송 간격 설정
  audioInterval = setInterval(() => {
    mediaRecorder.stop();
    mediaRecorder.start();
  }, 3000); // 3초마다 오디오 스트림 전송 (조정 가능)

  // 변환된 텍스트를 HTML 요소에 추가하는 함수
function appendTranscription(transcription) {
    const p = document.createElement('p');
    p.innerHTML = transcription;
    transcriptionElement.appendChild(p);
  }

  // STT 작업 중지 함수 호출 설정
  stopRecognizeOnCallEnd();
}

// STT 작업 중지
function stopSpeechToText() {
  if (recognizeStream) {
    recognizeStream.destroy();
    recognizeStream = null;
  }
  if (audioInterval) {
    clearInterval(audioInterval);
    audioInterval = null;
  }
// 팝업창 닫기
    closePopupContainer();

// DB에 저장
    saveAllTranscriptionsToDB();
}

// 팝업창 닫기 함수
function closePopupContainer() {
    if (popupContainer) {
    document.body.removeChild(popupContainer);
    popupContainer = null;
    }
}

// 통화 종료 시 STT 작업 중지
function stopRecognizeOnCallEnd() {
  // stop() 함수가 호출될 때 STT 작업 중지
  const stopButton = document.getElementById('stopButton');
  stopButton.addEventListener('click', () => {
    stopSpeechToText();
    saveAllTranscriptionsToDB(); // 텍스트화된 내용을 DB에 저장하는 함수 호출
  });
}

// 모든 텍스트화된 내용을 DB에 저장 1
// function saveAllTranscriptionsToDB() {
//   const transcriptions = document.getElementById('transcription').innerText;
//   const query = 'INSERT INTO transcriptions (transcription) VALUES (?)';

//   // 텍스트를 줄 단위로 분리하여 배열로 변환
//   const transcriptionArray = transcriptions.split('\n');

//   // DB에 각 텍스트를 저장
//   transcriptionArray.forEach((transcript) => {
//     connection.query(query, [transcript], (error, results) => {
//       if (error) {
//         console.error('Error saving transcription to DB:', error);
//       } else {
//         console.log('Transcription saved to DB');
//       }
//     });
//   });
// }

// 모든 텍스트화된 내용을 DB에 저장
function saveAllTranscriptionsToDB() {
    const transcriptions = Array.from(popupContainer.querySelectorAll('p'))
      .map((p) => p.innerText)
      .join('\n');
  
    const query = 'INSERT INTO transcriptions (transcription) VALUES (?)';
  
    // DB에 텍스트 저장
    connection.query(query, [transcriptions], (error, results) => {
      if (error) {
        console.error('Error saving transcription to DB:', error);
      } else {
        console.log('Transcription saved to DB');
      }
    });
  }

function handleRemoteStreamRemoved(event) {
    console.log('Remote stream removed. Event: ', event);
    remoteAudio.srcObject = null;
    localAudio.srcObject = null;
}

window.onbeforeunload = function () {
    if (callInProgress) {
        stop();
    }
};


function stop() {
    localStream.getTracks().forEach(track => track.stop());
    callInProgress = false;
    peerConnection.close();
    peerConnection = null;
    document.getElementById("call").style.display = "block";
    document.getElementById("answer").style.display = "none";
    document.getElementById("inCall").style.display = "none";
    document.getElementById("calling").style.display = "none";
    document.getElementById("endAudioButton").style.display = "none"
    otherUser = null;
    window.location.href = '/survey/';
}

function callProgress() {

    document.getElementById("audios").style.display = "block";
    document.getElementById("otherUserNameC").innerHTML = otherUser;
    document.getElementById("inCall").style.display = "block";

    callInProgress = true;
}


var startTime = new Date();

function updateCallDuration() {
    var currentTime = new Date();
    var timeDifference = currentTime - startTime;
    var seconds = Math.floor(timeDifference / 1000);
    var minutes = Math.floor(seconds / 60);
    var hours = Math.floor(minutes / 60);
    seconds %= 60;
    minutes %= 60;

    var durationString = hours.toString().padStart(2, '0') + ':' +
                         minutes.toString().padStart(2, '0') + ':' +
                         seconds.toString().padStart(2, '0');

    document.getElementById("callDuration").textContent = "Call Duration: " + durationString;
}

setInterval(updateCallDuration, 1000);
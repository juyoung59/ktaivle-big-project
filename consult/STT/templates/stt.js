// WebSocket 연결
var socket = new WebSocket('ws://서버주소');

// WebSocket 연결 성공 시 실행되는 이벤트 핸들러
socket.onopen = function(event) {
  console.log('WebSocket 연결 성공');
};

// WebSocket 메시지 수신 시 실행되는 이벤트 핸들러
socket.onmessage = function(event) {
  var response = JSON.parse(event.data); // 응답 데이터 파싱
  handleSTTResponse(response); // STT 응답 처리
};

// WebSocket 연결 종료 시 실행되는 이벤트 핸들러
socket.onclose = function(event) {
  console.log('WebSocket 연결 종료');
};

// 스트리밍 STT API의 응답을 처리하는 함수
function handleSTTResponse(response) {
  // 응답 데이터를 사용하여 원하는 작업 수행
  // 예를 들어, 변환된 텍스트를 출력하거나 다른 로직을 수행할 수 있습니다.
  console.log('STT 응답:', response);
}

// sendStreamData() 함수에서 WebSocket으로 데이터 전송
function sendStreamData(data) {
  if (socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ audioData: data }));
  }
}

function beReady() {
  return navigator.mediaDevices.getUserMedia({
    audio: true,
    // video: true
  })
    .then(stream => {
      localStream = stream;
      localAudio.srcObject = stream;

      // getUserMedia()를 통해 오디오 스트림을 가져온 후, 스트리밍 STT API로 전송
      var audioContext = new AudioContext();
      var mediaStreamSource = audioContext.createMediaStreamSource(stream);
      var mediaStreamDestination = audioContext.createMediaStreamDestination();
      mediaStreamSource.connect(mediaStreamDestination);

      var recorder = new MediaRecorder(mediaStreamDestination.stream);
      recorder.addEventListener('dataavailable', function(event) {
        sendStreamData(event.data);
      });
      recorder.start();

      // 스트리밍 STT API로부터 응답을 받아 처리
      socket.onmessage = function(event) {
        var response = JSON.parse(event.data); // 응답 데이터 파싱
        handleSTTResponse(response); // STT 응답 처리
      };

      return createConnectionAndAddStream();
    })
    .catch(function (e) {
      alert('getUserMedia() error: ' + e.name);
    });
}
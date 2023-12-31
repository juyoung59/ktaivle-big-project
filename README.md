# 외국인을 위한 번역 AI 상담 서비스(+폭언 탐지)
## **🗓 개발 기간**

2023.05.30 ~ 2023.07.10

## **🤝 팀 구성**

강성필, 김주열, 이유진, 이주영, 이지현, 이채원, 채종현

## **⚙ 사용 방법**
- 가상환경 생성
```bash
conda create -n (가상환경 이름) python=3.10 -y
conda activate (가상환경 이름)
```   
- 라이브러리 설치
```bash
pip install -r requirements.txt
```   
- 프로젝트 시작
```bash
python manage.py runserver
```

## **🛠 주요 서비스**
- **음성 자동 번역**<br>
: 외국인 고객의 문의 내용을 실시간으로 번역해서 상담사에게 제공 한 뒤 상담사 답변 내용을 번역한 뒤 고객에게 제공
- **폭언 탐지**<br>
: 전화 상담 도중 폭언 시 경고 후 반복시 전화 상담 종료하고 문자 상담 혹은 챗봇 상담 전환 
- **상담 내용 요약**<br>
: 상담 내용 요약 후 고객에게 제공

## **🗃 선정 배경**
- 행정안전부 통계에 따르면 폭언·폭행·성희롱 등 민원인의 위법행위는 2019년 3만 8054건, 2020년 4만 6079건, 2021년 5만 1883건으로 매년 크게 늘고 있음(경기신문 (https://www.kgnews.co.kr))
- 콜센터 상담사 감정 노동 및 스트레스

<br>

- 외국인이 콜센터 사용 시 예약 필요
- 법무부 '출입국·외국인정책본부' 통계에 따르면 코로나 방역 완화로 2022년 1월 9만여명에서 2023년 1월 46만여명으로 외국인 입국 증가함

## **📈 기대 효과**
- 상담 연결율 향상 → 고객 만족도 향상 및 고객 유치
- 실시간 다국어 서비스를 통해 외국인 고객 만족도 향상 및 고객 유치
- 상담원 업무 부담 감소 및 만족도 향상 → 상담원 퇴직률 감소
- 중견 기업에 구독형 AICC 제공 가능 → 기업 매출액 증가
- 인건비 절감

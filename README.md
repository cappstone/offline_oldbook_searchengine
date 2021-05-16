# offline_oldbook_searchengine
yes24, 알라딘 오프라인 중고 서점 크롤링 검색엔진

## 세팅방법
### 원스크립트 세팅
1. 터미널에 ./env_setting.sh
### 수동세팅
1. 리눅스 또는 macOS에 npm, python 설치하기
2. frontend 디렉토리로 가서 npm install
3. pip install -r requirements.txt
4. npm run serve 하여 vue-cli실행
5. python api_server.py
### 주의사항
* 위의 세팅방법은 linux계열 및 macOS에서만 가능함
* api_server.py 들어가서 포트세팅 할 것 (기본: 7000)

## 실행방법
1. 터미널에 ./server_start.sh
### 주의사항
* 이 실행방법은 vue-cli의 포트를 오픈하여 실행하는 방식임
* flask api 서버도 백그라운드에서 실행됨

## webpack 배포방법
1. npm run build
2. /dist 에 있는 webpack을 nginX로 연동할것

## 주소조합
http://{서버주소}:{포트}/search?word={검색어}&mode={검색모드}
### 예시
http://sc0nep.iptime.org:7000/search?word=스즈미야하루히의우울&mode=0
### 검색모드
0: 알라딘
1: yes24

from typing import Dict
from flask_restful import Resource, reqparse, Api
from flask import Flask, make_response
from flask_cors import CORS
from module.aladinV2 import Aladin
from module.yes24V2 import Yes24
# import module.aladin as Aladin
# import module.yes24 as Yes24

import json
import redis
import datetime


# redis 연결
rd = redis.StrictRedis(host='localhost', port=6379, charset="utf-8", decode_responses=True)

# 크롤링 요청하는 함수
def crawl_data(word: str, mode: int):
    if mode == 0:
        crawl_type = "aladin"
        aladin = Aladin(word)
        result = aladin.result()

    elif mode == 1:
        crawl_type = "yes24"
        yes24 = Yes24(word)
        result = yes24.result()

    # redis에 저장 (예시: "yes24 - 파이썬" : 데이터)
    jsonDataDict = json.dumps(result, ensure_ascii=False)
    rd.set(f"{crawl_type}_{word}", jsonDataDict)

    return result


class Search(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('word', required=True,
                                type=str, help='Please enter word')
            parser.add_argument('mode', required=True,
                                type=int, help='Please enter mode')
            args = parser.parse_args()

            # redis에 값이 있는지 없는지 확인
            rd_aladin = rd.get(f"aladin_{args['word']}")
            rd_yes24 = rd.get(f"yes24_{args['word']}")

            # 현재 시간 구하기
            now = datetime.datetime.now()

            result = ""
            
            # 알라딘 모드로 검색했을 경우
            if args['mode'] == 0:
                # 캐싱된 데이터가 있는 경우
                if rd_aladin is not None:
                    cached_data: Dict = dict(json.loads(rd_aladin))

                    # 크롤링 한 시간 확인하기
                    crawl_time: str = datetime.datetime.strptime(cached_data['crawledDate'], "%Y%m%d %H%M%S")
                    time_diff = now - crawl_time
                    
                    # 지금시간과 크롤링한 데이터 차이가 1시간 이상 차이나는 경우 새로 크롤링
                    if (time_diff.seconds / 3600) > 1:
                        result = crawl_data(args['word'], args['mode'])
                    else:
                        result = cached_data
                # 캐싱된 데이터가 없는 경우 -> 새로 크롤링
                else:
                    result = crawl_data(args['word'], args['mode'])

            # yes24 모드로 검색했을 경우
            elif args['mode'] == 1:
                # 캐싱된 데이터가 있는 경우
                if rd_yes24 is not None:
                    cached_data: Dict = dict(json.loads(rd_yes24))

                    # 크롤링 한 시간 확인하기
                    crawl_time: str = datetime.datetime.strptime(cached_data['crawledDate'], "%Y%m%d %H%M%S")
                    time_diff = now - crawl_time
                    
                    # 지금시간과 크롤링한 데이터 차이가 3시간 이상 차이나는 경우 새로 크롤링
                    if (time_diff.seconds / 3600) > 3:
                        result = crawl_data(args['word'], args['mode'])
                    else:
                        result = cached_data
                # 캐싱된 데이터가 없는 경우 -> 새로 크롤링
                else:
                    result = crawl_data(args['word'], args['mode'])

            resp = make_response(json.dumps(result, ensure_ascii=False))
            return resp
        except Exception as e:
            return {'error': str(e)}


app = Flask('api_offbookstore')
CORS(app)
app.config['JSON_AS_ASCII'] = False
api = Api(app)
api.add_resource(Search, '/search')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)

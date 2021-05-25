from flask_restful import Resource, reqparse, Api
from flask import Flask, make_response
from flask_cors import CORS
from module.aladinV2 import Aladin
from module.yes24V2 import Yes24
# import module.aladin as Aladin
# import module.yes24 as Yes24

import json
import redis


# redis 연결
rd = redis.StrictRedis(host='localhost', port=6379, db=0)


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
            rd_aladin = rd.get(f"aladin - {args['word']}")
            rd_yes24 = rd.get(f"yes24 - {args['word']}")

            result = ""
            crawl_type = ""
            if args['mode'] == 0:
                if rd_aladin is True:
                    result = rd_aladin
                else:
                # redis에 없는 경우(크롤링 프로세스 진행)
                    crawl_type = "aladin"
                    aladin = Aladin(args['word'])
                    # redis에 저장 (예시: "yes24 - 파이썬" : 데이터)
                    rd.set(f"{crawl_type} - {args['word']}", result)
                    result = aladin.result()
            elif args['mode'] == 1:
                if rd_yes24 is True:
                    result = rd_yes24
                else:
                # redis에 없는 경우(크롤링 프로세스 진행)
                    crawl_type = "yes24"
                    yes24 = Yes24(args['word'])
                    # redis에 저장 (예시: "yes24 - 파이썬" : 데이터)
                    rd.set(f"{crawl_type} - {args['word']}", result)
                    result = yes24.result()

            """
            elif args['mode'] == "common":
            """
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

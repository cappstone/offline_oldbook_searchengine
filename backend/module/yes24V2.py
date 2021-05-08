'''
YES24 OfflineShop Parse Module by Sc0_Nep
'''
from typing import Dict, List
from bs4 import BeautifulSoup
import bs4.element
import requests
import asyncio
import json
import time

# yes24 중고몰 관련된 URL
MAIN_URL = "http://www.yes24.com/Mall/UsedStore/Main" # 중고몰 메인페이지 URL
COMMON_URL = "http://www.yes24.com/Mall/UsedStore/Search?STORE_CODE=" # 중고몰 공통 URL

# 중고서점 고유코드 dict형태의 변수
malls: Dict = {}  # 중고서점 지점 : 중고서점 고유코드

# 중고몰 고유코드 미리 가져오는 작업
html: str = requests.get(MAIN_URL).text
soup = BeautifulSoup(html, "lxml")
get_malls: List = soup.find("ul", id="ulStoreSerchCategory").find_all("li")
for i in get_malls:
    malls.setdefault(i.text.strip(), i.find("a").attrs["value"])

# dict형태의 검색결과 저장하는 함수
search_result: Dict = {}

# 검색결과 가져오는 클래스
class SearchResult:
    def __init__(self, keyword) -> None:
        # mall정보 가져오기
        mall_names: List[str] = list(malls.keys()) # 중고몰 이름
        mall_codes: List[str] = list(malls.values()) # 중고몰 코드

        # 키워드값 받는 변수
        # yes24는 ascii형태로 인코딩된 값을 파라미터에 넣는 형식임
        self.keyword = str(keyword.encode('ascii', 'backslashreplace')).upper(
        ).replace('\\\\U', '%u')[2:][:-1]

        # url조합
        url_list: List = (COMMON_URL + url + "&searchText=" + self.keyword for url in mall_codes)

        # 검색된 북 타이틀들 기록하는 리스트
        self.books: List = []

        for i, url in enumerate(url_list):
            self.__scrap_process(url, mall_names[i])

        print(self.books)


    def __scrap_process(self, url, mall_name) -> Dict:
        source: str = requests.get(url).text
        soup = BeautifulSoup(source, "lxml")
        tag_ul = soup.find("ul", id="ulResult")
        result = []

        # 검색 결과 없는 경우도 있으니 확인
        if str(tag_ul) == "None":
            result.append("검색 결과 없음")
        else:
            tag_li: List = tag_ul.find_all("li")
            for j in tag_li:
                # 책 제목 가져오는 부분
                title: str = j.find("strong", class_="name").text.strip()

                # 책이 books에 있는지 없는지 중복확인하고 저장
                if title not in self.books:
                    self.books.append(title)
                else:
                    pass

                # 설명부분 text들 싹다 가져와서 합쳐버리기 - description 크롤링
                tag_p: str = j.find("p", class_="storeG_pubGrp")
                tag_span: List = tag_p.find_all("span")
                description: str = "| "
                for k in tag_span:
                    description += k.text + " | "

                # YES24는 매물에 가격또는 도서 위치가 없는 경우가 있음;;
                price: str = ""
                location: str = ""
                try:
                    # 가격 부분 가져오기
                    price = j.find(
                        "p", class_="storeG_price").text[2:].strip() # 가격 가져오기
                    location = j.find("dd").text.strip()  # 책 위치 가져오기
                except AttributeError:
                    price = "가격정보 없음"
                    location = "위치정보 없음"

                # 이제 이것들을 json으로 저장시켜버리자
                item = {'bookname': title, 'description': description,
                        'price': price, 'location': location}
                result.append(item)
        return {'mall': mall_name, 'result': result}



# 아이템별로 검색결과 가져오는 클래스

# test
if __name__ == "__main__":
    a = SearchResult("파이썬")
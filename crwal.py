import codecs

import re

import collections
import requests

from bs4 import BeautifulSoup


# 에러 리스트 생성 함수
def insert_error(blog_id, error, error_doc):
    for i in error_doc:
        error_log = str(error_doc["page"]) + "page / " + str(error_doc["post_number"]) \
                    + "th post / " + error + " / http://blog.naver.com/PostList.nhn?blogId=" + blog_id + "&currentPage=" + str(error_doc["page"])
    error_list.append(error_log)

total_num = 0;

error_list = []

# print("블로그 ID->")
# blog_id = input()


print("\n탐색 시작 페이지 수->")
start_p = int(input())

print("\n탐색 종료 페이지 수->")
end_p = int(input())

print("\nCreating File Naver_Blog_Crawling_Result.txt...\n")

# 파일 열기
# file = codecs.open("Naver_Blog_Crawling_Result.txt", 'w', encoding="utf-8")

# 페이지 단위
for page in range(start_p, end_p + 1):
    # print("=" * 50)
    # file.write("=" * 50 + "\n")
    doc = collections.OrderedDict()

    url = "http://blog.naver.com/PostList.nhn?blogId=hotleve"+ "&currentPage=" + str(page)
    r = requests.get(url)
    
    if (not r.ok):
        print("Page" + page + "연결 실패, Skip")
        continue

    # html 파싱
    soup = BeautifulSoup(r.text.encode("utf-8"), "html.parser")
    postcategory = soup.find("span",{"class":"cate pcol2"})
    if postcategory == None:
      continue
    pc = ""
    if "다쓴글" in postcategory.text:
      pc = "writings"
    else:
      continue
    


    # 페이지 당 포스트 수 (printPost_# 형식의 id를 가진 태그 수)
    # post_count = len(soup.find_all("table", {"id": re.compile("printPost.")}))
    doc["page"] = page
    post = soup.find("table", {"id": "printPost1"})

        # 제목 찾기---------------------------
    if postcategory == None:
      continue

        # 스마트에디터3 타이틀 제거 임시 적용 (클래스가 다름)

    title = post.find("span", {"class": "pcol1 itemSubjectBoldfont"})
    if (title == None):
      title = post.find("span", {"class": "pcol1 itemSubjectBoldfont"})

    if (title != None):
      doc["title"] = title.text.strip()
    else:
      doc["title"] = "TITLE ERROR"

    date = post.find("span", {"class": re.compile("se_publishDate.")})

        # 스마트에디터3 타이틀 제거 임시 적용 (클래스가 다름)
    if (date == None):
      date = post.find("p", {"class": "date fil5 pcol2 _postAddDate"})

    if (date != None):
      doc["date"] = date.text.strip()
    else:
      doc["date"] = "DATE ERROR"
    
    datetime = date.text.replace(" ","0")
    dt = datetime.split(".")
    year = dt[0]
    month = dt[1]
    
    if len(month) == 3 :
      month = month[1:3]
    day = dt[2]
    if len(day) == 3 :
      day = day[1:3]
    tdate  = year +"-"+month+"-"+day
    title= title.text.replace("/", '_').replace("[", '_').replace("]", '_').replace("<", '_').replace(">", '_').replace(" ", '_').replace('"', '_').replace(",", '_').replace("'", '_').replace("*", '_').replace("?", '_')
    file = codecs.open(".\\_posts\\"+tdate+"-"+"writings"+dt[3][4:]+".md", 'w', encoding="utf-8")
    file.write("---"+"\n")
    file.write("layout: post"+"\n")
    file.write("title: "+'"'+title+'"'+"\n")

        # 날짜 찾기---------------------------

    
    file.write("date: " + tdate + " " +dt[3][1:]+":00 +0900"+"\n")
    file.write("comments: true \n")
    file.write("categories: ["+pc+"] \n" )
    file.write("---"+"\n")
    content_up = post.find("div", {"id": "postViewArea"})
    content = content_up.find_all("p")
    diary = ""
    for wrapper in content:
      file.write( wrapper.text + "\n")
    
    img = post.find_all("img")
    print(img)
    for i in img:
      imgUrl = i.get('src')
      if "blogfiles" in imgUrl:
        print(imgUrl)
        imgUrl = imgUrl.replace('w80_blur','w1')
        file.write("![]("+imgUrl+") \n")
    
    file.close()


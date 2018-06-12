from bs4 import BeautifulSoup
from urllib.request import urlopen, HTTPError


try:
    html = urlopen("http://danielmarin.naukas.com/2018/06/02/es-la-tierra-el-mejor-mundo-posible-para-permitir-el-viaje-espacial/")
    bsObj = BeautifulSoup(html.read(), "html.parser")
    
    all_paragraphs = bsObj.find("div", {"class":"entry-content"})
    for paragraph in all_paragraphs:
        print(paragraph)
        print(paragraph.name)
        print("------\n")

except HTTPError as e:
    print(e)
except AttributeError as e:
    print(e)



from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import random
import gzip

HEARDERS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"]
limit = 14125
start = str(4001).zfill(5)  # 开始期数
end = 18126 #结束期数


def getContent(url):
    """
    此函数用于抓取返回403禁止访问的网页
    """
    random_header = random.choice(HEARDERS)

    """ 
    对于Request中的第二个参数headers，它是字典型参数，所以在传入时 
    也可以直接将个字典传入，字典中就是下面元组的键值对应 
    """
    req = Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("Host", "datachart.500.com")

    content = urlopen(req).read()
    html = gzip.decompress(content)
    html = html.decode('gbk')
    return html

def getNum(soup):
    all_subject_tag = soup.find_all('td', attrs={'class': 'cfont2'})

    sub_name_list = [l.string.replace(' ', '') for l in all_subject_tag]  # 所有科目名称

    return sub_name_list

url = "https://datachart.500.com/pls/history/inc/history.php?limit=%s&start=%s&end=%s"%(limit,start,end)
html = getContent(url)
# print(html)
bsoup = BeautifulSoup(html, features='lxml')

all_data = getNum(bsoup)
print(all_data)
fp = open('lottery_data.txt',"w+")
for item in all_data:
    fp.write(item+"\n")
fp.close()
# in_json = json.dumps(all_data, ensure_ascii=False)
# operate_file('data_json.txt', in_json)
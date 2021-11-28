import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
def Disguise():
   header = {
   'User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
   opener = urllib.request.build_opener()
   opener.addheaders = [header]
   urllib.request.install_opener(opener)
def Get_page(url,num):
   try:
      page = urllib.request.urlopen(url).read()
      soup = BeautifulSoup(page, 'lxml')
      print('--------第%d页抓取成功--------'%num)
      return soup
   except urllib.request.URLError as e:
      if hasattr(e,'code'):
         print('错误原因：',e.code)
      if hasattr(e,'reason'):
         print('错误原因：',e.reason)

def Get_House_info(page):
   item = {}
   item['house_type'] = [i.get_text().strip().split('|')[0] for i in page.select('div[class="houseInfo"]')] #户型
   item['house_area'] = [i.get_text().strip().split('|')[1] for i in page.select('div[class="houseInfo"]')] #面积
   item['house_price'] = [i.get_text().strip() for i in page.select('div[class="totalPrice totalPrice2"] span')] #房价
   item['house_unit_price'] = [i.get_text().strip() for i in page.select('div[class="unitPrice"] span')] #单位价格
   item['house_interest'] = [i.get_text().strip().split('/')[0] for i in page.select('div[class="followInfo"]')]  # 关注人数
   return pd.DataFrame(item)
def main():
   filename = '/Users/sunnnjx/Desktop/house_data.csv'
   Disguise()
   house_data = []
   for pg in range(1,101):
      lianjia_url = 'http://gz.lianjia.com/ershoufang/pg' + str(pg) +'/'
      page = Get_page(lianjia_url,pg)
      if len(page) > 0:
         house_info = Get_House_info(page)
         house_data.append(house_info)
         data = pd.concat(house_data, ignore_index = True)
         data.to_csv(filename, encoding = 'gbk', index = False)
         print('------写入完毕------')
if __name__ == '__main__':
   main()
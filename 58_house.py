from bs4 import BeautifulSoup
import requests
import csv
import time
import lxml

def main():

    # 1、筛选条件为租金的范围，可自定义修改
    # 2、地点不同则网址二级域名不同,如此时南京：nj.58.com  北京：bj.58.com
    # 3、因为没有做一些动态切换处理，多次运行可能会触发网址防爬机制，此时需要手动访问该网站进行验证
    # 4、使用此程序需要了解一些爬虫基本原理
    # 5、2023-11-9 最近测试代码发现该网站已经做了防爬虫，频繁访问后需要进行验证
    url = "https://nj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000"

    # 已完成的页数序号，初时为0

    csv_file = open("house.csv", "w", encoding="utf-8")
    csv_writer = csv.writer(csv_file, delimiter=',')

    for page in range(0,20):
        page += 1
        print("正在爬取第" + str(page) + "页信息........")
        print("URL: ", url.format(page=page))
        time.sleep(3)
        response = requests.get(url.format(page=page))
        response.encoding = 'utf-8'
        html = BeautifulSoup(response.text,features="lxml")
        house_list = html.select(".list > li")

        for house in house_list:
            house_title = house.select("img")[0]["alt"]
            house_url = house.select("a")[0]["href"]
            house_info_list1 = house_title.split('-')

            # 如果第二列是公寓名或者社区则取第一列作为地址
            if "公寓" in house_info_list1[0] or "社区" in house_info_list1[0]:
                house_info_list2 = house_info_list1[0].split(' ')
                house_info_list2 = house_info_list2[0].replace('【','')
                house_info_list2 = house_info_list2.replace('】', '｜')
            else:
                house_info_list2 = house_info_list1[0]
            print(house_info_list2 + " " + house_url)

            house_location = house_info_list2.replace('｜',' ')
            house_info_list = house_location.split(' ')
            print(house_info_list)

            house_url = "https://nj.58.com" + house_url
            csv_writer.writerow([house_info_list[1], house_url])
    csv_file.close()

if __name__ == '__main__':
    main()
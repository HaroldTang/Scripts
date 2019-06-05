import requests
import pymysql
from bs4 import BeautifulSoup

ret = requests.get(url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html")
ret.encoding = ret.apparent_encoding

soup = BeautifulSoup(ret.text, 'html.parser')
allProvince = soup.find(name='table', attrs={"class":"provincetable"})
provinceList = allProvince.find_all(name='tr', attrs={"class":"provincetr"})
conn = pymysql.connect('localhost', 'root', 'XXXX', 'data')
cursor = conn.cursor()
for line in provinceList:
    name_list = line.find_all(name='a')
    for provinceName in name_list:
        # print(provinceName.get('href'))
        # try:
        #     sql_province_insert = "insert into province(province_name) values ('%s')" % (provinceName.text)
        #     cursor.execute(sql_province_insert)
        #     conn.commit()
        # except:
        #     conn.rollback()
        #     print("failed!")
        cursor.execute("select province_id from province where province_name = '%s'" % provinceName.text)
        provinceId = cursor.fetchone()

        newRequest = requests.get(url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/" + "%s" % provinceName.get('href'))
        newRequest.encoding = newRequest.apparent_encoding
        soup1 = BeautifulSoup(newRequest.text, 'html.parser')
        city_list = soup1.find_all(name='table', attrs={"class":"citytable"})
        for line2 in city_list:
            city_list_divide = line2.find_all(name='a')
            city_code_list = city_list_divide[::2]
            city_name_list = city_list_divide[1::2]
            for i in range(len(city_name_list)):
                city_name = city_name_list[i]
                city_code = city_code_list[i]
                # print(city_name.text)
                # print(city_code.text)
                # print(provinceId[0])
                # try:
                #     cityCode = city_code.text
                #     cityName = city_name.text
                #     province_id = provinceId[0]
                #     cursor.execute("insert into city(city_code, city_name, province_id) values ('%s','%s',%i)" % (cityCode,cityName,province_id))
                #     conn.commit()
                # except:
                #     conn.rollback()
                #     print("failed!")
                cursor.execute("select city_id from city where city_name = '%s'" % city_name.text)
                cityId = cursor.fetchone()

                countyRequest = requests.get(url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/" + "%s" % city_name.get('href'))

                countyRequest.encoding = countyRequest.apparent_encoding
                countySoup = BeautifulSoup(countyRequest.text, 'html.parser')
                county_list = countySoup.find_all(name ='table', attrs={"class" : "countytable"})
                for countyline in county_list:
                    county_list_divide = countyline.find_all(name='td')
                    county_code_list = county_list_divide[::2]
                    county_name_list = county_list_divide[1::2]

                    county_href = countyline.find_all(name='a')
                    county_href = county_href[::2]
                    for j in range(1,len(county_code_list)):
                        county_html = county_href[j]
                        # try:
                        #     cursor.execute("insert into county(county_code, county_name, city_id) values ('%s', '%s', %i)" % (county_code_list[j].text, county_name_list[j].text, cityId[0]))
                        #     conn.commit()
                        # except:
                        #     conn.rollback()
                        #     print("failed!")
                        print(county_html)
                        townRequest = requests.get(url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/" + "%s/%s" %(county_code_list[j].text[:2], county_html.get('href')))
                        townRequest.encoding = townRequest.apparent_encoding
                        townSoup = BeautifulSoup(townRequest.text, 'html.parser')
                        town_list = townSoup.find_all(name = 'table', attrs = {"class":"towntable"})
                        for townline in town_list:
                            town_list_divide = townline.find_all(name='td')
                            town_code_list = town_list_divide[::2]
                            town_name_list = town_list_divide[1::2]
                            # print(town_name_list)

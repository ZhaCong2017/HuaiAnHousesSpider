import requests
from bs4 import BeautifulSoup
import chardet
import re
import xlwt


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = chardet.detect(r.content)['encoding']
        return r.text
    except:
        return "Wrong"


def getdata(text, sheet):
    soup = BeautifulSoup(text, 'html.parser')
    data = soup.find_all('tr')

    result = []
    building = []
    for i in data:
        now = str(i)
        key = r"<td bgcolor=\"#FFFFFF\" class=\"l1\">(.*?)</td>"
        tmp = re.compile(key).findall(now)
        key = r"<a href=\"/project/ckbno/prjid/.*?target=\"_blank\">(.*?)</a>"
        place = re.compile(key).findall(now)
        result += tmp
        building += place

    sheet.write(1, 0, result[0])
    sheet.write(1, 1, result[1])
    sheet.write(1, 2, result[2])
    sheet.write(1, 3, result[3])

    length = int(len(result) / 4)
    result = result[4:length]
    length = int(len(building) / 4)
    building = building[:length]

    i = 0
    line = 3
    if len(building) * 5 != len(result):
        print('Wrong!!!')
    while i < len(building):
        sheet.write(line, 0, result[i * 5])
        sheet.write(line, 1, building[i])
        sheet.write(line, 2, result[i * 5 + 1])
        sheet.write(line, 3, result[i * 5 + 2])
        sheet.write(line, 4, result[i * 5 + 3])
        sheet.write(line, 5, result[i * 5 + 4])
        i += 1
        line += 1


def sheetinit(sheet):
    sheet.write(0, 0, '入网总套数')
    sheet.write(0, 1, '可签约套数')
    sheet.write(0, 2, '可签约住宅套数')
    sheet.write(0, 3, '可签约非住宅套数')
    sheet.write(2, 0, '用途类别')
    sheet.write(2, 1, '楼盘名称')
    sheet.write(2, 2, '用途')
    sheet.write(2, 3, '总套数')
    sheet.write(2, 4, '自留拆迁套数')
    sheet.write(2, 5, '已签约套数')


if __name__ == "__main__":
    wbk = xlwt.Workbook()
    url = 'http://www.lousw.com'

    nameexist = set()
    name = []
    link = []
    with open('links.txt', 'r', encoding='utf-8') as f:
        while 1:
            line = f.readline()
            if not line:
                break
            tmp = line.split('  ')
            name.append(tmp[0] + ' ')
            link.append(tmp[1][:-1])
    f.close()

    for i in range(len(name)):
        j = 1
        while name[i] in nameexist:
            print(name[i], j)
            name[i] = name[i][:-1] + str(j)
            j += 1
        nameexist.add(name[i])
        sheet = wbk.add_sheet(name[i])
        sheetinit(sheet)

        response = 'Wrong'
        while response == 'Wrong':
            response = getHTMLText(url + link[i])
        getdata(response, sheet)
        print(str(i + 1) + '/' + str(len(name)))

    wbk.save('BuildingInfo.xls')

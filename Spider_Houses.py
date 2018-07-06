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


def getdata(text, sheet, line):
    soup = BeautifulSoup(text, 'html.parser')
    data = soup.findAll('td')
    # return data
    # for i in data:
    #     print(i)
    result = []
    num = []
    corpor = []
    links = []
    for i in range(len(data)):
        now = str(data[i])
        key = r"<td bgcolor=\"#FFFFFF\" class=\"s16\">(.*?)</td>"
        tmp = re.compile(key).findall(now)
        key = r"target=\"_blank\">(.*?)</a>"
        company = re.compile(key).findall(now)
        key = r"<td bgcolor=\"#FFFFFF\" class=\"s21\">(.*?)</td>"
        number = re.compile(key).findall(now)
        key = r"href=\"(/portal/project/buildlist/prjid/.*?html)"
        link = re.compile(key).findall(now)
        num += number
        result += tmp
        corpor += company
        links += link

    i = len(corpor) - 1
    while i >= 0:
        if i < 2 or (i - 1) % 3 == 0:
            del corpor[i]
        i -= 1

    i = len(result) - 1
    while i >= 0:
        if i < 6 or (i - 7) % 6 == 0 or (i - 9) % 6 == 0 or (i - 10) % 6 == 0:
            del result[i]
        i -= 1

    i = 0
    with open('link.txt', "a", encoding='utf-8') as f:
        while i < len(num) / 2:
            sheet.write(line, 0, result[i * 3])
            sheet.write(line, 1, corpor[i * 2])
            sheet.write(line, 2, result[i * 3 + 1])
            sheet.write(line, 3, corpor[i * 2 + 1])
            sheet.write(line, 4, result[i * 3 + 2])
            sheet.write(line, 5, num[i * 2])
            sheet.write(line, 6, num[i * 2 + 1])
            f.write(corpor[i * 2] + "  " + links[i] + '\n')
            i += 1
            line += 1
    f.close()

    return line


def getpagenum(text):
    soup = BeautifulSoup(text, 'html.parser')
    data = soup.findAll('a')
    # return data
    now = str(data[-1])
    result = []
    key = r"href=\".*p/(.*?).html\""
    result += re.compile(key).findall(now)
    if len(result) == 0:
        result.append('1')
    return result


def sheetinit(sheet):
    sheet.write(0, 0, '区域')
    sheet.write(0, 1, '项目名称')
    sheet.write(0, 2, '坐落')
    sheet.write(0, 3, '开发公司')
    sheet.write(0, 4, '总套数')
    sheet.write(0, 5, '可签约套数（住宅）')
    sheet.write(0, 6, '可签约套数（非住宅）')


if __name__ == "__main__":
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheetinit(sheet)
    url = 'http://www.lousw.com'
    urlstart = '/portal/index/kslpgs/district/'
    line = 1
    now = 1
    while now <= 11:
        response = getHTMLText(url + urlstart + str(now) + '.html')
        pagenum = int(getpagenum((response))[0])
        page = 1
        while page <= pagenum:
            response = getHTMLText(url + urlstart + str(now) + '/p/' + str(page) + '.html')
            line = getdata(response, sheet, line)
            print(now, str(page) + '/' + str(pagenum), line)
            page += 1
        now += 1

    wbk.save('test1.xls')

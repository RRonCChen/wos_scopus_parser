import csv
import json
import math
import re

from bs4 import BeautifulSoup
from selenium import webdriver

from wos_scopus_parser import scopus_paper


# url = "https://www.scopus.com/results/citedbyresults.uri?sort=plf-f&cite=2-s2.0-67650695660&src=s&imp=t&sid=9598eae676eac2bb238858200542531b&sot=cite&sdt=a&sl=0&origin=resultslist&editSaveSearch=&txGid=9e897c92882eef2b99e5c6ae5f0b80f0"


# 翻頁次數
def find_next_count(total_page):
    next_page_count = math.ceil(total_page / 20) -1
    return next_page_count


# 爬引用文資訊
def parse_citations(url, total_cite_count):

    # 先找citations的url
    browser = webdriver.Firefox()
    browser.implicitly_wait(15)
    browser.get(url)

    # request = requests.get(url)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    citation_url = soup.find('div',{'class':'recordPageBoxes docViewAll'}).a['href']
    print('citation_url : '+citation_url)

    browser.get(citation_url)


    # 要翻幾次
    next_count = find_next_count(total_cite_count)
    citations =[]
    while next_count >= 0:
        body = browser.page_source
        soup = BeautifulSoup(body, 'lxml')

        titles = soup.find_all('span', {'class': 'docTitle'})
        authors = soup.find_all('span', {'class': ' displayInlineBlock'})
        years = soup.find_all('div', {'class': 'dataCol4'})
        sourceTitle = soup.find_all('div', {'class': 'dataCol5'})
        cite_count = soup.find_all('div', {'class': 'dataCol6'})

        for i in range(0, len(titles)):
            replace1 = sourceTitle[i].find('div', {'class': 'additionalContent visibleHidden'}).text

            title = titles[i].text.strip()
            author = authors[i].text.strip()
            year = years[i].find('span').text.strip()
            source_title = sourceTitle[i].find('span').text.replace(replace1,'').strip()
            cite_text = re.search(r'\d{1,}', cite_count[i].text)
            cite = cite_text[0].strip()
            citation = scopus_paper.Citation(author, title, source_title, year, cite)
            citations.append(citation.__dict__)
        next_count -= 1
        if next_count >= 0:
            element = browser.find_element_by_class_name('nextPage')
            element.click()

    browser.close()
    return citations


with open('CKY.csv', encoding='utf-8', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    next(spamreader)
    Papers = []
    for row in spamreader:
        if row[4] != '':
            cite_count = int(row[4])
            url = row[6]
            print(row[6])
            print(row[0])
            citations = parse_citations(url, cite_count)
            Paper = scopus_paper.Paper(row[0], row[1], row[2], row[3], row[4], citations, row[7])
            Papers.append(Paper.__dict__)
        else:
            Paper = scopus_paper.Paper(row[0], row[1], row[2], row[3], '0', 'null', row[7])
            Papers.append(Paper.__dict__)


final = json.dumps(Papers)
with open('ChuanKaiYang.json', 'w') as outfile:
    outfile.write(final)
import json
import re

from bs4 import BeautifulSoup
from selenium import webdriver

from wos_scopus_parser import paper_object

# 存所有paper的url
paper_urls=[]
papers = []


# 取作者paper的urls
def get_urls(page):
    browser = webdriver.Firefox()
    browser.get('https://apps.webofknowledge.com/summary.do?product=WOS&parentProduct=WOS&search_mode=GeneralSearch&qid=4&SID=V1N1NKZsz1rPTwUpc91&page='+str(page)+'&action=changePageSize&pageSize=50')

    body = browser.page_source

    host_name = 'https://apps.webofknowledge.com'

    soup = BeautifulSoup(body,'lxml')
    url_blocks = soup.find_all("div", {"class" :"search-results-content"})


    for block in url_blocks:
        url = ''
        url = host_name+block.find("a",{"class":"smallV110"})['href']
        paper_urls.append(url)

    # 下一頁判斷
    total_page = soup.find('span',{'id':'pageCount.top'}).text
    if page < int(total_page):
        browser.close()
        page+=1
        get_urls(page)


# 去除第一頁的重複urls
def get_set_url(url_list):
    set_url = list(set(url_list))
    return set_url

# 根據第一頁爬到的url,擷取出其中的detail
def get_paper_detail():
    final_urls = get_set_url(paper_urls)

    browser = webdriver.Firefox()

    for url in final_urls:
        browser.get(url)

        # 按下期刊影響力，取得JCR資訊
        try:
            element = browser.find_element_by_link_text("檢視期刊影響力")
            element.click()

            soup = BeautifulSoup(browser.page_source, 'lxml')

            # impact_factor(5-years)
            impact_factor = soup.find('table', {'class': 'Impact_Factor_table'}).find('tbody').find_all('td')[
                1].text.strip()
            print(impact_factor)

            # JCR資訊
            JCR_table = soup.find('table', {'class': 'JCR_Category_table'}).find('tbody').find_all('tr')[1]
            JCR_categray = JCR_table.find_all('td')[0].text.strip()
            JCR_rank = JCR_table.find_all('td')[1].text.strip()
            JCR_quartile = JCR_table.find_all('td')[2].text.strip()
            print('JCR_categray : ' + JCR_categray)
            print('JCR_rank : ' + JCR_rank)
            print('JCR_quartile : ' + JCR_quartile)

            JCR_dic = {'impact_factor': impact_factor, 'JCR_categray': JCR_categray, 'JCR_rank': JCR_rank,
                       'JCR_quartile': JCR_quartile}
        except:

            soup = BeautifulSoup(browser.page_source, 'lxml')

            impact_factor = ''
            print(impact_factor)

            # JCR資訊
            JCR_categray = ''
            JCR_rank = ''
            JCR_quartile = ''
            print('JCR_categray : ' + JCR_categray)
            print('JCR_rank : ' + JCR_rank)
            print('JCR_quartile : ' + JCR_quartile)

            JCR_dic = {'impact_factor': impact_factor, 'JCR_categray': JCR_categray, 'JCR_rank': JCR_rank,
                       'JCR_quartile': JCR_quartile}


        # paper title
        title = soup.find(class_='title').value.text.replace('\\','')
        print('title : ' + title)

        # 取得paper共同作者
        authors = soup.find_all('a', {'title': '尋找此作者的其他記錄'})
        authors_list =[]
        for author in authors:
            print('aur'+author.text)
            authors_list.append(author.text)

        # 期刊或研討會名稱
        sourceTitle = soup.find('p', {'class', 'sourceTitle'}).value.text.replace('\\','')
        print('sourceTitle : ' + sourceTitle)

        # 時間
        date_group = soup.find_all('p', {'class': 'FR_field'})
        date =''
        for date_area in date_group:
            if re.search('出版日期:', date_area.text):
                date = date_area.value.text
                break
        print(date)



        # 引用數
        cite_count = soup.find('span', {'class': 'TCcountFR'}).text
        print('cite_count : ' + cite_count)

        host_name = 'https://apps.webofknowledge.com'

        # 判斷是否有引用次數
        if cite_count != '0':
            # 取引用文的第一頁
            citation_url = soup.find('a',{'title':'檢視引用這篇文獻的全部文獻'})['href']
            print(host_name + citation_url)

            # 引用文的urls
            citaion_urls = get_citation_url(host_name + citation_url)

            # 用來存citation detail的物件
            citations = []

            for url in citaion_urls:
                print('citation_paper : ')
                citation = get_citation_detail(url)
                citations.append(citation.__dict__)
            paper = paper_object.Paper(title, authors_list, sourceTitle, date, JCR_dic, cite_count, citations)
            print(paper.__dict__)
            papers.append(paper.__dict__)
        else:
            citation_url = 'null'
            print(citation_url)
            paper = paper_object.Paper(title, authors_list, sourceTitle, date, JCR_dic, cite_count, 'null')
            print(paper.__dict__)
            papers.append(paper.__dict__)

# 取的引用文的urls
def get_citation_url(url):
    browser = webdriver.Firefox()
    browser.get(url)

    body = browser.page_source

    host_name = 'https://apps.webofknowledge.com'

    soup = BeautifulSoup(body, 'lxml')
    url_blocks = soup.find_all("div", {"class": "search-results-content"})

    citaion_urls = []


    for block in url_blocks:
        url = ''
        url = host_name + block.find("a", {"class": "smallV110"})['href']
        citaion_urls.append(url)

    browser.close()

    final_citation_urls = get_set_url(citaion_urls)

    return final_citation_urls


#取得引用文detail
def get_citation_detail(url):
    browser = webdriver.Firefox()
    browser.get(url)

    # 按下期刊影響力，取得JCR資訊
    try:
        element = browser.find_element_by_link_text("檢視期刊影響力")
        element.click()

        soup = BeautifulSoup(browser.page_source, 'lxml')

        # impact_factor(5-years)
        impact_factor = soup.find('table', {'class': 'Impact_Factor_table'}).find('tbody').find_all('td')[
            1].text.strip()
        print(impact_factor)

        # JCR資訊
        JCR_table = soup.find('table', {'class': 'JCR_Category_table'}).find('tbody').find_all('tr')[1]
        JCR_categray = JCR_table.find_all('td')[0].text.strip()
        JCR_rank = JCR_table.find_all('td')[1].text.strip()
        JCR_quartile = JCR_table.find_all('td')[2].text.strip()
        print('JCR_categray : ' + JCR_categray)
        print('JCR_rank : ' + JCR_rank)
        print('JCR_quartile : ' + JCR_quartile)

        JCR_dic = {'impact_factor': impact_factor, 'JCR_categray': JCR_categray, 'JCR_rank': JCR_rank,
                   'JCR_quartile': JCR_quartile}
    except:
        soup = BeautifulSoup(browser.page_source, 'lxml')

        impact_factor = ''
        print(impact_factor)

        # JCR資訊
        JCR_categray = ''
        JCR_rank = ''
        JCR_quartile = ''
        print('JCR_categray : ' + JCR_categray)
        print('JCR_rank : ' + JCR_rank)
        print('JCR_quartile : ' + JCR_quartile)

        JCR_dic = {'impact_factor': impact_factor, 'JCR_categray': JCR_categray, 'JCR_rank': JCR_rank,
                   'JCR_quartile': JCR_quartile}


    title = soup.find(class_='title').value.text.replace('\\','')
    print('title : ' + title)

    sourceTitle = soup.find('p',{'class','sourceTitle'}).value.text.replace('\\','')
    print('sourceTitle : ' + sourceTitle)

    date_group = soup.find_all('p', {'class': 'FR_field'})
    date = ''
    for date_area in date_group:
        if re.search('出版日期:', date_area.text):
            date = date_area.value.text
            break
    print(date)

    cite_count = soup.find('span', {'class': 'TCcountFR'}).text
    print('cite_count : ' + cite_count)

    citation = paper_object.Citation(title, sourceTitle, date, JCR_dic, cite_count)

    browser.close()
    return citation


if __name__ == '__main__':
    get_urls(1)
    get_paper_detail()

    final = json.dumps(papers)
    with open('KwanLiuMa.json', 'w') as outfile:
        outfile.write(final)


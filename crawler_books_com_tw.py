# -*- coding: utf-8 -*-
"""
Author : Suo An Wang
參考 : http://pala.tw/python-web-crawler/
      http://cuiqingcai.com/1319.html

爬博客來的書籍
包括 書名, ISBN, 定價, 出版社, 作者, URL

有時候會有一點錯誤(定價1, -1元  之類的)
但是不會影響程式運行
會在最後結果看到有些書單不太正確
整體而言正常發揮
"""
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import re


def get_soup(url):
    driver = webdriver.PhantomJS(executable_path=r'C:\Users\shawn\Downloads\phantomjs-2.1.1-windows\bin\phantomjs')  # PhantomJs
    driver.get(url)  # 輸入範例網址，交給瀏覽器
    pageSource = driver.page_source  # 取得網頁原始碼
    #print(pageSource)
    driver.close()  # 關閉瀏覽器
    soup = BeautifulSoup(pageSource,'lxml')
    return soup
    
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

book_list = pd.DataFrame()

#在這裡修改想要抓取的書列，可以是List型態
url_multi = ['http://www.books.com.tw/web/books_bmidm_1411/?o=1&v=1&page=13',
             'http://www.books.com.tw/web/books_bmidm_1411/?o=1&v=1&page=14']

for k in url_multi:
    print(k)
    soup = get_soup(k)
    books = soup.body.find_all(name = 'h4')
    
    t_name = []
    t_url = []
    t_isbn = []
    t_price =[]
    t_pub = []
    t_author = []
    for i in range(len(books)):
        t_name = t_name + [str(books[i].string)] #取書名 page 1
        t_url = t_url + re.findall(r'"([^"]*)"', str(books[i])) #取URL page 1
        t_name = t_name[0:len(t_url)] #把非書籍砍掉

    count = 0
    for i in t_url:
        print(count)
        count = count + 1
        m_soup = get_soup(i)
        m_books = m_soup.body.find_all(itemprop="productID") # 取isbn
        t_isbn = t_isbn + [str(m_books)[21:34]]
        print("ISBN done.")
        m_books = m_soup.body.find_all(name="em") # 取 定價
        if (m_books == []):
            #print("T")
            t_price = t_price + ['-1']
        else:
            #print("F")
            t_price = t_price + [m_books[0].string]
        print("Price done.")
        m_books = m_soup.body.find_all(itemprop="brand") #取 出版社
        if (m_books == []):
            #print("T")
            t_pub = t_pub + ['-1']
        else:
            #print("F")
            t_pub = t_pub + [m_books[0].string]
        print("Publisher done.")
        m_books = str(m_soup.find_all(itemprop="author")) #取 作者名字
        t_author = t_author + [find_between( m_books, 'f=author">', '<' )]
        print("Author done.")

    t_dataframe = pd.DataFrame({'Book name': t_name,'URL': t_url,
                           'Price': t_price,'Pubilisher':t_pub,
                           'ISBN': t_isbn, 'Author': t_author})

    book_list = book_list.append(t_dataframe)
    print("book_list.shape : " +str(book_list.shape))
    del t_dataframe
    
book_list.to_csv('book_list_language_learning4.csv',line_terminator='\n',index = False)
print("Output to csv file")
                       

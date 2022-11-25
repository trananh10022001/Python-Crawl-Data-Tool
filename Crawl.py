from bs4 import BeautifulSoup
import urllib.request
import datetime
import mysql.connector

today = datetime.date.today()

count = 0
while(count <= 9):
    print("\t\t\t\t\t\tNgày: " + str(today.day-count) +" - " + str(today.month) +" - "+ str(today.year))
    url =  'https://tuoitre.vn/xem-theo-ngay/'+ str(today.day-count) +"-" + str(today.month) +"-"+ str(today.year)+'.htm'
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    new_feeds = soup.find('ul', class_='list-news-content').find_all('a')

    for feed in new_feeds:
        title = feed.get('title')
        if(title == 'Media' or title == 'Thời sự' or title == 'Thế giới' or title == 'Giải trí' or title == 'Pháp luật'
        or title == 'Nhịp sống trẻ' or title == 'Kinh doanh' or title == 'Cần biết' or title == 'Xe' or title == 'Thể thao'
        or title == 'Sức khỏe' or title == 'Nhà đất' or title == 'Tuyển sinh' or title == 'Doanh nghiệp'):
            continue
        else:
            link = feed.get('href')
            print('Title: {} - Link: {}'.format(title, link))
            # establishing the connection
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='news')
            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()
            # Preparing SQL query to INSERT a record into the database.
            sql = """INSERT INTO new(
               date,title,link)
               VALUES (%s,%s,%s)"""
            data = (str(today.year) + "-" + str(today.month) + "-" + str(today.day-count), title, link)
            try:
                # Executing the SQL command
                cursor.execute(sql,data)

                # Commit your changes in the database
                conn.commit()

            except:
                # Rolling back in case of error
                conn.rollback()
            # Closing the connection
            conn.close()
    count+=1








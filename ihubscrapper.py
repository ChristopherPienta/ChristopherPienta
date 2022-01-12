import sqlite3

# connect creates a connection to the data base file
conn = sqlite3.connect('ihub.db')

# cursor allows you to execut sql commands
cur = conn.cursor()

# get_ipython().system('pip install selenium')
# get_ipython().system('pip install msedge-selenium-tools')
# get_ipython().system('pip install bs4')
# get_ipython().system('pip install chromedriver-binary-auto')


from selenium import webdriver  # for interacting with brower? this is one of three that seem to have the same purpose?
import csv  # to make csv documents
import chromedriver_binary  # for interacting with brower? this is one of three that seem to have the same purpose?
import csv  # to make csv documents
from selenium.webdriver.common.keys import \
    Keys  # for interacting with brower? this is one of three that seem to have the same purpose?
import csv  # to make csv documents
import time  # using for time.sleep
from datetime import datetime  # for getting the current date
from bs4 import BeautifulSoup  # for extracting and html for websites
from selenium.webdriver.common.action_chains import ActionChains  # import is for the page scroller


## Setup date and time variables

now = datetime.now()  # current date and time

# year = now.strftime("%Y")
# print("year:", year)

# month = now.strftime("%m")
# print("month:", month)

# day = now.strftime("%d")
# print("day:", day)

# time = now.strftime("%H:%M:%S")
# print("time:", time)

date_time = now.strftime("%m/%d/%Y")

date = now.strftime("%m/%d/%Y")
print(str(date))

date2 = now.strftime('%m-%d-%y')
print(date2)

# ###  Investors Hub login page
driver = webdriver.Chrome()
url = 'https://investorshub.advfn.com/boards/profileb.aspx?user=190115'
driver.get(url)


# ### Enter login info
elem = driver.find_element_by_id("ctl00_CP1_LoginView1_Login1_UserName")
elem.send_keys("ENTER YOUR USER NAME HERE")
elem = driver.find_element_by_id("ctl00_CP1_LoginView1_Login1_Password")
elem.send_keys("ENTER_YOUR_PASSWORD_HERE")


# Navigate to favories page and extract html
fav_page = "https://investorshub.advfn.com/boards/favpeople.aspx"
driver.get(fav_page)
time.sleep(2)
soup = BeautifulSoup(driver.page_source, 'html.parser')


# ### Makes a list of the users and a list of the date they last posted
user_list = []
date_list = []


def fav_page(user_list, date_list):
    for t in soup.findAll('td', class_="text-truncate"):
        user = t.getText()
        user = user.replace('\n\n', '')
        if user[-1] == ' ':
            user = user[:-1]
        user_list.append(user)

    for x in soup.findAll('td', class_="text-center text-nowrap"):
        date = x.getText()
        date = date.replace("\n                    ", '')
        date = date.replace("\n                ", '')
        date = date[:10]
        date_list.append(date)

fav_page(user_list, date_list)



# ### Zips date and user list together
fav_messages = zip(user_list, date_list)
fav_page_dict = {key: value for key, value in zip(user_list, date_list)}
print(fav_page_dict)



# ### Makes list of users_who_posted today from user_list and date_list
users_who_posted = []
for key, value in fav_page_dict.items():
    day = str(date)
    if day == value:
        users_who_posted.append(key)
print(users_who_posted)


# Function to extract data from the user's (boards posted on) page
the_list = []
final_list = []
z_TS = []  # this trouble shoots turning z into an intiger for turning z into an int
user = ''
def extract_boards_posted_on(the_list, user):
    boards_posted_on = BeautifulSoup(driver.page_source, 'html.parser')  # extract data from boards posted on

    c = 1
    l = ''
    p = ''
    b = ''
    for i in boards_posted_on.findAll('td'):

        z = i.getText()
        if c == 1:
            b = z

        if c == 2:
            z = z[:10]
            l = z

        if c == 3:
            z = z.replace('\n', '')
            z = z.replace(',', '')
            z_TS.append(z)
            p = int(z)
            # print(type(l))
            # print(type(date))

        c += 1
        if c == 4:
            c = 1
            if p < 30:
                # the_list.append({'Board': b, 'Last Post': l, 'Posts': p})
                if l == date:
                    the_list.append({'User': user, 'Board': b, 'Posts': p})



# ### Loop goes through each users page and extracts the ticker symbol of new tickers that user posted about.
users = []  # this is for troble shooting this for loop
for user in users_who_posted:
    fav_page = "https://investorshub.advfn.com/boards/favpeople.aspx"
    driver.get(fav_page)

    # block below is the scroller
    element = driver.find_element_by_link_text(user)
    desired_y = (element.size['height'] / 2) + element.location['y']
    current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script(
        'return window.pageYOffset')
    scroll_y_by = desired_y - current_y
    driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)

    button = driver.find_element_by_link_text(user)
    # try:
    # button.click()
    # except:
    time.sleep(2)
    button.click()

    # try:
    time.sleep(2)
    button = driver.find_element_by_link_text('Boards Posted On')
    button.click()
    # except:
    # driver.execute_script("window.scrollTo(0, -500)")
    # time.sleep(2)
    # button.click()

    users.append(user)  # trouble shoot with this if for loop hits error
    extract_boards_posted_on(the_list, user)


# ### Srapeing the OTC Markets website for share structures
final_list = []
def otc_scrape(the_list, final_list):
    for index in range(len(the_list)):
        s = (the_list[index]['Board'])
        if s.count('(') > 0:
            t = s[s.find('(') + 1:s.find(')')]
            otc_url = 'https://www.otcmarkets.com/stock/{}/security'
            driver.get(otc_url.format(t))
            time.sleep(7)
            otc_soup = BeautifulSoup(driver.page_source, 'html.parser')
            field = 1
            for i in otc_soup.findAll('div', class_="sc-bdVaJa kYmYWE"):
                q = i.getText()
                q = str(q)
                if field == 1:
                    a = the_list[index]['User']
                if field == 2:
                    day = date_time
                if field == 5:
                    c = q
                if field == 6:
                    d = q
                if field == 7:
                    e = q
                if field == 8:
                    res = q
                if field == 9:
                    unr = q
                if field == 10:
                    dtc = q
                if field == 11:
                    f = q
                    final_list = [(a, t, c, d, e, res, unr, dtc, f, day)]
                    cur.executemany("INSERT INTO ihub_table values(?,?,?,?,?,?,?,?,?,?)", final_list)
                    conn.commit()
                if field == 13:
                    field == 0
                field += 1


otc_scrape(the_list, final_list)

conn.close();

# coding: utf-8

# In[1]:


import psycopg2
from bs4 import BeautifulSoup
from urllib.request import urlopen


# In[2]:


def db_entry(chat_id, username, tradelist_link, wishlist_link):
    try:
        conn = psycopg2.connect(DB.get_url(), sslmode='require')
        c = conn.cursor() 
        entry = (chat_id, username, tradelist_link, wishlist_link, chat_id, chat_id, username, tradelist_link, wishlist_link)
        c.execute('IF EXISTS(SELECT * FROM usernames WHERE chat_id=%s)'+ 
                      'UPDATE usernames SET username=%s, tradelist_link=%s, wishlist_link=%s WHERE chat_id=%s'
                  'ELSE'+
                      'INSERT INTO usernames VALUES (%s, %s, %s, %s)', entry)
        conn.commit()
    finally:
        c.close()
        conn.close()


# In[3]:


def cardset_fetcher(username):
    target_page = 'https://deckbox.org/users/'+username
    page = urlopen(target_page)
    if page != urlopen('https://deckbox.org/users'):
        soup = BeautifulSoup(page, 'lxml')
        cardlist = soup.find_all('li', attrs={'class':'submenu_entry'})
        return 'https://deckbox.org'+cardlist[1].a['href'], 'https://deckbox.org'+cardlist[2].a['href']
    else: 
        return 'https://deckbox.org', 'https://deckbox.org'


# In[4]:


def db_fetcher(index, searched_card):
    try:
        conn = psycopg2.connect(DB.get_url(), sslmode='require')
        c = conn.cursor()
        return_string = ''
        for row in c.execute('SELECT * FROM usernames'):
            return_string += search_cardset(row[1], row[index], searched_card)
        return return_string
    finally:
        c.close()
        conn.close()


# In[5]:


def search_cardset(username, cardlist, searched_card):
    target_page = cardlist+'/export?s=&f=&o='
    page = urlopen(target_page)
    soup = BeautifulSoup(page, 'lxml')
    if searched_card in soup.body.get_text().lower():
        return(username+'\n')
    return ''


# In[ ]:


def DB():
    url = ''
    def get_url():
        if DB.url == '':
            DB()
        return DB.url
    def __init__(self):
        if DB.url != '':
            pass
        else:
            DB.url = os.environ['DATABASE_URL']


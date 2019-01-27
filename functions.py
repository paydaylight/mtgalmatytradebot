
# coding: utf-8

# In[1]:


import psycopg2
from bs4 import BeautifulSoup
from urllib.request import urlopen


# In[2]:


def db_entry(chat_id, username, tradelist_link, wishlist_link):
    try:
        conn = psycopg2.connect(get_db_url(), sslmode='require')
        c = conn.cursor() 
        entry = (chat_id, username, tradelist_link, wishlist_link, username, tradelist_link, wishlist_link)
        c.execute('INSERT INTO usernames VALUES (%s, %s, %s, %s) ON CONFLICT (chat_id) DO UPDATE SET username=%s, tradelist_link=%s, wishlist_link=%s;', entry)
        conn.commit()
    finally:
        c.close()
        conn.close()


# In[3]:


def cardset_fetcher(username):
    target_page = 'https://deckbox.org/users/'+username
    page = urlopen(target_page)
    soup = BeautifulSoup(page, 'lxml')
    cardlist = soup.find_all('li', attrs={'class':'submenu_entry'})
    tradelist = 'https://deckbox.org'+cardlist[1].a['href']
    wishlist = 'https://deckbox.org'+cardlist[2].a['href']
    
    return tradelist, wishlist 


# In[4]:


def db_fetcher(index, searched_card):
    try:
        conn = psycopg2.connect(get_db_url(), sslmode='require')
        c = conn.cursor()
        return_string = ''
        c.execute('SELECT * FROM usernames;')
        for row in c:
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


# In[6]:


def get_db_url():
    return os.environ['DATABASE_URL']


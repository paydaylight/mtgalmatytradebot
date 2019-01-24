
# coding: utf-8

# In[1]:


import sqlite3
from bs4 import BeautifulSoup
from urllib.request import urlopen


# In[2]:


def db_entry(chat_id, username, tradelist_link, wishlist_link):
    try:
        conn = sqlite3.connect('mtgtradebot.db')
        c = conn.cursor() 
        entry = (chat_id, username, tradelist_link, wishlist_link, chat_id, chat_id, username, tradelist_link, wishlist_link)
        c.execute('IF EXISTS(SELECT * FROM usernames WHERE chat_id=?)'+ 
                      'UPDATE usernames SET username=?, tradelist_link=?, wishlist_link=? WHERE chat_id=?'
                  'ELSE'+
                      'INSERT INTO usernames VALUES (?, ?, ?, ?)', entry)
        conn.commit()
    finally:
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
        conn = sqlite3.connect('mtgtradebot.db')
        c = conn.cursor()
        return_string = ''
        for row in c.execute('SELECT * FROM usernames'):
            return_string += search_cardset(row[1], row[index], searched_card)
        return return_string
    finally:
        conn.close()


# In[5]:


def search_cardset(username, cardlist, searched_card):
    target_page = cardlist+'/export?s=&f=&o='
    page = urlopen(target_page)
    soup = BeautifulSoup(page, 'lxml')
    if searched_card in soup.body.get_text().lower():
        return(username+'\n')
    return ''


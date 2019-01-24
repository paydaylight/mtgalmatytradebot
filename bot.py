
# coding: utf-8

# Trade bot for MTG Almaty community

# In[23]:


import telebot, os, markups, functions
from telegram.ext import Updater


# In[17]:


TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(TOKEN)


# In[24]:


commands = {'/help' : 'List of available commands', 
            '/wts' : 'Want To Sell/trade card', 
            '/wtb' : 'Want To Buy/trade card', 
            '/start' : 'Initiate new user or update old information'}


# In[25]:


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id, get_commands())


# In[26]:


@bot.message_handler(commands=['wtb'])
def wtb_handler(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Enter card name to search')
    bot.register_next_step_handler(msg, wtb_response)
def wtb_response(message):
    chat_id = message.chat.id
    text = message.text.lower()
    lst = db_fetcher(2, text) 
    if all(x is '' for x in lst):
        msg = bot.send_message(chat_id, "Nothing found")
    else:
        msg = bot.send_message(chat_id, "That's what I found:\n"+lst)


# In[27]:


@bot.message_handler(commands=['wts'])
def wts_handler(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Enter card name to search')
    bot.register_next_step_handler(msg, wts_response)
def wts_response(message):
    chat_id = message.chat.id
    text = message.text.lower()
    lst = db_fetcher(3, text) 
    if all(x is '' for x in lst):
        msg = bot.send_message(chat_id, "Nothing found")
    else:
        msg = bot.send_message(chat_id, "That's what I found:\n"+lst)


# In[28]:


@bot.message_handler(commands=['start'])
def start_handler(message):
    msg = bot.send_message(message.chat.id, 'To work with this bot please provide your valid deckbox.org username')
    bot.register_next_step_handler(msg, username_handler)
def username_handler(message):
    username = message.text
    tradelist_link, wishlist_link = cardset_fetcher(username)
    if tradelist_link != wishlist_link:
        db_entry(message.chat.id, username, tradelist_link, wishlist_link)
        bot.send_message(message.chat.id, 'Successfully added', reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id, 'Seems like such user does not exist, please check spelling and try again', reply_markup=markup)
        bot.register_next_step_handler(msg, username_handler)


# In[29]:


def get_commands():
    string = ''
    for key in commands:
        string += key+' - '+commands[key]+'\n'
    return string


# In[13]:


PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN)
updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
updater.bot.set_webhook("https://mtgalmatytradebot.herokuapp.com/" + TOKEN)
updater.idle()


# In[15]:





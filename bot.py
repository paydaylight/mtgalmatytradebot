
# coding: utf-8

# Trade bot for MTG Almaty community

# In[1]:


import telebot
import os

# In[2]:


TOKEN = os.environ[TELEGRAM_TOKEN]
bot = telebot.TeleBot(TOKEN)


# In[3]:


@bot.message_handler(commands=['help'])
def start_handler(message):
    bot.send_message(message.chat.id, 'To be updated')
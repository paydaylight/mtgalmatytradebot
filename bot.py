
# coding: utf-8

# Trade bot for MTG Almaty community

# In[1]:


import telebot
import os

# In[2]:


TOKEN = "737356832:AAEoCl3if1mp_sHijO_Ij_dCyaveZcBcInQ"
bot = telebot.TeleBot(TOKEN)


# In[3]:


@bot.message_handler(commands=['help'])
def start_handler(message):
    bot.send_message(message.chat.id, 'To be updated', reply_markup=m.source_markup)


# In[4]:


@bot.message_handler(content_types=['text'])
def wts_handler(message):
    global isRunning
    if not isRunning:
        chat_id = message.chat.id
        text = message.text
        msg = bot.send_message(chat_id, 'Enter card name to search')
        bot.register_next_step_handler(msg, wtsResponse)
        isRunning = True
def wtsResponse(message):
    chat_id = message.chat.id
    text = message.text.lower()
    msg = bot.send_message(chat_id, 'Soon I will be able to find it!')
    isRunning = False

bot.polling(none_stop=True)


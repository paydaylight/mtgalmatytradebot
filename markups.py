
# coding: utf-8

# In[3]:


import telebot


# In[ ]:


source_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
source_markup_btn1 = types.KeyboardButton('wts')
source_markup_btn2 = types.KeyboardButton('wtb')
source_markup.add(source_markup_btn1, source_markup_btn2)


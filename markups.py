
# coding: utf-8

# In[4]:


from telebot import types


# In[5]:


markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
markup_btn1 = types.KeyboardButton('/wts')
markup_btn2 = types.KeyboardButton('/wtb')
markup_btn3 = types.KeyboardButton('/update')
markup_btn4 = types.KeyboardButton('/help')
markup.add(markup_btn1, markup_btn2, markup_btn3, markup_btn4)


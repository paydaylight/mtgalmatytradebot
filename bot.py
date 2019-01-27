
# coding: utf-8

# In[1]:


import os, functions
from telegram.ext import (Updater, CommandHandler)


# In[2]:


import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# In[3]:


commands = {'/help' : 'List of available commands', 
            '/wts' : 'Want To Sell/trade card', 
            '/wtb' : 'Want To Buy/trade card', 
            '/start' : 'Command to initiate conversation with bot',
            '/setname' : 'Set your deckbox.org username'}


# In[4]:


def start(bot, update):
    update.message.reply_text('Hello! I am trade bot, I will help you with trading MTG cards in Almaty!\n'
                              'Simply type /setname and your deckbox.org username(do not forget about whitespace) '
                              'to start searching for cards!\n'
                              'Run /help command to check list of available commands.\n\n'
                              'Type /wts + name of the card you want to sell/trade to search for any matches.\n'
                              'The same is true for /wtb + name of the card you want to buy/trade!\n\n'
                              'Example: "/wts Adorned Pouncer" command will return any matching person who have Adorned Pouncer '
                              'in their deckbox.org wishlist. ')


# In[5]:


def setname(bot, update, args):
    username = "".join(args)
    tradelist_link, wishlist_link = functions.cardset_fetcher(username)
    if 'users' not in tradelist_link+wishlist_link:
        functions.db_entry(update.message.chat_id, username, tradelist_link, wishlist_link)
        update.message.reply_text('Successfully added')
    else:
        update.message.reply_text('Seems like such user does not exist, please check spelling and try again')


# In[6]:


def wtb(bot, update, args):
    if ''.join(args) != '':
        lst = functions.db_fetcher(2, " ".join(args).lower()) 
        if all(x is '' for x in lst):
            update.message.reply_text("Nothing found")
        else:
            update.message.reply_text("That's what I found:\n"+lst)
    else:
        update.message.reply_text("Are you really searching for something? Provide real card name then!")


# In[7]:


def wts(bot, update, args):
    if ''.join(args) != '':
        lst = functions.db_fetcher(3, " ".join(args).lower()) 
        if all(x is '' for x in lst):
            update.message.reply_text("Nothing found")
        else:
            update.message.reply_text("That's what I found:\n"+lst)
    else:
        update.message.reply_text("Are you really searching for something? Provide real card name then!")


# In[8]:


def help_command(bot, update):
    update.message.reply_text(get_commands())


# In[9]:


def get_commands():
    string = ''
    for key in commands:
        string += key+' - '+commands[key]+'\n'
    return string


# In[10]:


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# In[11]:


def main():
    TOKEN = os.environ['TELEGRAM_TOKEN']
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('setname', setname, pass_args=True))
    dp.add_handler(CommandHandler('wts', wts, pass_args=True))
    dp.add_handler(CommandHandler('wtb', wtb, pass_args=True))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_error_handler(error)
    
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://mtgalmatytradebot.herokuapp.com/" + TOKEN)
    updater.idle()


# In[12]:


if __name__ == '__main__':
    main()


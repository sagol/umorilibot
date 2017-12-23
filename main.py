import logging
import time
from telegram.ext import Updater, Filters
from telegram.ext import (CommandHandler, MessageHandler, CallbackQueryHandler,
                          ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from config import Config
from bot import Bot

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

config = Config()
config.load()
ubot = Bot(config)

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text(ubot.start())


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(ubot.help())

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def site_handler(bot, update, user_data):
    query = update.callback_query

    if query.message:
        bot.editMessageReplyMarkup(chat_id=query.message.chat_id, 
                                   message_id=query.message.message_id,
                                   reply_markup=InlineKeyboardMarkup([]))

    names = ubot.get_sources_names(query.data)
    user_data['site'] = query.data
    button_list = [InlineKeyboardButton(desc, callback_data=name) for (name, desc) in names]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
    bot.send_message(query.message.chat_id, text="Выберите раздел", reply_markup=reply_markup)
    return SITE_NAME

def site_name_handler(bot, update, user_data):
    query = update.callback_query
    if query.message:
        bot.editMessageReplyMarkup(chat_id=query.message.chat_id, 
                                   message_id=query.message.message_id, 
                                   reply_markup=InlineKeyboardMarkup([]))    
    user_data['name'] = query.data
    user_data['stories'] = ubot.get(num=None, site_names=[user_data['name']])
    if (len( user_data['stories']) == 0):
        return ConversationHandler.END
    button_list = [InlineKeyboardButton(s, callback_data=s) for s in ['stop', 'next']]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    text = user_data['stories'][user_data['count']%len( user_data['stories'])]
    bot.send_message(query.message.chat_id, text=text, reply_markup=reply_markup, parse_mode='HTML')
    user_data['count'] = 1
    return SITE_READ

def site_read_handler(bot, update, user_data):
    query = update.callback_query
    if query.message:
        bot.editMessageReplyMarkup(chat_id=query.message.chat_id, 
                                   message_id=query.message.message_id, 
                                   reply_markup=InlineKeyboardMarkup([]))    
    if (query.data == 'stop' or user_data['count'] > len( user_data['stories'])):
        return ConversationHandler.END
        
    button_list = [InlineKeyboardButton(s, callback_data=s) for s in ['stop', 'next']]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    text = user_data['stories'][user_data['count']%len( user_data['stories'])]
#    bot.send_message(query.message.chat_id, text=user_data["count"])

    bot.send_message(query.message.chat_id, text=text, reply_markup=reply_markup, parse_mode='HTML')
    user_data['count'] = user_data['count'] + 1
    return SITE_READ

def get(bot, update, user_data):
    """Send a dev message when the command /get is issued."""
    user_data['count'] = 0
    messages = ubot.get_sources_sites()
    button_list = [InlineKeyboardButton(s, callback_data=s) for s in messages]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3), one_time_keyboard=True)
    bot.send_message(update.message.chat_id, text="Выберите сайт", reply_markup=reply_markup)
    return SITE

def random(bot, update, user_data):
    """Send a dev message when the command /random is issued."""
    user_data['count'] = 0
    user_data['stories'] = ubot.random(num=None, site_names=None)
    if (len( user_data['stories']) == 0):
        return ConversationHandler.END
    button_list = [InlineKeyboardButton(s, callback_data=s) for s in ['stop', 'next']]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    text = user_data['stories'][user_data['count']%len( user_data['stories'])]
    bot.send_message(update.message.chat_id, text=text, reply_markup=reply_markup, parse_mode='HTML')
    user_data['count'] = 1
    return SITE_READ

def stop(bot, update):
    print(stop)
    return ConversationHandler.END

def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    logger.info('Echo "%s"', update)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

SITE, SITE_NAME, SITE_READ = range(3)

def main():
    
    """Start the bot."""
    updater = Updater(config.get_token())

    while not ubot.load():
        logger.warning('Umorili bot loading error')
        time.sleep(10)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, help))

    dp.add_error_handler(error)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('get', get, pass_user_data=True)],
        states={
            SITE: [CallbackQueryHandler(site_handler, pass_user_data=True)],
            SITE_NAME: [CallbackQueryHandler(site_name_handler, pass_user_data=True)],
            SITE_READ: [CallbackQueryHandler(site_read_handler, pass_user_data=True)]
        },
        fallbacks=[CallbackQueryHandler(site_read_handler, pass_user_data=True)]
    )
    dp.add_handler(conv_handler)

    conv_rnd_handler = ConversationHandler(
        entry_points=[CommandHandler('random', random, pass_user_data=True)],
        states={
            SITE_READ: [CallbackQueryHandler(site_read_handler, pass_user_data=True)]
        },
        fallbacks=[CallbackQueryHandler(site_read_handler, pass_user_data=True)]
    )
    dp.add_handler(conv_rnd_handler)


    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
import logging
from telegram.ext import Updater, Filters
from telegram.ext import (CommandHandler, MessageHandler, CallbackQueryHandler,
                          ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from config import Config
from bot import Bot

#names = stories.get_names()
#sites = list(set(names.values()))
#site_names = list(names.keys())
#print(sites)
#print(site_names)
#print([(x.get().get('site'), x.get().get('site_name')) for x in
#    stories.get(num=1, sites=sites, site_names=site_names, random=True)])

#print(list(set(names.values())))


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

config = Config()
config.load()
ubot = Bot(config)

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text(ubot.help())

def random(bot, update):
    """Send a message when the command /help is issued."""
    messages = ubot.random()
    for message in messages:
        bot.send_message(update.message.chat_id, text=message, parse_mode='HTML')


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

def site_handler(bot, update):
    query = update.callback_query
    print(query.data)
    names = ubot.get_sources_names(query.data)
    button_list = [InlineKeyboardButton(s, callback_data=s) for s in names]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
    bot.send_message(query.message.chat_id, text="Выберите раздел", reply_markup=reply_markup)
    return SITE_NAME

def site_name_handler(bot, update):
    query = update.callback_query
    print(query.data)
    query.message.reply_text(query.data)
    return SITE


def get(bot, update):
    """Send a dev message when the command /dev is issued."""
    messages = ubot.get_sources_sites()
    button_list = [InlineKeyboardButton(s, callback_data=s) for s in messages]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
    bot.send_message(update.message.chat_id, text="Выберите сайт", reply_markup=reply_markup)
    return SITE

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

SITE, SITE_NAME = range(2)

def main():
    
    """Start the bot."""
    updater = Updater(config.get_token())

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("random", random))

    #dp.add_handler(CommandHandler("get", get))
    #dp.add_handler(CallbackQueryHandler(button_handler))

    dp.add_handler(MessageHandler(Filters.text, help))

    dp.add_error_handler(error)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('get', get)],
        states={
            SITE: [CallbackQueryHandler(site_handler)],
            SITE_NAME: [CallbackQueryHandler(site_name_handler)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)


    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
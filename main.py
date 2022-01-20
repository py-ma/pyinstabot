from telebot import *
import instaloader
import time
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])  # command handler for /start
def welcome(message):
    bot.send_message(message.chat.id,
                     'Добро пожаловать!\nОтправь мне никнейм Instagram—аккаунта, и я пришлю тебе его анализ'
                     '\nВнимание! Действует ограничение по времени (аккаунты можно присылать раз в 10 минут)')
@bot.message_handler(content_types=['text'])
def search(message):
    try:
        msg = message.text
        nickname = msg
        bot.send_message(message.chat.id, f'Анализ пользователя {nickname}'
                         f'\nПроцесс может занять некоторое время, пожалуйста, подождите')

        L = instaloader.Instaloader()
        L.login(config.nick, config.password)  # (login)

        # NICK FROM USER
        Profile = instaloader.Profile.from_username(L.context, nickname)

        # Create list of followers
        followers_list = []
        for followers in Profile.get_followers():
            followers_list.append(followers.username)

        bot.send_message(message.chat.id, f'Пользователь {nickname}'
                                          f'\nКоличество подписчиков: {len(followers_list)}')

        # Checking followers without pic
        followers_pic = []
        followers_no_pic = []
        for acc in followers_list:
            account = instaloader.Profile.from_username(L.context, acc)
            account.profile_pic_url
            followers_pic.append(account.profile_pic_url)
            # time.sleep(0.1)
        for no_pic in followers_pic:
            if "https://instagram" in no_pic:
                followers_no_pic.append(no_pic)
            else:
                pass
            # time.sleep(0.1)
        bot.send_message(message.chat.id, f'\nИз них без аватарок: {len(followers_no_pic)}')

        # Checking the list of subscribers on existing business accounts
        check_business = []
        for accounts in followers_list:
            business = instaloader.Profile.from_username(L.context, accounts)
            if business.is_business_account is True:
                check_business.append(business.is_business_account)
            else:
                pass


        bot.send_message(message.chat.id, f'\nБизнес-аккаунтов: {len(check_business)}')
        time.sleep(600)


    except:
        bot.send_message(message.chat.id, 'Не понял! Попробуй еще раз')


bot.polling(none_stop=True, interval=0)

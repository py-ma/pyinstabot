from telebot import *
import instaloader
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
        
        # Checking followers without pic
        followers_no_pic = []
        
        # Checking the list of subscribers on existing business accounts
        check_business = []
        
        # Create list of followers
        followers_list = []
        
        for followers in Profile.get_followers():
            followers_list.append(followers.username)

            account = instaloader.Profile.from_username(L.context, followers.username)
            if account.is_business_account is True:
                check_business.append(account.is_business_account)
            pic = account.profile_pic_url
            pic = str(pic)
            if "https://instagram" in pic:
                followers_no_pic.append(pic)
            else:
                pass

        bot.send_message(message.chat.id, f'Пользователь {nickname}'
                                          f'\nКоличество подписчиков: {len(followers_list)}')

        bot.send_message(message.chat.id, f'\nИз них без аватарок: {len(followers_no_pic)}')

        bot.send_message(message.chat.id, f'\nБизнес-аккаунтов: {len(check_business)}')

    except:
        bot.send_message(message.chat.id, 'Ошибка! Попробуй еще раз')

bot.polling(none_stop=True, interval=0)

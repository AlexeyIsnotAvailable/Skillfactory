# %%
import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n <имя валюты> \
<в какую валюту перевести>\
<количество переводимой валюты>\n\
Увидеть список всех доступных валют /values'
    bot.reply_to(message, text)
    
@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        values = message.text.split(' ')
    
        if len(values) != 3:
            raise ConvertionException('Слишком много или мало параметров.')
    
        quote, base, amount = values
    
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка ввода пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка программы\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)
    
    
bot.polling(non_stop=True)





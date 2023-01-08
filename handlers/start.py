from config import *

@bot.message_handler(commands=['start'])
def startbot(msg):
    # import pdb; pdb.set_trace()
    msg.from_user.id
    "Ignites the bot application to take action"

    bot.reply_to(
        msg,
        f"Welcome To Token Transaction Buy Bot, Your Bot Session Is Live And Running - {msg.from_user.id}"
    )



def start_event(symbol, event):
    res = Web3.toHex(event['transactionHash'])
    print(res)
    bot.send_message(
        577180091,
        f"New {symbol} Buy Event - {res}"
    )

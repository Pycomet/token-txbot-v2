from config import *
import multiprocessing

@bot.message_handler(commands=['start'])
def startbot(msg):
    # import pdb; pdb.set_trace()
    msg.from_user.id
    "Ignites the bot application to take action"

    bot.reply_to(
        msg,
        f"Welcome To Token Transaction Buy Bot, Your Bot Session Is Live And Running - {msg.from_user.id}"
    )

    


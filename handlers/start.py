from config import *
from multiprocessing import active_children


@bot.message_handler(commands=['start'])
def startbot(msg):
    # import pdb; pdb.set_trace()
    msg.from_user.id
    "Ignites the bot application to take action"

    bot.reply_to(
        msg,
        f"Welcome To Token Transaction Buy Bot, \n\n Your Bot Session Is Live And Watching {len(threading.enumerate()) - 3} Tokens With Ease 😊  \n\n  <b>ID: {msg.from_user.id}</b>",
        parse_mode="html"
    )

    # for e in active_children():
    #     bot.send_message(
    #         msg.from_user.id,
    #         f"{e.name} Running...."
    #     )
    for thread in threading.enumerate()[3:]:
        sym = thread.getName()

        bot.send_message(
            msg.from_user.id,
            f"{sym} Running...."
        )

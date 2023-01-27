from config import *
from multiprocessing import active_children


@bot.message_handler(commands=['start'])
def startbot(msg):
    # import pdb; pdb.set_trace()
    msg.from_user.id
    "Ignites the bot application to take action"

    bot.reply_to(
        msg,
        f"Welcome To Token Transaction Buy Bot, \n\n Your Bot Session Is Live And Watching {len(active_pools.keys())} Tokens With Ease 😊  \n\n  <b>ID: {msg.from_user.id}</b>",
        parse_mode="html"
    )
    print(active_pools)
    # bot.send_message(
    #     'ETHTopBullishTrending',
    #     "HELl o Test ,e"
    # )

    for e in active_pools.keys():
        bot.send_message(
            msg.from_user.id,
            f"{e} Running"
        )

    # for thread in threading.enumerate()[3:]:
    #     sym = thread.getName()

    #     bot.send_message(
    #         msg.from_user.id,
    #         f"{sym} Running...."
    #     )

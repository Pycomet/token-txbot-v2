from config import *
from bot import *


@bot.message_handler(commands=['add'])
def add_token(msg):
    "Remove Running Token Session"

    question = bot.send_message(
        msg.from_user.id,
        "Please paste the <b>token address</b> of the token you would like Bobby to track. (Example: <b>0xe03B2642A5111aD0EFc0cbCe766498c2dd562Ae9 BC BCChat 🟢</b>)",
        parse_mode="html"
    )
    bot.register_next_step_handler(question, add_action)


def add_action(msg):
    data = msg.text.split()
    address = data[0].lower()
    symbol = data[1].upper()
    tg_link = data[2]
    icon = data[3]

    # p = Process(target=start_streaming, name=symbol, args=(symbol, address))
    # p.start()

    if len(data) == 4:
        r = executor.submit(start_streaming, symbol, address, tg_link, icon)
        print(r.done())
        active_pools[symbol] = r

        bot.send_message(
            msg.from_user.id,
            f"📗 <b>New Token Alert {icon} </b> \n\nSession Name: <b>{symbol}</b> \n\nContract Address: <b>{address}</b> \n\nTelegram Link: <b>{tg_link}</b>",
            parse_mode="html"
        )

    else:
        bot.send_message(
            msg.from_user.id,
            f" <b> Invalid Parameters </b> ",
            parse_mode="html"
        )

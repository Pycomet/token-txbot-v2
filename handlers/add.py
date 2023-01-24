from config import *
from bot import *


@bot.message_handler(commands=['add'])
def add_token(msg):
    "Remove Running Token Session"

    question = bot.send_message(
        msg.from_user.id,
        "Please paste the <b>token address</b> of the token you would like Bobby to track. (Example: <b>0xe03B2642A5111aD0EFc0cbCe766498c2dd562Ae9 BC</b>)",
        parse_mode="html"
    )
    bot.register_next_step_handler(question, add_action)


def add_action(msg):
    data = msg.text.split()
    address = data[0].lower()
    symbol = data[1].upper()

    # p = Process(target=start_streaming, name=symbol, args=(symbol, address))
    # p.start()

    # executor.submit(start_streaming, symbol, address, name=symbol)

    p = threading.Thread(start_streaming, name=symbol, args=(symbol, address))
    p.start()

    bot.send_message(
        msg.from_user.id,
        f"📗 <b>New Token Alert </b> \n\nSession Name: <b>{symbol}</b> \n\nContract Address: <b>{address}</b>",
        parse_mode="html"
    )

from config import *
from bot import *


@bot.message_handler(commands=['add'])
def add_token(msg):
    "Remove Running Token Session"
    # print(msg)

    question = bot.send_message(
        msg.from_user.id,
        "Please paste the <b>token address</b> of the token you would like Bobby to track. (Example: <b>0xe03B2642A5111aD0EFc0cbCe766498c2dd562Ae9 BC https://t.me/BCChat 🟢</b>)",
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
        if len(active_children()) <= 10 and symbol not in active_pools.keys():
            with SemaphoreContext(sem):
                # r = executor.submit(start_streaming, symbol,
                #                     address, tg_link, icon)
                # print(r.done())
                active_pools[symbol] = {
                    "symbol": symbol,
                    "address": address,
                    "tg_link": tg_link,
                    "icon": icon
                }
                global executor
                for session in active_children():
                    session.terminate()
                    print("terminator")
                executor.shutdown(wait=False)

                executor = ProcessPoolExecutor(max_workers=10)

                for token_symbol in active_pools.keys():
                    data = active_pools[token_symbol]

                    r = executor.submit(
                        start_streaming,
                        data['symbol'],
                        data['address'],
                        data['tg_link'],
                        data['icon'],
                    )

                    print(r.done())

                bot.send_message(
                    msg.from_user.id,
                    f"📗 <b>New Token Alert {icon} </b> \n\nSession Name: <b>{symbol}</b> \n\nContract Address: <b>{address}</b> \n\nTelegram Link: <b>{tg_link}</b>",
                    parse_mode="html"
                )
        elif symbol in active_pools.keys():
            bot.send_message(
                msg.from_user.id,
                f" <b> Token already registered </b> ",
                parse_mode="html"
            )

        else:
            bot.send_message(
                msg.from_user.id,
                f" <b> You have reach the maximum allowed tokens </b> ",
                parse_mode="html"
            )

    else:
        bot.send_message(
            msg.from_user.id,
            f" <b> Invalid Parameters </b> ",
            parse_mode="html"
        )

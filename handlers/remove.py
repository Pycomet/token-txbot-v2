from config import *
import threading


@bot.message_handler(commands=['remove'])
def remove_token(msg):
    "Remove Running Token Session"

    question = bot.send_message(
        msg.from_user.id,
        "Please provide the symbol of the token you wish to remove (Example: <b>BC</b>)",
        parse_mode="html"
    )
    bot.register_next_step_handler(question, remove_action)


def remove_action(msg):
    token_symbol = msg.text.upper()

    # for session in active_children():
    if token_symbol.upper() in active_pools.keys():
        # Remove process and notify user
        try:
            active_pools[token_symbol.upper()].set_result("Process completed.")
        except:
            active_pools[token_symbol.upper()].cancel()

        del active_pools[token_symbol.upper()]

        bot.send_message(
            msg.from_user.id,
            f"<b>{token_symbol}</b> 🗑️ ... Has Been Removed From My Registry!  ",
            parse_mode="html"
        )

        return
    else:
        pass
    # for thread in threading.enumerate():
    #     if token_symbol == thread.getName():
    #         thread.cancel()
    #         thread.join()

    bot.send_message(
        msg.from_user.id,
        f"<b>{token_symbol}</b> Not Found!",
        parse_mode="html"
    )
    return

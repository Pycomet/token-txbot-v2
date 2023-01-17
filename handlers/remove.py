from config import *

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

    for session in active_children():
        if session.name == token_symbol:
            # Remove process and notify user
            session.terminate()
            bot.send_message(
                msg.from_user.id,
                f"<b>{token_symbol}</b> 🗑️ ... Has Been Removed From My Registry!  ",
                parse_mode="html"
            )

            return
        else:
            pass

    
    bot.send_message(
        msg.from_user.id,
        f"<b>{token_symbol}</b> Not Found!",
        parse_mode="html"
    )   
    return


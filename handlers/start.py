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


# Bitcoin Buy!
# 🟢🟢🟢🟢

# 💵 0.035 ETH ($42.31)
# 🪪 0x94af…f888 | Txn | Track
# ✅ New Holder
# 🔘 Market Cap $5,474,579

# 📊 Chart 🗳 Buy Now
# 🅰️ Alpha 🔵 Trending


def start_event(symbol, event):
    "Send Buy Event To Group"
    print(event)
    bot.send_message(
        577180091,
        f"New {symbol} Buy Event - {event}"
    )


    bot.send_message(
        -374682568,
        f"<a href='https://google.com'>{event['token_symbol']}</a> Buy! \n🟢🟢🟢🟢🟢🟢🟢🟢 \
            \n\n 💵 {event['price']} ETH (${event['usd_value']}) \
            \n 🪪 <a href='https://etherscan.io/address/{event['address']}'>{event['address'][:5]}...{event['address'][-4:]}</a> | <a href='https://etherscan.io/tx/{event['tx_hash']}'>Txn</a>| Track \
            \n ✅  New Holder \n 🔘 Market Cap ${event['market_cap']} \
            \n\n <a href='https://dexscreener.com/ethereum/{event['contractAddress']}'>📊 Chart</a>",
        parse_mode="html"
    )


from config import *
from handlers import *
from bot import *
import os
import multiprocessing

@app.route('/' + TOKEN, methods=['POST', 'GET'])
def checkWebhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Your bot application is still active!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    process = multiprocessing.Process(target=run)
    process.start()
    bot.set_webhook(url=SERVER_URL + '/' + TOKEN)
    return "Application running!", 200


if __name__ == "__main__":
    
    if DEBUG != True:
        app.run(host="0.0.0.0", threaded=True, port=int(os.environ.get('PORT', 5003)))
    else:
        process = multiprocessing.Process(target=run)
        bot.remove_webhook()
        process.start()
        print("Bot polling!")
        bot.polling()
        

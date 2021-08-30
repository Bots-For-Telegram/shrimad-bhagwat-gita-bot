from telegram.ext import Updater ,CommandHandler, MessageHandler, Filters
import logging
import random
import os
import pygita
TOKEN = os.environ.get("TOKEN")
PORT = os.environ.get("PORT",5000)
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

client = pygita.Client(CLIENT_ID, CLIENT_SECRET)


def start(update,context):
    message = "Hi!! {} , To get random verse of Srimadbhagavad Gita send /verse.To get a specific verse send /verse <chapter no> <verse no>.\n \nadd 'hi' or 'en' to get meaning also. \nExamples : /verse 1 4 (verse 1 from chapter 2)\n ,/verse 1 (random verse from chapter 1)\n ,/verse (random verse)\nBot developed by @TheShubhendra".format(update.message.from_user.first_name)  
    context.bot.send_message(update.message.chat_id,message)

def verse(update,context):
  text = update.message.text.lower()
  text=text.split()
  numbers = [i for i in text if i.isdigit()]
  verse_numner=None
  chapter_numner=None
  try:
    verse_number = numbers[1]
  except:
    pass
  try:
    chapter_number = numbers [0]
  except:
    pass
  if verse_number and chapter_number:
    if "hi" in text:
      verse = client.get_verse(chapter_number,verse_number,language="hi")
      update.message.reply_text(verse.text+"\n"+verse.meaning)
    elif "en" in text:
      verse = client.get_verse(chapter_number,verse_number,language="en")
      update.message.reply_text(verse.text+"\n"+verse.meaning)
    else:
      verse = client.get_verse(chapter_number,verse_number)
      update.message.reply_text(verse.text)
  else:
    update.message.reply_text("Please provide verse and chapter number properly.")
def main():  
  
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  updater = Updater(token=TOKEN)
  dispatcher = updater.dispatcher

  handler = CommandHandler(["verse","verse_hi","verse_en"],verse)
  
  start_handler = CommandHandler('start',start)
  dispatcher.add_handler(handler)
  dispatcher.add_handler(start_handler)

  updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
  updater.bot.setWebhook("https://shrimad-bhagwat-gita-bot.herokuapp.com/" + TOKEN)
  #updater.start_polling()
  updater.idle()
if __name__ == '__main__':
  main()

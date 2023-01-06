import logging
import os
import re
import json
from web3 import Web3
from flask import Flask, request
from datetime import date
import telebot
from telebot import types
from dotenv import load_dotenv
load_dotenv()



# Logging Setup
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)

TOKEN = os.getenv('TOKEN')

cwd = os.getcwd()

DEBUG = True
SERVER_URL = os.getenv("SERVER_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

WEB3_API_KEY = os.getenv("WEB3_API_KEY")

NODE_PROVIDER = os.getenv("NODE_PROVIDER")

web3_client = Web3(Web3.HTTPProvider(NODE_PROVIDER))
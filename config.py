import logging
import os
import re
import json
from web3 import Web3
from eth_abi import encode_abi, decode_abi
from flask import Flask, request
from datetime import date
import telebot
from telebot import types
import cryptocompare as cc
import threading
from multiprocessing import Manager
from multiprocessing import Event
from multiprocessing import set_start_method, Process, Semaphore, active_children
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from dotenv import load_dotenv
load_dotenv()

# set_start_method('fork')
# pool = multiprocessing.Pool(10)

executor = ProcessPoolExecutor(max_workers=10)


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

active_pools = {}


class SemaphoreContext:
    def __init__(self, semaphore):
        self.semaphore = semaphore

    def __enter__(self):
        self.semaphore.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.semaphore.release()


sem = Semaphore(1)

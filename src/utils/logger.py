import logging

class Logger:
    def __init__(self):
        logging.basicConfig(filename='debate.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    def log(self, message):
        logging.info(message)
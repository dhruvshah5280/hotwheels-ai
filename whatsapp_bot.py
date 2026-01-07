import pywhatkit as kit
from ai_engine import ask_ai

def send(msg):
    kit.sendwhatmsg_instantly("+917304313872", msg, 15)

import speech_recognition
import pyttsx3
from datetime import date
import webbrowser
from pyspectator.computer import Computer

computer = Computer()
computer.os
computer.python_version
computer.processor.name

robot_ear = speech_recognition.Recognizer()
robot_mouth = pyttsx3.init()
robot_brain =""


with speech_recognition.Microphone() as mic:
     print("Robot: I'm Listening")
     audio = robot_ear.listen(mic)

print("Robot...") 

try:
    you = robot_ear.recognize_google(audio)
except:
     you = ""

print("you: " + you)

if you == "":
   robot_brain = "I can't hear you, try again"
elif you == "today":
     today = date.today()
     robot_brain = today.strftime("%B %d, %Y")
     print("robot_brain:" + robot_brain)
elif you == "open":
     webbrowser.open_new_tab('https://fireant.vn/charts')
     webbrowser.open_new_tab('https://fialda.com/thong-ke-thi-truong/tong-hop')
     webbrowser.open_new_tab('https://fialda.com/phan-tich-ky-thuat')
     webbrowser.open_new_tab('https://trade.vndirect.com.vn/chung-khoan/danh-muc')
     webbrowser.open_new_tab('https://www.binance.com/vi/my/wallet/account/main')
     webbrowser.open_new_tab('https://www.binance.com/vi/trade/BTC_USDT?layout=pro&type=spot')
     print("robot_brain: open_successful")
     robot_mouth.say("open_successful")
     robot_mouth.runAndWait()
     exit()
elif you =="information":
     print(computer.os)
     print(computer.python_version)
     print(computer.processor.name)
     robot_brain = "get information successful"

robot_mouth.say(robot_brain)
robot_mouth.runAndWait()
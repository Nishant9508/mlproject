import speech_recognition as sr
import pyttsx3
import datetime
import time
import wikipedia
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes
from wikipedia.wikipedia import search
from bs4 import BeautifulSoup
import requests
from PIL import Image
import wolframalpha
from sys import platform
from GoogleNews import GoogleNews
import cv2


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

newVoiceRate = 180
engine.setProperty('rate', newVoiceRate)

googlenews=GoogleNews()

def computational_intelligence(question):
	try:
		client = wolframalpha.Client("GWL394-2JYHWK299Q")
		answer = client.query(question)
		answer = next(answer.results).text
		print(answer)
		return answer
	except:
		speak("Sorry sir I couldn't fetch your question's answer. Please try again ")
		return None


def speak(audio):
	engine.say(audio)
	engine.runAndWait()


def wishme():
	speak("Welcome")
	hour = datetime.datetime.now().hour

	if hour >= 6 and hour <= 12:
		speak("Good Morning Sir")
	elif hour > 12 and hour <= 16:
		speak("Good Afternoon Sir")
	elif hour > 16 and hour < 21:
		speak("Good Evening Sir")
	else:
		speak("Good to See you Sir")

	speak("I am Chin two, your personal voice assistant. How may i help you ?")


def takeCommand():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		r.pause_threshold = 1
		audio = r.listen(source)

	try:
		print("Recognizing...")
		query = r.recognize_google(audio, language='en=in')
		print("You said : " + query)
	except Exception as e:
		print(e)
		speak("say that again please")
		return "None"

	return query


def time1():
	time1 = datetime.datetime.now().strftime("%I:%M:%S")
	speak("The time right now is")
	speak(time1)


def date():
	year = int(datetime.datetime.now().year)
	month = int(datetime.datetime.now().month)
	date = int(datetime.datetime.now().day)
	speak("Today's date is")
	speak(date)
	speak(month)
	speak(year)


def cpu():
	usage = str(psutil.cpu_percent())
	speak("Cpu is at "+usage)

	battery = psutil.sensors_battery()
	speak("Battery is at ")
	speak(battery.percent)
	speak("Percent")


def screenshot():
	img = pyautogui.screenshot()
	img.save(r'')                                                                       


def jokes():
	speak(pyjokes.get_joke())


def myclass():
	time.sleep(2)
	wb.open_new('https://myclass.lpu.in/')

	time.sleep(4)

	pyautogui.press("tab")
	pyautogui.typewrite('11911240')
	pyautogui.press("tab")
	time.sleep(1)
	pyautogui.typewrite('')      
	pyautogui.press("enter")
	time.sleep(3)

	for i in range(5):
		pyautogui.press("tab")
	pyautogui.press("enter")
	time.sleep(2)
  
def Temperature(query):
	city = query.split("in", 1)
	data = BeautifulSoup(requests.get(
		f"https://www.google.com/search?q=weather+in+{city [1]}").text, "html.parser")
	region = data.find("span", class_="BNeawe tAd8D AP7Wnd")
	temp = data.find("div", class_="BNeawe iBp4i AP7Wnd").text
	day = data.find("div", class_="BNeawe tAd8D AP7Wnd").text
	weather = day.split("m", 1)
	temperature = temp.split("C", 1)
	speak("Its Currently"+weather[1]+" and " +
		  temperature[0]+"celcuis"+"in"+region.text)
	print("Its Currently"+weather[1]+" and " + temperature[0]+" celcuis "+"in "+region.text)


def TaskExecution():
	cv2.destroyAllWindows()
	speak("verification Successful")
  
							
	wishme()

	while True:
		query = takeCommand().lower()
		print(query)

		if "time" in query:
			time1()

		elif "date" in query:
			date()

		elif "cpu" in query:
			cpu()

		elif "joke" in query:
			jokes()

		elif ("class" in query) or ("myclass" in query) or ("my class" in query):
			speak("Opening My class")
			myclass()

		elif 'search' in query:
			speak('Searching Wikipedia...')
			query = query.replace("wikipedia", "")
			results = wikipedia.summary(query, sentences=2)
			speak("According to Wikipedia")
			print(results)
			speak(results)
			
		elif ("chrome" in query) or ("google" in query):
			wb.open_new('https://google.com/')

		elif "play songs" in query:
			songs_dir ='C:\\Users\\ASUS\\Documents\\Dev\\Ml_assignment\\Songs'                              
			songs = os.listdir(songs_dir)
			os.startfile(os.path.join(songs_dir,songs[0]))

		elif "remember that" in query:
			speak("What should i remember?")
			data = takeCommand()
			speak("You said me to remember,"+data)
			remember = open("data.txt", "w")
			remember.write(data)
			remember.close()

		elif ("do you remember" in query) or ("do you remember anything" in query):
			remember = open("data.txt", "r")
			speak("you told me to remember that  " + remember.read())

		elif (" go offline" in query) or ("off" in query):
			speak("Bye and Have a great Day Sir, Alex now going offline")
			quit()

		elif "shutdown" in query:
			os.system("shutdown /s /t 1")

		elif "restart" in query:
			os.system("shutdown /r /t 1")

		elif "temperature" in query:
			Temperature(query)
		
		elif 'open youtube' in query:      
			wb.open("youtube.com")
		
		elif 'open google' in query:
			wb.open("google.com")
		
		elif 'open stackoverflow' in query:
			wb.open("stackoverflow.com")
			  
		
		elif "switch the window" in query or "switch window" in query:
			speak("Okay sir, Switching the window")
			pyautogui.keyDown("alt")
			pyautogui.press("tab")
			time.sleep(1)
			pyautogui.keyUp("alt")
		 
		elif "ip address" in query:
			ip = requests.get('https://api.ipify.org').text
			print(ip)
			speak(f"Your ip address is {ip}")

		elif "take screenshot" in query or "take a screenshot" in query or "capture the screen" in query:
			speak("By what name do you want to save the screenshot?")
			name =takeCommand()
			speak("Alright sir, taking the screenshot")
			img = pyautogui.screenshot()
			name = f"{name}.png"
			img.save(name)
			speak("The screenshot has been succesfully captured")
			
		elif "show me the screenshot" in query:
			try:
				img = Image.open('C:\\Users\\ASUS\\Documents\\Dev\\Ml_assignment\\'+name)                     
				img.show(img)
				speak("Here it is sir")
				time.sleep(2)

			except IOError:
				speak("Sorry sir, I am unable to display the screenshot")    
		  
		elif "what is" in query or "who is" in query:
			question = query
			answer = computational_intelligence(question)
			speak(answer)

		elif 'your master' in query:
			if platform == "win64" or "darwin":
				speak('Shahnawaz and Nishant are my masters. They created me couple of days ago')
				
		elif 'headlines' in query:
			speak("getting news for you")
			googlenews.get_news("todays news")
			googlenews.result()
			a=googlenews.gettext()
			print(*a[1:5],sep=',')
			speak(a[1:5])

		elif 'tech news' in query:
			speak("getting news for you")
			googlenews.get_news("Latest tech news")
			googlenews.result()
			a=googlenews.gettext()
			print(*a[1:5],sep=',')
			speak(a[1:5])
		
		elif 'politics' in query:
			speak("getting news for you")
			googlenews.get_news("Latest politics news")
			googlenews.result()
			a=googlenews.gettext()
			print(*a[1:5],sep=',')
			speak(a[1:5])
			
if __name__== "__main__":

	recognizer = cv2.face.LBPHFaceRecognizer_create() 
	recognizer.read('C:\\Users\\ASUS\\Documents\\Dev\\Ml_assignment\\trainer.yml')                                      
	cascadePath = "C:\\Users\\ASUS\\Documents\\Dev\\Ml_assignment\\haarcascade_frontalface_default.xml"                 
	faceCascade = cv2.CascadeClassifier(cascadePath) 

	font = cv2.FONT_HERSHEY_SIMPLEX 

	id = 2 

	names = ['','Nishant']                             


	cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
	cam.set(3, 640) 
	cam.set(4, 480) 

	minW = 0.1*cam.get(3)
	minH = 0.1*cam.get(4)

	while True:

		ret, img =cam.read() 

		converted_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  

		faces = faceCascade.detectMultiScale( 
			converted_image,
			scaleFactor = 1.2,
			minNeighbors = 5,
			minSize = (int(minW), int(minH)),
		   )

		for(x,y,w,h) in faces:

			cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2) 

			id, accuracy = recognizer.predict(converted_image[y:y+h,x:x+w]) 

			if (accuracy < 100):
				id = names[id]
				accuracy = "  {0}%".format(round(100 - accuracy))
				TaskExecution()

			else:
				id = "unknown"
				accuracy = "  {0}%".format(round(100 - accuracy))
				speak("not authorized")
				quit()
		
		cv2.imshow('camera',img)
		k = cv2.waitKey(100) & 0xff 
		if k == 27:
			break

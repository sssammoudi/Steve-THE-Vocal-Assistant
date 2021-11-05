#the libraries needed for the project
import speech_recognition as sr
import pyttsx3
import pyautogui as pyg
import webbrowser
import time
import datetime
import subprocess
from googletrans import Translator
import wikipedia
import smtplib
import logging
from playsound import playsound
import requests

#show the login
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Admin logged in')

#language dict
language_dict = {
  'arabic' : 'ar', 
  'chinese' : 'zh-CN', 
  'danish' : 'da', 
  'dutch' : 'nl', 
  'english' : 'en', 
  'french' : 'fr', 
  'german' : 'de', 
  'greek' : 'el', 
  'hindi' : 'hi', 
  'indonesian' : 'id', 
  'italian' : 'it', 
  'japanese' : 'ja', 
  'korean' : 'ko', 
  'latin' : 'la', 
  'norwegian' : 'no', 
  'russian' : 'ru', 
  'spanish' : 'es', 
  'vietnamese' : 'vi'
  } 

#initialize the translator
translator = Translator()

#read voice
speech = sr.Recognizer()

#activate voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')

az = ''
qsd = str(input('Which language shall I speak ? \nEnter: '))
def english() :  
  global az
  engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')
  az = 1

def french() :
  global az
  engine.setProperty('voice', 'com.apple.speech.synthesis.voice.amelie.premium')
  az = 2

if 'english' == qsd :
  english()
elif 'french' == qsd :
  french()
else :
  exit()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate)

time.sleep(3)

#for saying the text
def speak_text(enter) :
  engine.say(enter)
  print(enter)
  engine.runAndWait()

#to read the voice
def read_voice() :
  text = ''

  with sr.Microphone() as source :
    audio = speech.listen(source = source, timeout = 7,phrase_time_limit = 5)

  try :
    if az == 1 :
      text = speech.recognize_google(audio, language = 'en_US').lower()
    elif az == 2 :
      text = speech.recognize_google(audio, language = 'fr-FR').lower()

  except sr.UnknownValueError :
    pass
  except sr.WaitTimeoutError :
    pass
  except sr.RequestError :
    speak_text('conection lost')
    pass

  return text

#shut down
def shut_down() :
  pyg.moveTo(x=32, y=3)
  time.sleep(0.5)
  pyg.click(x=32, y=3)
  time.sleep(0.5)
  pyg.moveTo(x=52, y=176)
  time.sleep(0.5)
  pyg.click(x=52, y=176)

# send a mail
def sendEmail(to, content) :
  email_user = 'sssammoudi@gmail.com'
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(email_user, 'SaaD2006')

  server.sendmail(email_user, to, content)
  server.quit()

#for the actual time
def times() :
  current_time = str(time.strftime('%H:%M'))
  speak_text(current_time)

#for the actual date
def date() :
  current_date = datetime.date.today().strftime('%A-%B-%d-20%y')
  speak_text(current_date)

#take screen shots
def screen_shots(voice_note) :
  time.sleep(2)
  pyg.screenshot('/Users/mac/screen_shots/'+voice_note+'.png')

def translate(text) :
  for key, value in language_dict.items() :
    if key in text :
      split_text = text.split(' ')
      list_remove = []
      list_remove.append(split_text[0])
      list_remove.append(split_text[-1])
      list_remove.append(split_text[-2])
      for word in list_remove :
        text = text.replace(word, '')
        translation = translator.translate(text, dest=value).text
      print(translation)
      speak_text('I have translated the phrase')

def left() :
  pyg.press('left')

def right() :
  pyg.press('right')

if az == 1 :  
  speak_text('Welcome I am Steve your personnal desktop assistant.')
elif az == 2 :
  speak_text('Je suis Amélie votre assistante personnel') 

#the main
while True :
  if az == 1 :
    print('\nlistening...')

    voice_note = read_voice()
    print ('command is :{}'.format(voice_note))

    #change language
    if 'speak french' in voice_note :
      french()
      speak_text('langue changer')
    
    #commun functionnalities
    #shut down the laptop and quit(only macs)
    elif 'shut down the laptop and quit' in voice_note:
      shut_down()
      break

    elif 'change your voice' == voice_note :
      speak_text('man or woman')
      print('listening...')
      z = read_voice()
      if 'woman' in z :
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Victoria')
        speak_text('I am Victoria')
      elif 'man' in z :
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')
        speak_text('I am Steve')
      print(z)
      continue
    
    #press left arrow
    elif 'left' == voice_note :
      left()
      continue

    #press right arrow
    elif 'right' == voice_note :
      right()
      continue

    #send a mail(public)
    elif 'send email' in voice_note :
      speak_text('To who should I send the message')
      receiver = str(input('enter :'))
      speak_text('What will I write')
      print('listening...')
      content = read_voice()
      print(content)
      speak_text('Are you sure of that ?')
      print('listening...')
      answer = read_voice()
      if 'yes' in answer :
        sendEmail(receiver, content)
        speak_text('Email sent')
        continue

      elif 'no' in answer :
        speak_text('the email will not be sent')
        continue
    
    #greeting(public)
    elif 'hello' in  voice_note : 
      speak_text('How can I help you ?')
      continue
    
    #Bye(public)
    elif 'bye' in voice_note or 'see you' in voice_note :
      speak_text('Bye mister')
      break
    
    #give the time(public)
    elif 'the time' in voice_note :
      times()
      continue

    #give the date(public)
    elif 'the date' in voice_note :
      date()
      continue

    #take a screenshot(public)
    elif 'screenshot' in voice_note :
      speak_text('wait a second')
      screen_shots('{}.png'.format(voice_note.replace('screenshot named ', '')))
      speak_text('screenshot took.')
      continue
    
    #what are the languages that can be translated to(public)
    elif 'give me the languages of the translator' in voice_note :
      languages = language_dict.keys()
      speak_text('{}'.format(languages))
      print(languages)
      continue
    
    #translating words or phrases(public)
    elif 'translate' in voice_note :
      text = voice_note
      translate(text)
      continue
    
    #openning my calculator(only my mac)
    elif 'my calculator' in voice_note :
      file_to_show = '/Applications/Steve.app'
      subprocess.call(["open", "-R", file_to_show])
      speak_text('Click...')
      time.sleep(3)
      pyg.typewrite('/usr/local/bin/python3 /Users/mac/python/projects/calculator/calculator.py')
      pyg.typewrite(['enter'])
      speak_text('Opened')
      continue
    
    #opening my games(only my mac)
    elif 'my games' in voice_note :
      speak_text('Wich game should I open ?')
      game = read_voice()
      if 'xo' in game or 'XO' in game :
        file_to_show = '/Applications/Steve.app'
        subprocess.call(["open", "-R", file_to_show])
        speak_text('Click...')
        time.sleep(3)
        pyg.typewrite('/usr/local/bin/python3 /Users/mac/python/projects/Tic_Tac_Toe/Tic_Tac_Toe.py')
        pyg.typewrite(['enter'])
        speak_text('Opened')
        continue
            
      else :
        speak_text('Any of the games you created is named {}'.format(game))
        continue

    #my to do list(only my mac)
    elif 'my to do list' in voice_note :
      file_to_show = '/Applications/Steve.app'
      subprocess.call(["open", "-R", file_to_show])
      speak_text('Click...')
      time.sleep(3)
      pyg.typewrite('/usr/local/bin/python3 /Users/mac/python/projects/Todolist/TodoList.py')
      pyg.typewrite(['enter'])
      speak_text('Opened')
      continue
    
    #tell a joke
    elif 'tell me a joke' in voice_note:
      res = requests.get(
            'https://icanhazdadjoke.com/',
             headers={"Accept":"application/json"}
            )
      if res.status_code == requests.codes.ok:
        speak_text(str(res.json()['joke']))
      else:
        speak_text('oops!I ran out of jokes')

    #play songs
    elif 'play songs' == voice_note :
      subprocess.call(["open", "-R", '/python/projets/Steve/songs'])

    #openning the applications(only macs)
    elif 'open the application' in voice_note :
      file_to_show = "/Applications/{}.app".format(voice_note.replace('open the application ', ''))
      subprocess.call(["open", "-R", file_to_show])
      continue

    #openning facebook(public)
    elif 'open facebook' in voice_note :
      speak_text('I am opening facebook')
      webbrowser.open('https://www.facebook.com/?locale=fr_FR')
      continue
    
    #openning the finder(only my mac)
    elif 'finder' in voice_note :
      speak_text('I am opening finder')
      pyg.moveTo(x=166, y=788, duration = 1)
      pyg.click(x=166, y=788)
      continue

    #openning Instagram(public)
    elif 'open instagram' in voice_note :
      speak_text('I am opening instagram')
      webbrowser.open('https://www.instagram.com')
      continue

    #openning Youtube(public)
    elif 'open youtube' in voice_note :
      speak_text('I am opening youtube')
      webbrowser.open('https://www.youtube.com/?gl=FR&hl=fr')
      continue

    #asking for the creator(public (unchangeable))
    elif 'who is your creator' in voice_note :
      speak_text('It\'s my master Saad Sammoudi')
      continue

    #making a ressearch that contains Wh questions(public)
    elif 'what' in voice_note or 'who' in voice_note or 'why' in voice_note or 'where' in voice_note or 'how' in voice_note or 'which' in voice_note :
      speak_text('I am searching...')
      webbrowser.open('https://www.google.com/search?q={}'.format(voice_note))
      continue

    #making a ressearch that doesn't contain Wh questions(public)
    elif 'search for' in voice_note :
      speak_text('I am searching...')
      webbrowser.open('https://www.google.com/search?q={}'.format(voice_note.replace('search for ', '')))
      continue

    #searching on wikipédia(public)
    elif 'search on wikipedia' in voice_note :
      speak_text('I am searching ...')
      result = wikipedia.summary('{}'.format(voice_note.replace('search on Wikipedia for', '')), sentences = 3)
      speak_text('Acording to Wikipedia '+result)
      print(result)
      continue

    #thanking public
    elif 'thank you' in voice_note :
      speak_text('you\'re welcome')
      continue
    
    #shuting down(only macs)
    elif 'shut down' in voice_note :
      shut_down()
      continue
    
    #openning the mac if we didn't quit(personnal)
    elif 'steve gates' in voice_note :
      speak_text('wait...')
      pyg.typewrite('2006') 
      pyg.typewrite(['enter'])
      speak_text('laptop opened')
      continue

  if az == 2 :
    print('\nJ\'écoute...')

    voice_note = read_voice()
    print ('la commande est :{}'.format(voice_note))

    if '' == voice_note :
      pass
    
    #change voice
    elif 'change de voix' == voice_note :
      speak_text('homme ou femme')
      print('J\'écoute...')
      z = read_voice()
      if 'femme' in z :
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.amelie.premium')
        speak_text('je suis Amélie')
      elif 'homme' in z :
        engine.setProperty('voice', 'com.apple.speech.synthesis.voice.thomas')
        speak_text('Je suis Albert')
      print(z)
      continue

    #change language
    elif 'parle anglais' in voice_note :
      print('Ok')
      english()

    #birthday program(personnal)
    elif 'rashid' in voice_note :
      speak_text('According to his great family; Rachid is a great man, a great father, a great husband and a great friend. Those few words to tell about a man that is really important. Today is the birthday of this man. So... I am telling him in the name of his family.')
      playsound('/Users/mac/python/projects/Steve/happy_birthday/happy_birthday.mp3')
      continue
    
    #commun functionnalities
    #shut down the laptop and quit(only macs)
    elif 'éteins l\'ordinateur est quitte' in voice_note:
      shut_down()
      break
    
    #press left arrow
    elif 'gauche' == voice_note :
      left()
      continue

    #press right arrow
    elif 'droite' == voice_note :
      right()
      continue

    #send a mail(public)
    elif 'envoie un email' in voice_note :
      speak_text('à qui dois-je envoyer un message?')
      receiver = str(input('entrer :'))
      speak_text('Que dois-je écrire?')
      print('J\'écoute...')
      content = read_voice()
      print(content)
      speak_text('Vous-étes sur de ça?')
      print('J\'écoute...')
      answer = read_voice()
      if 'oui' in answer :
        sendEmail(receiver, content)
        speak_text('Email envoyer')
        continue

      elif 'non' in answer :
        speak_text('l\'Email ne sera pas envoyer')
        continue
    
    #greeting(public)
    elif 'bonjour' in  voice_note : 
      speak_text('Comment puis-je vous aider?')
      continue
    
    #Bye(public)
    elif 'au revoir' in voice_note or 'à plus tard' in voice_note :
      speak_text('au revoir')
      break
    
    #give the time(public)
    elif 'le temps' in voice_note :
      times()
      continue

    #give the date(public)
    elif 'la date' in voice_note :
      date()
      continue

    #take a screenshot(public)
    elif 'screenshot' in voice_note :
      speak_text('attendez une second')
      screen_shots('{}.png'.format(voice_note.replace('screenshot appelée', '')))
      speak_text('screenshot pris.')
      continue
    
    #what are the languages that can be translated to(public)
    elif 'donne moi les langues du traducteur' in voice_note :
      languages = language_dict.keys()
      speak_text('{}'.format(languages))
      print(languages)
      continue
    
    #translating words or phrases(public)
    elif 'traduis' in voice_note :
      text = voice_note
      translate(text)
      continue
    
    #openning my calculator(only my mac)
    elif 'ma calculatrice' in voice_note :
      file_to_show = '/Applications/Steve.app'
      subprocess.call(["open", "-R", file_to_show])
      speak_text('Click...')
      time.sleep(3)
      pyg.typewrite('/usr/local/bin/python3 /Users/mac/python/projects/calculator/calculator.py')
      pyg.typewrite(['enter'])
      speak_text('Ouvèr')
      continue
    
    #opening my games(only my mac)
    elif 'mes jeux' in voice_note :
      speak_text('Quelle jeu dois-je ouvrir?')
      game = read_voice()
      if 'xo' in game or 'XO' in game :
        file_to_show = '/Applications/Steve.app'
        subprocess.call(["open", "-R", file_to_show])
        speak_text('Click...')
        time.sleep(3)
        pyg.typewrite('/usr/local/bin/python3 /Users/mac/python/projects/Tic_Tac_Toe/Tic_Tac_Toe.py')
        pyg.typewrite(['enter'])
        speak_text('Ouvère')
        continue
            
      else :
        speak_text('Aucun de vos jeux ne s\'appelle {}'.format(game))
        continue

    #my to do list(only my mac)
    elif 'ma liste' in voice_note :
      file_to_show = '/Applications/Steve.app'
      subprocess.call(["open", "-R", file_to_show])
      speak_text('Click...')
      time.sleep(3)
      pyg.typewrite('/usr/local/bin/python3 /Users/mac/python/projects/Todolist/TodoList.py')
      pyg.typewrite(['enter'])
      speak_text('Ouvère')
      continue

    elif 'dis-moi une blague' in voice_note:
      res = requests.get(
            'https://icanhazdadjoke.com/',
             headers={"Accept":"application/json"}
            )
      if res.status_code == requests.codes.ok:
        speak_text(str(res.json()['joke']))
      else:
        speak_text('oops!Je n\'est plus de blague')

    #play songs
    elif 'jouez de la musique' == voice_note :
      subprocess.call(["open", "-R", '/python/projets/Steve/songs'])

    #openning the applications(only macs)
    elif 'ouvre l\' application' in voice_note :
      file_to_show = "/Applications/{}.app".format(voice_note.replace('ouvrez les applications', ''))
      subprocess.call(["open", "-R", file_to_show])
      continue

    #openning facebook(public)
    elif 'ouvre facebook' in voice_note :
      speak_text('J\'ouvre facebook')
      webbrowser.open('https://www.facebook.com/?locale=fr_FR')
      continue
    
    #openning the finder(only my mac)
    elif 'finder' in voice_note :
      speak_text('J\'ouvre finder')
      pyg.moveTo(x=166, y=788, duration = 1)
      pyg.click(x=166, y=788)
      continue

    #openning Instagram(public)
    elif 'ouvre instagram' in voice_note :
      speak_text('I am opening instagram')
      webbrowser.open('https://www.instagram.com')
      continue

    #openning Youtube(public)
    elif 'ouvre youtube' in voice_note :
      speak_text('J\'ouvre youtube')
      webbrowser.open('https://www.youtube.com/?gl=FR&hl=fr')
      continue

    #asking for the creator(public (unchangeable))
    elif 'qui est ton createur' in voice_note :
      speak_text('c\'est mon maitre Saad Sammoudi')
      continue

    #making a ressearch that contains Wh questions(public)
    elif 'quoi' in voice_note or 'qui' in voice_note or 'pourquoi' in voice_note or 'ou' in voice_note or 'comment' in voice_note or 'quelle' in voice_note :
      speak_text('Je cherche...')
      webbrowser.open('https://www.google.com/search?q={}'.format(voice_note))
      continue

    #making a ressearch that doesn't contain Wh questions(public)
    elif 'cherche' in voice_note :
      speak_text('Je cherche...')
      webbrowser.open('https://www.google.com/search?q={}'.format(voice_note.replace('cherche ', '')))
      continue

    #searching on wikipédia(public)
    elif 'cherche sur wikipedia' in voice_note :
      speak_text('Je cherche...')
      result = wikipedia.summary('{}'.format(voice_note.replace('cherche sur wikipedia ', '')), sentences = 3)
      speak_text('d\'après wikipédia '+result)
      print(result)
      continue

    #thanking public
    elif 'merci' in voice_note :
      speak_text('De rien')
      continue
    
    #shuting down(only macs)
    elif 'éteins l\'ordinateur' in voice_note :
      shut_down()
      continue
    
    #openning the mac if we didn't quit(personnal)
    elif 'ordinateur' in voice_note :
      speak_text('attends...')
      pyg.typewrite('2006') 
      pyg.typewrite(['enter'])
      speak_text('ordinateur ouvère')
      continue

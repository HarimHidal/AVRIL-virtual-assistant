# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 11:00:43 2022

@author: Harim
"""

#### IMPORTS 

import speech_recognition as sr
import pyttsx3 as tts

from pywhatkit import playonyt, search as googlesearch
import webbrowser as wb
from os import startfile, path, walk
from datetime import datetime
from random import choice
from pyautogui import press, write
from time import sleep
from pyperclip import copy

#### SKILLS' FUNCTIONS 

def play(music, verbose=True):
    if 'en youtube' in music:
        music = music.replace('en youtube', '').strip()
        if verbose: print('Reproduciendo ' + music + ' en YouTube')
        playonyt(music)
        talk('Reproduciendo ' + music + ' en YouTube')
    else:
        music = music.replace('en spotify', '').strip()
        if verbose: print('Reproduciendo ' + music + ' en Spotify')
        wb.open('https://open.spotify.com/search/' + music)
        talk('Reproduciendo ' + music + ' en Spotify')
    
def searching(request, verbose=True):
    if 'en wikipedia' in request:
        request = request.replace('en wikipedia', '').strip()
        if verbose: print('Resultados para ' + request)
        wb.open('https://es.wikipedia.org/wiki/' + request)    
    else:
        request = request.replace('en google', '').strip()
        if verbose: print('Resultados para ' + request)
        googlesearch(request)
    talk('Estos son los resultados para ' + request)
    
def opening(request, verbose=True):
    searching_path = configs['srch-path']
    if 'la carpeta' in request or 'el folder' in request:
        request = request.replace('la carpeta', '').strip()
        request = request.replace('el folder', '').strip()
        dir_path = find(request, searching_path, directory=True)
        if verbose: print('Abriendo carpeta ' + dir_path)
        startfile(dir_path)        
        talk('Abriendo carpeta ' + path.basename(dir_path))
    elif 'el archivo' in request or 'el documento' in request:
        request = request.replace('el archivo', '').strip()
        request = request.replace('el documento', '').strip()
        file_path = find(request, searching_path, file=True)
        if verbose: print('Abriendo archivo ' + file_path)
        startfile(file_path)
        talk('Abriendo el archivo ' + path.splitext(path.basename(file_path))[0])
    elif 'en spotify' in request:
        play(request, verbose)
    elif 'temporizador' in request:
        startimer(request, verbose)
    else:
        for site in sites:
            if site in request:
                if verbose: print('Abriendo ' + site)
                wb.open(sites[site])
                talk('Abriendo la página de ' + site)
                return
        for app in apps:
            if app in request: 
                if verbose: print('Abriendo ' + app)
                startfile(apps[app])
                talk('Abriendo la aplicación de ' + app)
                return
        if verbose: print('Lo siento {}, todavía no puedo abrir {}'.format(configs['your-name'], request))
        talk('Lo siento {}, todavía no puedo abrir {}'.format(configs['your-name'], request))

def greeting(text, verbose=True):
    msg = []
    hello = ['Hola', 'Quiubo', 'Qué tal', 'Qué onda mi', 'Tanto sin escucharte', 
             'Qué gusto escucharte']
    msg.append(choice(hello))
    msg.append(configs['your-name'] + ',')
    current_hour = int(datetime.now().strftime("%H"))
    if current_hour >= 0 and current_hour < 13:
        msg.append('buenos días!')
    elif current_hour >= 13 and current_hour < 19:
        msg.append('buenas tardes!')
    else:
        msg.append('buenas noches!')
    if verbose: print(' '.join(msg), end=' ')
    talk(' '.join(msg))
    
def gladly(text, verbose=True):
    happily = ['Con mucho gusto', 'En seguida', 'Claro que sí', 'Ya estoy en eso', 'De volón pimpón',
               'Será un placer', 'No hay problema', 'Por supuesto', 'Desde luego', 'Por su pollo']
    msg = choice(happily)
    if verbose: print(msg, end='. ')
    talk(msg)

def goodbye(text, verbose=True):
    msg = []
    bye = ['Hasta pronto', 'Nos vemos', 'Cuídate', 'Adiós,', 'Fue un gusto',
           'Que tengas un bonito día', 'Te echaré de menos', 'Hasta lueguito', 
           'Aquí estaré cuando regreses', 'Hablamos luego', 'Excelente resto del día']
    msg.append(choice(bye))
    msg.append( ' ' + configs['your-name'] + '!')
    if verbose: print(' '.join(msg))
    talk(' '.join(msg))
    global active 
    active = False
    
def tellme(request, verbose=True):
    if 'hora' in request:
        if verbose: print('En este momento son las ' + datetime.now().strftime("%I %M %p"))
        talk('En este momento son las ' + datetime.now().strftime("%I %M %p"))
    elif 'fecha' in request:
        month = {1:'enero', 2:'febrero', 3:"marzo", 4:"abril", 5:"mayo", 6:"junio", 7:"julio", 8:"agosto", 9:"septiembre", 10:"octubre", 11:"noviembre", 12:"diciembre"}
        if verbose: print('Hoy es el ' + str(datetime.now().day) + ' de ' + month[int(datetime.now().month)] + ' de ' + str(datetime.now().year))
        talk('Hoy es el ' + str(datetime.now().day) + ' de ' + month[int(datetime.now().month)] + ' de ' + str(datetime.now().year))
    elif 'tu nombre' in request or 'te llamas' in request or 'sobre ti' in request:
        msg = 'Soy una Asistente Virtual Reducida con Interfaz Limitada. Pero tú puedes llamarme '
        name = configs['asis-name']
        if verbose: print(msg + name)
        talk(msg + name)
    elif 'mi nombre' in request or 'me llamo' in request:
        msg = 'Si mis circuitos no se equivocan, tu nombre es {}'.format(configs['your-name'])
        if verbose: print(msg)
        talk(msg)
    elif 'un chiste' in request:
        joke = configs['joke-lst1'].split('; ')
        [ joke.append(j) for j in configs['joke-lst2'].split('; ') ]
        msg = choice(joke)
        if verbose: print(msg)
        talk(msg)
    elif 'algo' in request:
        if 'gracioso' in request or 'chistoso' in request:
            funny = configs['fnny-list'].split('; ')
            msg = choice(funny)
            if verbose: print(msg)
            talk(msg)            
        else:
            smtg = configs['smtg-lst1'].split('; ')
            [ smtg.append(x) for x in configs['smtg-lst2'].split('; ') ]
            msg = choice(smtg)
            if verbose: print(msg)
            talk(msg)                 
    else:
        if verbose: print('Lo siento {}, todavía no puedo decirte {}'.format(configs['your-name'], request))
        talk('Lo siento {}, todavía no puedo decirte {}'.format(configs['your-name'], request))
        
def startimer(request, verbose=True):
    time = [ int(word) for word in request.split() if word.isdigit() ]
    if 'segundos' in request and time != []:
        wb.open('https://reloj-alarma.es/temporizador-' + str(time[0]) + '-segundos')
        if verbose: print('Estableciendo temporizador por ' + str(time[0]) + ' segundos')
        talk('Estableciendo temporizador por ' + str(time[0]) + ' segundos')
    elif 'minutos' in request and time != []:
        wb.open('https://reloj-alarma.es/temporizador-' + str(time[0]) + '-minutos')
        if verbose: print('Estableciendo temporizador por ' + str(time[0]) + ' minutos')
        talk('Estableciendo temporizador por ' + str(time[0]) + ' minutos')
    else:
        if verbose: print('Lo siento, no puede iniciar el temporizador.')
        talk('Lo siento, no puede iniciar el temporizador.')

def writing(request, verbose=True):
    if 'en una nota' in request:
        request = request.replace('en una nota', '').strip()
        startfile(apps['notas'])
        sleep(1)
        press(['pagedown', 'end', 'enter'])
        write(request)
        if verbose: print('Listo! Ya quedó anotado como me lo pediste')
        talk('Listo {}! Ya quedó anotado como me lo pediste'.format(configs['your-name']))
    elif 'en whatsapp' in request:
        request = request.replace('en whatsapp', '').strip()
        wb.open('https://web.whatsapp.com/send?phone={}&text={}'.format(configs['cell-numb'], request))
        if verbose: print('Listo! Ya quedó escrito como me lo pediste')
        talk('Listo {}! Ya quedó escrito como me lo pediste'.format(configs['your-name']))
    else:
        copy(request)
        if verbose: print('Listo! Guardé tu dictado en el portapapeles')
        talk('Listo {}! Guardé tu dictado en el portapapeles'.format(configs['your-name']))
    
def helpme(request, verbose=True):
    if verbose: print('No te preocupes {}, aquí están las palabras clave que puedes usar.'.format(configs['your-name']))
    talk('No te preocupes {}, aquí están las palabras clave que puedes usar.'.format(configs['your-name']))
    msg = []
    for skill in skills:
        if type(skill) is not str: # then there are several key word
            msg.append(skill[0])
        else:
            msg.append(skill)
    if verbose: print(', '.join(msg))
    talk(', '.join(msg))
    print('''
() --> requerido
[] --> opcional
| ---> uno u otro

HOLA [ instrucción ]
[ instrucción ] POR FAVOR
AYUDA
GRACIAS | MUCHAS GRACIAS
[ instrucción ] ADIOS | BYE | AUTODESTRÚYETE

QUIERO ESCUCHAR | REPRODUCE ( canción | playlist | artista ) [ en YouTube | en Spotify ]
BUSCA | GOOGLEA ( contenido a buscar ) [ en Wikipedia  | en Google ]
ABRE | INICIA ( aplicación | sitio web ) | ( la carpeta | el archivo ) ( nombre ) 
ABRE | INICIA ( canción | playlist | artista )  EN SPOTIFY | TEMPORIZADOR ( # segundos | # minutos )
ESCRIBE | ANOTA [ en una Nota | en WhatsApp ] ( dictado )
TEMPORIZADOR ( # segundos | # minutos )
DIME | CUÉNTAME ( hora | fecha | tu nombre | mi nombre | un chiste | algo [ gracioso | chistoso ] )
          ''')
    
def urwelcome(request, verbose=True):
    welcome = ['No hay de qué', 'No ha sido nada', 'Encantada!', 'Es un placer', 'Es mi trabajo',
               'De nada!', 'Ni lo menciones', 'Me alegra poder ayudar', 'Cuando gustes!', 
               'Para eso estamos', 'Cualquier cosa por ti', 'Ya te la sábanas que pa eso andamios']
    msg = choice(welcome)
    if verbose: print(msg, end='. ')
    talk(msg)

#### SKILLS' DICTIONARY 

skills = {'hola': greeting,
          'por favor': gladly,
          ('quiero escuchar', 'reproduce'): play,
          ('busca', 'googlea'): searching,
          ('abre', 'inicia'): opening,
          ('escribe', 'anota'): writing,
          'temporizador': startimer,
          ('dime', 'cuéntame'): tellme,
          'ayuda': helpme,
          ('gracias', 'muchas gracias'): urwelcome,
          ('adiós', 'bye', 'autodestrúyete'): goodbye}

#### OTHER FUNCTIONS 

def find(name, searchpath, file=False, directory=False, findall=False):
    ''' Searches for a file (default) or directory name inside a given searching 
        path and returns the first (default) or all coincidences found.'''
   
    result = []
    if file or not file and not directory:
        for root, dirs, files in walk(searchpath):
            for i in files:
                if name in path.basename(i).lower():
                    if findall: result.append(path.join(root, i))
                    else: return path.join(root, i)
    else:
        for root, dirs, files in walk(searchpath):
            for i in dirs:
                if name in i.lower():
                    if findall: result.append(path.join(root, i))
                    else: return path.join(root, i)
    return result

def read_configs(file):
    ''' Parses the configurations in the .txt file given and stores 
        them in a dictionary. '''
    
    lines = []
    with open(file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        file.close()
    lines = [ x.strip().split(": ") for x in lines ]    
    return dict(lines)


#### MAIN FUNCTIONS 


def talk(text, voice=0, speed=145):
    engine.setProperty('voice', engine.getProperty('voices')[voice].id)
    engine.setProperty('rate', speed)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Calibrando el micrófono, por favor espera.")  
        listener.adjust_for_ambient_noise(source, duration=int(configs['clbn-time']))  
        print("Escuchando...")
        micro = listener.listen(source)
        try:
            recog = listener.recognize_google(micro, language='es')
            recog = recog.lower()
            name = configs['asis-name']
            if name in recog:
                recog = recog.replace(name, '') 
            return recog
        except sr.UnknownValueError:
            print('No entendí, inténtalo de nuevo.')
            return ''
        except sr.RequestError():
            print('No pude conectarme a los servicios de reconocimiento de voz de Google.')
            return ''
    
def run(verbose=True):
    
    request = listen()
    if verbose: print(request)
    if request == '': return
    
    for skill in skills:
        if type(skill) is not str: # then there are several key words
            for keyword in skill: 
                if keyword in request: # then complete the request
                    request = request.replace(keyword, '')
                    skills[skill](request, verbose)
        elif skill in request:
                request = request.replace(skill, '')
                skills[skill](request, verbose)

#### EXECUTION (MAIN)

listener = sr.Recognizer()
engine = tts.init()

sites = read_configs('sites.txt')
apps = read_configs('apps.txt')
configs = read_configs('configurations.txt')
active = True

while active:
    try:
        run()
    except:
        print('ERROR: Por favor, checa el código fuente.')
        input()
        

    
    
    
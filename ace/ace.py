import pyttsx3
import requests
from requests.api import request 
import speech_recognition as sr
import datetime
import cv2
import numpy as np
import os  
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit
import sys  
import csv
import threading
import time
import tkinter.messagebox
import pyjokes
import pyautogui
from tkinter import * ##must be com while alpha code##
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk
from mutagen.mp3 import MP3
from pygame import mixer
from urllib.parse import quote_from_bytes
from PIL import ImageFont, ImageDraw, Image 


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voices',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=3,phrase_time_limit=5)
    
    try:
        print("Recognize...")
        query = r.recognize_google(audio,language='en-in')
        print(f"user said:{query}")

    except Exception as e :
        speak("say that again please...")
        return "none"   
    return query            

def wish():
    ##Initializing ..
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour>=0 and hour<=12:
        speak(f"good morning, its{tt}")
    elif hour>=12 and hour<=18:
        speak(f"good afternoon,its {tt}")
    else: 
        speak(f"good evening,its{tt}") 
    speak("I am Ace    Please tell me how can i help you")  
    speak("")      

if __name__ =="__main__":
    wish()
    while True:
    #if 1:
        query = takecommand().lower()

        if "open notepad" in query:
            npath ="C:\\WINDOWS\\system32\\notepad.exe"
            os.startfile(npath)
        

        elif "open ms office" in query:
            apath ="C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.exe"
            os.startfile(apath)


        elif "open google chrome " in query :
            sai ="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(sai)                                                                                         ##google.exe path wrong


        elif "open vlc media player " in query:
            cpath ="C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"
            os.startfile(cpath) 


        elif "open command promt" in query: 
            os.system("start cmd")


        elif "open camera" in query:
            cap = cv2.VideoCapture(0)  #0= local camera ,1=external camera
            while True:
                ret,  img = cap.read()
                cv2.imshow('webcam',img)
                k = cv2.waitkey(50)
                if k==27:
                    break;
            cap.release()
            cv2.destroyAllWindows()   


        elif "play music" in query:
            root = tk.ThemedTk()
            root.get_themes()  
            root.set_theme("radiance")   
            statusbar = ttk.Label(root, text="music", relief=SUNKEN, anchor=W, font='Times 10 italic')
            statusbar.pack(side=BOTTOM, fill=X)
            menubar = Menu(root)
            root.config(menu=menubar)
            subMenu = Menu(menubar, tearoff=0)
            playlist = []

            def browse_file():
                global filename_path
                filename_path = filedialog.askopenfilename()
                add_to_playlist(filename_path)

                mixer.music.queue(filename_path)
            def add_to_playlist(filename):
                filename = os.path.basename(filename)
                index = 0
                playlistbox.insert(index, filename)
                playlist.insert(index, filename_path)
                index += 1    

            menubar.add_cascade(label="File", menu=subMenu)
            subMenu.add_command(label="Open", command=browse_file)
            subMenu.add_command(label="Exit", command=root.destroy)

            def about_us():
                tkinter.messagebox.showinfo('player', 'This is a music player build  by @charan')
            
            subMenu = Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Help", menu=subMenu)
            subMenu.add_command(label="About Us", command=about_us)

            mixer.init()

            root.title("Music")
            root.iconbitmap(r'images/melody.ico')

            leftframe = Frame(root)
            leftframe.pack(side=LEFT, padx=30, pady=30)

            playlistbox = Listbox(leftframe)    
            playlistbox.pack()

            addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
            addBtn.pack(side=LEFT)

            def del_song():
                selected_song = playlistbox.curselection()
                selected_song = int(selected_song[0])
                playlistbox.delete(selected_song)
                playlist.pop(selected_song)

            
            delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
            delBtn.pack(side=LEFT)

            rightframe = Frame(root)
            rightframe.pack(pady=30)

            topframe = Frame(rightframe)
            topframe.pack()

            lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
            lengthlabel.pack(pady=5)

            currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE)
            currenttimelabel.pack()

            
            def show_details(play_song):
                file_data = os.path.splitext(play_song)

                if file_data[1] == '.mp3':
                    audio = MP3(play_song)
                    total_length = audio.info.length
                else:
                    a = mixer.Sound(play_song)
                    total_length = a.get_length()
                mins, secs = divmod(total_length, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                lengthlabel['text'] = "Total Length" + ' - ' + timeformat

                t1 = threading.Thread(target=start_count, args=(total_length,))
                t1.start()  
            def start_count(t):
                global paused    
                current_time = 0
                while current_time <= t and mixer.music.get_busy():
                    if paused:
                        continue
                    else:
                        mins, secs = divmod(current_time, 60)
                        mins = round(mins)
                        secs = round(secs)
                        timeformat = '{:02d}:{:02d}'.format(mins, secs)
                        currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
                        time.sleep(1)
                        current_time += 1


            def play_music():
                global paused

                if paused:
                    mixer.music.unpause()
                    statusbar['text'] = "Music Resumed"
                    paused = FALSE
                else:
                    try:
                        stop_music()
                        time.sleep(1)
                        selected_song = playlistbox.curselection()
                        selected_song = int(selected_song[0])
                        play_it = playlist[selected_song]
                        mixer.music.load(play_it)
                        mixer.music.play()
                        statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
                        show_details(play_it)
                    except:
                         tkinter.messagebox.showerror('File not found', 'Music player could not find the file. Please check again.')
            def stop_music():
                mixer.music.stop()
                statusbar['text'] = "Music Stopped"

            paused = FALSE

            def pause_music():
                global paused
                paused = TRUE
                mixer.music.pause()
                statusbar['text'] = "Music Paused"    

            def rewind_music():
                play_music()
                statusbar['text'] = "Music Rewinded"    

            def set_vol(val):
                volume = float(val) / 100
                mixer.music.set_volume(volume)   

            muted = FALSE

            def mute_music():
                global muted
                if muted:  # Unmute the music
                    mixer.music.set_volume(0.7)
                    volumeBtn.configure(image=volumePhoto)
                    scale.set(70)
                    muted = FALSE
                else:  # mute the music
                    mixer.music.set_volume(0)
                    volumeBtn.configure(image=mutePhoto)
                    scale.set(0)
                    muted = TRUE 
            middleframe = Frame(rightframe)
            middleframe.pack(pady=30, padx=30)

            playPhoto = PhotoImage(file='images/play.png')
            playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)
            playBtn.grid(row=0, column=0, padx=10)

            stopPhoto = PhotoImage(file='images/stop.png')
            stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)
            stopBtn.grid(row=0, column=1, padx=10)

            pausePhoto = PhotoImage(file='images/pause.png')
            pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)
            pauseBtn.grid(row=0, column=2, padx=10)            

            bottomframe = Frame(rightframe)
            bottomframe.pack()

            rewindPhoto = PhotoImage(file='images/rewind.png')
            rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)
            rewindBtn.grid(row=0, column=0)

            mutePhoto = PhotoImage(file='images/mute.png')
            volumePhoto = PhotoImage(file='images/volume.png')
            volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)
            volumeBtn.grid(row=0, column=1)

            scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
            scale.set(70)  # implement the default value of scale when music player starts
            mixer.music.set_volume(0.7)
            scale.grid(row=0, column=2, pady=15, padx=30) 

            def on_closing():
                stop_music()
                root.destroy()
            
            
            root.protocol("WM_DELETE_WINDOW", on_closing)
            root.mainloop()
  



            # music_dir ="D:\project\ace\music" #music location //path
            # songs = os.listdir(music_dir)                                 ## dir music only in folder 
            # rd = random.choice(songs)
            # os.startfile(os.path.join(music_dir, rd)) 
            

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text    ## ip address https://api.ipify.org (ip)
            speak(f"your Ip address is {ip}")    


        elif "wikipedia" in query:
            speak("searching wikipedia....")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences=2) ## wikipedia search audio 
            speak("according to wikipedia")
            speak(results)
            print(results)   


        elif "search on youtube" in query: 
            speak("what should i search on youtube..")  ## youtube search
            ym=takecommand().lower()
            webbrowser.open(f"{ym}") 


        elif "play song on youtube" in query:
            pywhatkit.playonyt("life goes on on")## any song name


        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")  ##youtube open
                

        elif "open gmail" in query:
            webbrowser.open("www.gmail.com") ##gmail


       # elif "open Facebook " in  query:
        #    webbrowser.open("https://www.facebook.com/")  ##facebook
            


        elif "open Goolge" in query:  
            speak("what should i search on google..")  ##google
            cm=takecommand().lower()
            webbrowser.open(f"{cm}")     


        elif "open alpha" in query:   
            f = open("coords.txt","w")
            def draw_circle(event,x,y,flags,param):
                if event == cv2.EVENT_LBUTTONDBLCLK:
                    cv2.putText(img,"coordinates (%d,%d)"%(x,y),(60,60),2,1,(0,255,0)) 
                    f.write(str(x)+"\n")                                              
                    f.write(str(y)+"\n")                                              
            img = cv2.imread("cse.jpg")
            cv2.namedWindow('image')
            cv2.setMouseCallback('image',draw_circle)
            while(1):
                cv2.imshow('image',img)
                if cv2.waitKey(10) & 0xFF == 27:
                    break
            cv2.destroyAllWindows()   
            f.close()

            f = open("names.txt","r")
            names_list = f.read().split("\n")
            f1 = open("coords.txt","r")
            coordinates = f1.read().split("\n")
            flag=True
            for i in range(len(names_list)):
                name_to_print = names_list[i]
                #date_to_print = "30/10/2021"  
                image = cv2.imread("cse.jpg")  
                cv2_im_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)  
                pil_im = Image.fromarray(cv2_im_rgb)  
                draw = ImageDraw.Draw(pil_im)  
                font = ImageFont.truetype("./fonts/Lato-Black.ttf", 40)     
                font1 = ImageFont.truetype("./fonts/MLSJN.ttf", 22) 
                draw.text((int(coordinates[0]), int(coordinates[1])), name_to_print, font=font , fill='black')
                #draw.text((int(coordinates[2]), int(coordinates[3])), date_to_print , font=font1, fill='blue')
                cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)  
                if flag:
                    cv2.imshow('Certificate', cv2_im_processed) 
                    flag=False
                    path = ''
                    cv2.imwrite('./output/'+name_to_print+'.png',cv2_im_processed)
                cv2.waitKey(0)  
                cv2.destroyAllWindows()


        elif "kill"  in query:
            speak("thank for using me,have a good day")
            sys.exit()


        elif "close notepad" in query:
            speak("closing notepad")
            os.system("taskkill /f /im notepad.exe")   
      
      
        elif  "where i am " in query or "where we are" in query:
            speak("wait sir,let me check")
            try:
                ipAdd = request.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                geo_requests = request.get(url)
                geo_data = geo_requests.json()
                
                city = geo_data['city']
                country = geo_data['country']
                speak(f"sir i am not sure , but i think we are in {city} city of {country} country")
            except Exception as e:
                speak("sorry sir , Due to network issue i am not able to find where we are.")
                pass    
                
         
        elif "take screenshot" in query or "take a screenshot" in query:
            speak("please tell me the name for this screenshot")
            name = takecommand().lower()
            speak("plaese hold the screen for few seconds,i am taking screeenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("i am done taking screenshot. now i am ready for next command")
            
         
        elif "tell me a joke" in query:
            joke=pyjokes.get_joke()
            speak(joke)
       
       
       
        speak("do we have any other work")    
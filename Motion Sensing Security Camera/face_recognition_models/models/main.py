import cv2
import sys
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import winsound
import face_recognition

from pkg_resources import resource_filename

def pose_predictor_model_location():
    return resource_filename(__name__, "models/shape_predictor_68_face_landmarks.dat")

def pose_predictor_five_point_model_location():
    return resource_filename(__name__, "models/shape_predictor_5_face_landmarks.dat")

def face_recognition_model_location():
    return resource_filename(__name__, "models/dlib_face_recognition_resnet_model_v1.dat")

def cnn_face_detector_model_location():
    return resource_filename(__name__, "models/mmod_human_face_detector.dat")
#sys.path.append('C:\\Users\\Lenovo\\AppData\\Local\\Programs\\Python\\Python3\\Lib\\site-packages')
#sys.path.append('C:\\Users\\Lenovo\\Anaconda3\\Lib\\site-packages')

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_picture():
    print("scanning")
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read(0)
    cv2.imwrite('picture.jpeg', frame)
    cap.release()
    print("face scan complete")



def analyzer_user():
    print("analizing")
    baseing = face_recognition.load_image_file("mainpic.jpeg")
    baseing = cv2.cvtColor(baseing, cv2.COLOR_BGR2RGB)

    myface = face_recognition.face_locations(baseing)[0]
    encodemyface = face_recognition.face_encodings(baseing)[0]
    cv2.rectangle(baseing, (myface[3], myface[0]), (myface[1], myface[2]), (255, 0, 255), 2)

    sampleimage = face_recognition.load_image_file("picture.jpeg")
    sampleimage = cv2.cvtColor(sampleimage, cv2.COLOR_BGR2RGB)

    try:
        encodesampleface = face_recognition.face_encodings(sampleimage)[0]
    except ImportError as e:
        print("Index error Authentication failed")
        sys.exit()

    result = face_recognition.compare_faces([encodemyface], encodesampleface)
    resultstring = str(result)

    if resultstring == "[True]":

        talk("welcome sir")
        talk(" AJ here ")

        def take_command():
            try:
                with sr.Microphone() as source:
                    print('listening...')
                    voice = listener.listen(source)
                    command = listener.recognize_google(voice)
                    command = command.lower()
                    if 'aj' in command:
                        command = command.replace('aj', '')

            except:
                pass
            return command
        def run_AJ():
            command = take_command()
            print(command)
            if 'yourself' in command:
                talk('Hello everyone I am AJ . A chat bot built by Anfinsen, Trisha, Monish, Sahil')
                run_AJ()
            elif 'play' in command:
                song = command.replace('play', '')
                talk('playing ' + song)
                pywhatkit.playonyt(song)
                run_AJ()
            elif 'open camera' in command:
                talk('Opening')
                cam = cv2.VideoCapture(0)
                run_AJ()
                while cam.isOpened():
                    ret, frame1 = cam.read()
                    ret, frame2 = cam.read()
                    diff = cv2.absdiff(frame1, frame2)
                    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
                    blur = cv2.GaussianBlur(gray, (5, 5), 0)
                    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
                    dilated = cv2.dilate(thresh, None, iterations=3)
                    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    for c in contours:
                        if cv2.contourArea(c) < 5000:
                            continue
                        x, y, w, h = cv2.boundingRect(c)
                        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        winsound.Beep(500, 200)
                    if cv2.waitKey(10) == ord('q'):
                        break
                    cv2.imshow('sem3 Cam', frame1)
                run_AJ()
            elif 'time' in command:
                time = datetime.datetime.now().strftime('%I:%M %p')
                talk('Current time is ' + time)
                run_AJ()
            elif 'who is'  in command:
                person = command.replace('who is', '')
                info = wikipedia.summary(command, 5)
                print(info)
                talk(info)
                run_AJ()
            elif 'what is'  in command:

                info = wikipedia.summary(command, 5)
                print(info)
                talk(info)
                run_AJ()
            elif 'joke' in command:
                talk(pyjokes.get_joke())
                run_AJ()
            elif 'thank you' in command:
                talk('thank you sir')
            else:
                talk('Please say the command again.')
                run_AJ()
        while True:
            run_AJ()
            break
    else:
        print("sorry")
take_picture()
analyzer_user()


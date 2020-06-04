from tkinter import *
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import time
import sys
from rehamove import * 


## initiate global variables
global electrode_status
electrode_status = [0,0,0,0,0,0,0,0]  # check the status of the electrodes

global customized_pulse
customized_pulse = [[1,2],[3,4]]  # store the customized pulse

global pulse_train
pulse_train = [0,0,0,0] # represent amplitude, width, period, duration respectively

global cus_duration 
cus_duration = 0 # total duration of the customized pulse

global cus_wid
cus_wid = 0  # the duration of each single customized pulse

global start
start = 0  # record starting time

global send
send = 0  # record the status, sending or not

global stop
stop = 0  # check stop button status

global rehamove_connection
rehamove_connection = 0  # initiate the connection
 
## Design the pulse
def designPulse():
    global amplitude_input
    global width_input
    global period_input
    global duration_input
    global pulse_train
    try:
        pulse_train[0] = int(amplitude_input.get())
        pulse_train[1] = int(width_input.get())
        pulse_train[2] = int(period_input.get())
        pulse_train[3] = int(duration_input.get())
        if pulse_train[0] <= 0 or pulse_train[1] <= 0 or pulse_train[2] <= 0 or pulse_train[3] <= 0:
            messagebox.showinfo("Error", "Cannot be zero or negative number")
    except ValueError:
         messagebox.showinfo("Error", "Inappropriate input")
    print(pulse_train)


## Change electrode colour   
def selectElectrode(num):
    global electrode_array
    global master
    global electrode_status
    index = num-1
    if electrode_status[index] == 0:
        image_button = Image.open("orange.png")
        electrode_status[index] = 1
    elif electrode_status[index] != 0:
        image_button = Image.open("electrode.png")
        electrode_status[index] = 0
    new_img = image_button.resize((50,50))
    img = ImageTk.PhotoImage(new_img)
    electrode_array[index].config(image=img)
    master.mainloop()

def sendPulseSignal():
    global send
    global stop
    global pulse_train # [amplitude, width, period, duration], pulse_train[3] = duration
    global electrode_status
    global rehamove_connection
    if electrode_status.count(1) != 2: # check if two electrodes are selected
        messagebox.showinfo("Error", "Choose exact two channels")
    else:
        if send == 0: # no existed sending
            start = time.time()
            rehamove_connection.change_mode(1) # change to mid-level
            if stop == 0: # if stop button is not pressed
                rehamove_connection.set_pulse(pulse_train[0], pulse_train[1])
                rehamove_connection.start("blue", pulse_train[2])
            while ((time.time()-start) < pulse_train[3]) and stop == 0: # if the time passed is still within the set duration and stop button is not pressed
                send = 1 # record the status
                master.after(10, master.update()) # update the interface
                rehamove_connection.update() # update the rehamove

            # if the duration is complete, or if the stop button is pressed
            rehamove_connection.end()
            send = 0
            stop = 0
 stop sending message to the stimulator
    
def stopSignal():
    global stop
    stop = 1
    

master = Tk()

# connect with the stimulator
rehamove_connection = Rehamove("COM7")

# start building the frame
signal = Frame(master, bg = "white")
electrode = Frame(master, bg = "white")
signal.pack(fill=X, side=TOP)
pulse_signal = Frame(signal, bg = "white")
custom_signal = Frame(signal, bg = "white")
pulse_signal.pack(side=LEFT)
custom_signal.pack()
electrode.pack(fill=X, expand=1, side=TOP)
electrode_pic = Frame(electrode, bg="white")
electrode_pic.pack(side=LEFT)
electrode_arrangement = Frame(electrode, bg="white")
electrode_arrangement.pack(expand=1)

##pulse_signal
design_signal = Label(pulse_signal, text = "Design pulse train", bg = "light yellow")
design_signal.grid(row = 1, padx = 5)
amplitude = Label(pulse_signal, text = "Amplitude (mA): ", bg = "white")
amplitude.grid(row = 2, padx = 5)
amplitude_input = Entry(pulse_signal)
amplitude_input.grid(row = 2, column = 6)
width = Label(pulse_signal, text = "Pulse width (us): ", bg = "white")
width.grid(row = 3, padx = 5)
width_input = Entry(pulse_signal)
width_input.grid(row = 3, column = 6)
period = Label(pulse_signal, text = "Interval between pulses (ms): ", bg = "white")
period.grid(row = 4, padx = 5)
period_input = Entry(pulse_signal)
period_input.grid(row = 4, column = 6)
duration = Label(pulse_signal, text = "Duration(s): ", bg = "white")
duration.grid(row = 5, padx = 5)
duration_input = Entry(pulse_signal)
duration_input.grid(row = 5, column = 6)
submit_button = Button(pulse_signal, text = "Set parameters", command = lambda: designPulse(), bg = "white")
submit_button.grid(row = 3, column = 8, padx=10)


##electrode selection
select_electrode = Label(electrode_pic, text = "Select electrodes", bg = "light yellow")
select_electrode.pack(side=TOP)
image_hand = Image.open("pic.png")
new_img = image_hand.resize((100,200))
img = ImageTk.PhotoImage(new_img)
img_label = Label(electrode_pic, image = img)
img_label.pack(expand=1)
button_image = Image.open("electrode.png")

button_img = ImageTk.PhotoImage(button_image.resize((50,50)))
electrode_button1 = Button(electrode_arrangement, image = button_img, command = lambda: selectElectrode(1))
electrode_button1.grid(row=1,column=20,padx=30,pady=3)

electrode_button2 = Button(electrode_arrangement, image = button_img, command = lambda: selectElectrode(2))
electrode_button2.grid(row=1,column=28,padx=3,pady=3)

electrode_button3 = Button(electrode_arrangement, image = button_img, command = lambda: selectElectrode(3))
electrode_button3.grid(row=3,column=20,padx=3,pady=3)

electrode_button4 = Button(electrode_arrangement, image = button_img, command = lambda: selectElectrode(4))
electrode_button4.grid(row=3,column=28,padx=3,pady=3)

electrode_button5 = Button(electrode_arrangement, image = button_img, command = lambda: selectElectrode(5))
electrode_button5.grid(row=4,column=20,padx=3,pady=3)

electrode_button6 = Button(electrode_arrangement, image = button_img, command = lambda: selectElectrode(6))
electrode_button6.grid(row=4,column=28,padx=3,pady=3)

electrode_button7 = Button(electrode_arrangement, image = button_img, command = lambda: selectElectrode(7))
electrode_button7.grid(row=5,column=20,padx=3,pady=3)

electrode_button8 = Button(electrode_arrangement, image = button_img, command = lambda: selectElectrode(8))
electrode_button8.grid(row=5,column=28,padx=3,pady=3)

electrode_array = [electrode_button1,electrode_button2, electrode_button3,
                   electrode_button4, electrode_button5, electrode_button6,
                   electrode_button7, electrode_button8]



stop_button = Button(electrode_arrangement, text = "Stop", command = lambda: stopSignal(), bg = "white")
stop_button.grid(row=4,column=30, padx=30)
pulse_train_stimulation_button = Button(electrode_arrangement, text = "Stimulate", command = lambda: sendPulseSignal(), bg = "white")
pulse_train_stimulation_button.grid(row=1,column=30, padx=30)

master.mainloop()

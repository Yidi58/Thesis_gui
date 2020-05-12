from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import time

global count
count = [0,0,0,0,0,0,0,0]

global customed_pulse
customed_pulse = [[1,2],[3,4]]

global cus_duration
cus_duration = 0

global cus_wid
cus_wid = 0

global send
send = False

global start
start = 0

def designPulse():
    global amplitude_input
    global duration_input
    global repeat_input
    amp = int(amplitude_input.get())
    freq = int(repeat_input.get())
    dur = int(duration_input.get())
    D = np.linspace(0, dur,num=dur*10)
    P = freq
    assist = dur/P
    width = dur/(2*P)
    sig = amp*((D%assist+0.02) < width)
    plt.plot(D,sig)
    plt.show()

def customPulse():
    global customed_pulse
    global cus_duration
    global cus_wid
    cus_amp = float(custom_amp_input.get())
    cus_wid = float(custom_width_input.get())
    cus_ratio = float(custom_ratio_input.get())
    cus_duration = float(custom_duration_input.get())
    customed_signal_info = [cus_amp, cus_wid, cus_ratio, cus_duration]
    if customed_signal_info[2] > 0:
        customed_pulse[0][0] = customed_signal_info[0]*(customed_signal_info[2]/100)
        customed_pulse[0][1] = customed_signal_info[1]*(100/customed_signal_info[2])
        customed_pulse[1][0] = (-1)*customed_signal_info[0]
        customed_pulse[1][1] = customed_signal_info[1]
    if customed_signal_info[2] < 0:
        customed_pulse[1][0] = customed_signal_info[0]*(customed_signal_info[2]/(100))
        customed_pulse[1][1] = customed_signal_info[1]*(-100/customed_signal_info[2])
        customed_pulse[0][0] = customed_signal_info[0]
        customed_pulse[0][1] = customed_signal_info[1]
    if customed_signal_info[2] == 0:
        customed_pulse[0][0] = customed_signal_info[0]
        customed_pulse[0][1] = customed_signal_info[1]
        customed_pulse[1][0] = (-1)*customed_signal_info[0]
        customed_pulse[1][1] = customed_signal_info[1]
    

   
def selectElectrode(num):
    global electrode_array
    global master
    global count
    index = num-1
    if count[index] == 0:
        image_button = Image.open("orange.png")
        count[index] = 1
    elif count[index] != 0:
        image_button = Image.open("electrode.png")
        count[index] = 0
    new_img = image_button.resize((50,50))
    img = ImageTk.PhotoImage(new_img)
    electrode_array[index].config(image=img)
    master.mainloop()

def sendSignal():

    global cus_duration
    global cus_wid
    global customed_pulse    
    start = time.time()
    while((time.time()-start)*1000 < cus_duration):
        master.after(10, master.update())
        master.after(300, print(customed_pulse))
        #customPulse()
    
    

master = Tk()
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
repeat = Label(pulse_signal, text = "Repeat times: ", bg = "white")
repeat.grid(row = 2, padx = 5)
repeat_input = Entry(pulse_signal)
repeat_input.grid(row = 2, column = 6)
amplitude = Label(pulse_signal, text = "Pulse amplitude(mA): ", bg = "white")
amplitude.grid(row = 3, padx = 5)
amplitude_input = Entry(pulse_signal)
amplitude_input.grid(row = 3, column = 6)
duration = Label(pulse_signal, text = "Duration(ms): ", bg = "white")
duration.grid(row = 4, padx = 5)
duration_input = Entry(pulse_signal)
duration_input.grid(row = 4, column = 6)
submit_button = Button(pulse_signal, text = "Finish", command = lambda: designPulse(), bg = "white")
submit_button.grid(row = 6, padx = 5)
##custom_signal
custom_design_signal = Label(custom_signal, text = "Design custom pulse", bg = "light yellow")
custom_design_signal.grid(row=1, padx=5)
custom_amp = Label(custom_signal, text="Customed amplitude(mA): ", bg="white")
custom_amp.grid(row=2, padx=5)
custom_amp_input = Entry(custom_signal)
custom_amp_input.grid(row=2, column=6, padx=5)
custom_width = Label(custom_signal, text="Customed pulse width(us): ", bg="white")
custom_width.grid(row=3, padx=5)
custom_width_input = Entry(custom_signal)
custom_width_input.grid(row=3, column=6, padx=5)
custom_ratio = Label(custom_signal, text="Customed pulse width ratio(-100~100): ", bg="white")
custom_ratio.grid(row=4, padx=5)
custom_ratio_input = Entry(custom_signal)
custom_ratio_input.grid(row=4, column=6, padx=5)
custom_dur = Label(custom_signal, text="Customed pulse duration(ms): ", bg="white")
custom_dur.grid(row=5, padx=5)
custom_duration_input = Entry(custom_signal)
custom_duration_input.grid(row=5, column=6, padx=5)
custom_submit_button = Button(custom_signal, text = "Finish", command = lambda: customPulse(), bg = "white")
custom_submit_button.grid(row=7, padx = 5)


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

stimulation_button = Button(electrode_arrangement, text = "Stimulate", command = lambda: sendSignal(), bg = "white")
stimulation_button.grid(row=3,column=30, padx=30)

master.mainloop()

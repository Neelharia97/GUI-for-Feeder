import tkinter as tk
from tkinter import ttk
from tkinter import *
from UDP_for_rotator_2 import MjkFeederControl

a = MjkFeederControl()


def Create_window():
    root = Tk()
    root.title('GUI For Feeder : OTA@Jabil')
    root.geometry('{}x{}'.format(460, 350))

    # create all of the main containers
    top_frame = Frame(root, bg='White', width=45, height=50, pady=3)
    center = Frame(root, bg='white', width=50, height=40, padx=3, pady=3)
    btm_frame = Frame(root, bg='white', width=45, height=45, pady=3)
    btm_frame2 = Frame(root, bg='white', width=45, height=60, pady=3)

    # layout all of the main containers
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    top_frame.grid(row=0, sticky="ew")
    center.grid(row=1, sticky="nsew")
    btm_frame.grid(row=3, sticky="ew")
    btm_frame2.grid(row=4, sticky="ew")

    # create the widgets for the top frame
    model_label = Label(top_frame, text='Feeder GUI')
    Positioner_label = Label(top_frame, text='Positioner IP:')
    Server_label = Label(top_frame, text='Server IP:')
    entry_Positioner_IP = Entry(top_frame, background="white")
    entry_Server_IP = Entry(top_frame, background="white")

    # layout the widgets in the top frame
    model_label.grid(row=0, columnspan=6)
    Positioner_label.grid(row=1, column=0, padx=2)
    Server_label.grid(row=1, column=2, padx=2)
    entry_Positioner_IP.grid(row=1, column=1, padx=2)
    entry_Server_IP.grid(row=1, column=3, padx=2)

    # Function To connect
    def connect():
        pip = entry_Positioner_IP.get()
        sip = entry_Server_IP.get()

        a.open(address=pip)

    button4 = Button(top_frame, text="Connect", command=connect)
    button4.grid(row=1, column=4, padx=2)

    # create the center widgets
    center.grid_rowconfigure(0, weight=1)
    center.grid_columnconfigure(1, weight=1)

    ctr_left = Frame(center, bg='white', width=10, height=10)
    ctr_mid = Frame(center, bg='Gray', width=10, height=10, padx=0, pady=0)
    ctr_right = Frame(center, bg='white', width=10, height=10, padx=0, pady=0)

    ctr_left.grid(row=0, column=0, sticky="ns")
    ctr_mid.grid(row=0, column=1, sticky="nsew")
    ctr_right.grid(row=0, column=2, sticky="ns")

    # Creating widgets for center

    speed_label = Label(btm_frame, text="enter speed:")
    position_label = Label(btm_frame, text="enter position:")
    speed_label.grid(row=1, column=0)
    position_label.grid(row=1, column=3)
    entry_speed = Entry(btm_frame, background="white")
    entry_position = Entry(btm_frame, background="white")
    entry_speed.grid(row=1, column=2)
    entry_position.grid(row=1, column=4)




    def set_position():
        try:
            sp = int(entry_speed.get())
            pos = int(entry_position.get())
            print("moving by" ,sp,"to", pos)
            (a.set_position(pos, sp))
            print("Correct Number")
        except ValueError:
            pass
    button1 = Button(center, text="ClockWise",command=set_position)
    button1.grid(row=0, column=0, padx=2, pady=2)
    button3 = Button(center, text="Anti-Clockwise", command=set_position)
    button3.grid(row=0, column=2, padx=2, pady=2)

    def reset():
        a.search_zero()

    button2 = Button(center, text="Reset/Search for Home", command=reset)
    button2.grid(row=0, column=1, padx=2, pady=2)

    root.mainloop()


Create_window()

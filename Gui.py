import os
import sys
import subprocess
import tkinter as tk
from ctypes import * # type: ignore

import customtkinter as ctk
from PIL import Image

from MapView import App
from PhoneNumber import PhoneNumber
from ScrolledListBox import ScrolledListbox


def country_code_uploader():
    country_code_list = []
    try:
        current_file_path = os.path.dirname(os.path.realpath(__file__))
        img_path = os.path.join(current_file_path, "Country-Codes.txt")
        with open(img_path, "r") as file:
            for line in file:
                country_code_list.append(line.strip())
    except FileNotFoundError:
        print("Error: File not found")
    return country_code_list

values = country_code_uploader()

def list_to_dict(code_list):
    country_codes_dict = {}
    for code in code_list:
        try:
            country, phone_code = code.split('+')
            country_codes_dict[country] = '+'+phone_code.strip()
        except ValueError as e:
            print(f"Invalid value {code}: {e}")
    return country_codes_dict


class GUI:
    def __init__(self):
################## Widgets Initialization ###############   
     
        # Create the main window
        self.root = ctk.CTk()
        self.width, self.height = 720, 460
        self.root.geometry(f"{self.width}x{self.height}+400+300")
        self.root.resizable(False,False)
        self.root.title('Phone Tracker')
        self.app = None # Initialize the App instance

        # Adding labels to GUI
        current_file_path = os.path.dirname(os.path.realpath(__file__))
        img_path = os.path.join(
            current_file_path, 'images/Phone-Tracker.png')
        # Load and convert the image to a PhotoImage
        pil_image = Image.open(img_path)
        self.image_widget = ctk.CTkImage(
            light_image=pil_image, dark_image=pil_image, size=(100, 100))
        self.label_widget = ctk.CTkLabel(
            self.root, text='', image=self.image_widget,)
        self.label_widget.place(relx=0.25, rely=0.2, anchor=tk.W)
        self.label1 = ctk.CTkLabel(self.root,
                                text="\n Phone-Tracker\n",
                                font=("Arial Bold", 40), text_color="#357EC7")
        self.label1.place(relx=0.40, rely=0.2, anchor=tk.W)
    
        # Adding Label, ScrolledListBox and Button for phone_code
        self.label1 = ctk.CTkLabel(self.root,
                                text="  Choose your Country Code?   ",
                                font=("Arial Bold", 14))
        self.label1.place(relx=0.05, rely=0.44, anchor=tk.W)
        
        self.scrolled_listbox = ScrolledListbox(
            self.root, width=35, height=1, bg='#4F4F4F',
            listvariable=values)
        self.scrolled_listbox.place(relx=0.38, rely=0.38)
        
        self.selection_btn = ctk.CTkButton(
            self.root, text="Selection",
            command=lambda: self.get_country_code(self.scrolled_listbox.selected_item))
        self.selection_btn.place(relx=0.75, rely=0.40)

        # Adding Label,textbox and Button for phone number
        self.label2 = ctk.CTkLabel(self.root,
                                text="  Enter your phone number:   ",
                                font=("Arial Bold", 14))
        self.label2.place(relx=0.05, rely=0.64, anchor=tk.W)

        self.phone_number_textbox = ctk.CTkEntry(self.root, width=200)
        self.phone_number_textbox.place(relx=0.37, rely=0.64, anchor=tk.W)
        self.phone_number_textbox.bind(
            "<Return>", lambda event: self.enter_pressed())
        
        self.enter_btn = ctk.CTkButton(self.root,
                                    text="Enter",
                                    font=("Arial", 12),
                                    command=lambda: self.enter_pressed())
        self.enter_btn.place(relx=0.68, rely=0.64, anchor=tk.W)
         

        # Adding appearance option menu to GUI
        self.label_mode = ctk.CTkLabel(master=self.root,
                                    text="   Appearance Mode:",
                                    font=("Arial", 12))
        self.label_mode.place(relx=0.05, rely=0.94, anchor=tk.W)

        self.optionmenu_1 = ctk.CTkOptionMenu(master=self.root,
                                            values=["Dark", "Light", "System"],
                                            font=("Arial", 12), fg_color="#4F4F4F", button_color="#4F4F4F",
                                            command=self.change_appearance_mode)
        self.optionmenu_1.set("System")
        self.optionmenu_1.place(relx=0.22, rely=0.94, anchor=tk.W)

        self.root.bind("<Return>",
                    lambda event: self.enter_pressed)
        self.root.bind("<Command-q>", self.on_closing)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

########## Functions for the widgets ##############
    
    def get_country_code(self,code):
        code_number = code.split("+")[1]
        phone_code = '+'+code_number.strip()
        return phone_code        
    
    def phonenumber(self,phone_number):
        phone_code = self.get_country_code(self.scrolled_listbox.selected_item)
        phone_number = phone_code + phone_number
        phone = PhoneNumber(phone_number)
        latitude, longitude = phone.map_location()
        coordinates = (latitude, longitude)
        return coordinates

    def open_MapView(self,phone_number):
        coordinates = self.phonenumber(phone_number)
        self.app = App(self.root)
        self.app.start(coordinates)

        
    def enter_pressed(self):
        phone_number = self.phone_number_textbox.get().lower()
        # If phone_number is not provided
        if len(phone_number)<1:
            dialog = ctk.CTkInputDialog(
                text="Type in a phonenumber:", title="Phonenumber Register")
            phonenumber = dialog.get_input().lower() # type: ignore
            if len(phonenumber)<1:
                self.enter_pressed()
            else:
                self.phonenumber(phonenumber)
                self.open_MapView(phonenumber)
        # Else if phone_number is provided
        else:
            self.phonenumber(phone_number)  
            self.open_MapView(phone_number)


    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
        
    def start(self):
        self.root.mainloop()
        
    def on_closing(self):
        self.root.destroy()
        
        
if __name__ == '__main__':
    phone = GUI()
    phone.start()

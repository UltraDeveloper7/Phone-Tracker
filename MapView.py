import customtkinter as ctk
import os
import sys
import subprocess

from tkintermapview import TkinterMapView

ctk.set_default_color_theme("blue")


class App:

    APP_NAME = "Map-View/Phone Locator"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = master
        self.top = ctk.CTkToplevel(self.master)
        # Bring the window to the top
        self.top.lift()
        self.top.grab_set()
        self.top.title(App.APP_NAME)
        self.top.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.top.minsize(App.WIDTH, App.HEIGHT)

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.top.bind("<Command-q>", self.on_closing) # type: ignore
        #self.top.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []

        # ============ create two CTkFrames ============

        self.top.grid_columnconfigure(0, weight=0)
        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_rowconfigure(0, weight=1)

        self.frame_left = ctk.CTkFrame(master=self.top, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = ctk.CTkFrame(master=self.top, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = ctk.CTkButton(master=self.frame_left,
                        text="Set Marker",
                        command=self.set_marker_event)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = ctk.CTkButton(master=self.frame_left,
                                                text="Clear Markers",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.map_label = ctk.CTkLabel(self.frame_left, text="Map Style:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = ctk.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google Normal", "Google Satellite"],
                                                                    command=self.change_map)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = ctk.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)


        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.map_widget.bind("<Button-1>",self.map_widget.mouse_click)
        

        self.entry = ctk.CTkEntry(master=self.frame_right,
                                            placeholder_text="Type Address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = ctk.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)
        
        # Right/Left click events
        self.map_widget.add_right_click_menu_command(label="Add Marker",
                                                     command=self.add_marker_event,
                                                     pass_coords=True)
        self.map_widget.add_left_click_map_command(self.left_click_event)

        # Set default values
        self.map_widget.set_address("Athens")
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")
        
    def add_marker_event(self,coords):
        print("Add marker:", coords)
        new_marker = self.map_widget.set_marker(coords[0], coords[1])
        self.marker_list.append(new_marker)
        # Center the map on the new marker
        self.map_widget.set_position(coords[0], coords[1])
        
    def left_click_event(self,coordinates_tuple):
        clicked_position = coordinates_tuple
        self.marker_list.append(self.map_widget.set_marker(
            clicked_position[0], clicked_position[1]))
        print(f"{clicked_position[0]}-{clicked_position[1]}")

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())
        
    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))
    
    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "Google Normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "OpenStreetMap":
            self.map_widget.set_tile_server(
                "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google Satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22) 

    def on_closing(self, event=0):
        self.top.destroy()

    def start(self, coordinates=None):
        if coordinates is not None:
            self.add_marker_event(coordinates)
        self.top.mainloop()

    

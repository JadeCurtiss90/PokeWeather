import tkinter as tk
import os, sys
from tkinter import messagebox, PhotoImage
from datetime import datetime, timedelta

class WeatherLightGui:
    def __init__(self):
        self.root = tk.Tk(className="WeatherLight")
        self.root.geometry("800x120")
        self.root.attributes("-alpha", .9)
        self.root.resizable(False,False)
        self.root.geometry("-0-30")

        self.sunny_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gr1.png"))
        self.hot_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gr2.png"))
        self.raining_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "ky1.png"))
        self.snowing_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "ky2.png"))
        self.clear_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "ra1.png"))

        current_datetime = datetime.now()
        #this is updated every time the API is called, so there's no reason to keep track of it

        for i in range(1,8):
            setattr(self, f"day{i}data", "No Data")
            setattr(self, f"day{i}frame", tk.Frame(self.root, width=114, height=120))
            setattr(self, f"day{i}image", tk.Label(getattr(self, f"day{i}frame"), image=self.sunny_img))
            setattr(self, f"day{i}forecast", tk.Label(getattr(self, f"day{i}frame"),
                                                      text=getattr(self, f"day{i}data"), wraplength=114))
            if i == 1:
                setattr(self, f"day{i}text", tk.Label(getattr(self, f"day{i}frame"),
                                                  text="Today"))
            else:
                setattr(self, f"day{i}text", tk.Label(getattr(self, f"day{i}frame"),
                                                  text=(current_datetime + timedelta(days=1)).strftime('%a')))
            #it's customary for any weather report to explicitly indicate today as "Today" and not the day
            getattr(self, f"day{i}image").place(relx = .5, rely = .2, anchor = "n")
            getattr(self, f"day{i}forecast").place(relx = .5, rely = .7, anchor = "center")
            getattr(self, f"day{i}text").place(relx = .5, rely = .99, anchor = "s")
            getattr(self, f"day{i}frame").place(relx = (i-1)/7, relwidth = 1/7, rely = .5, anchor = "w")

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())
        #set window close protocol

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to exit?"):
            self.root.destroy()
            sys.exit(0)
            #since asyncio is still waiting for APILink, this is needed for a window close to be "proper"

    def gui_update(self, day1data = "No Data", day2data = "No Data", day3data = "No Data", day4data = "No Data",
               day5data = "No Data", day6data = "No Data", day7data = "No Data"):
        args = locals()
        #for easy dynamic referencing

        for i in range(1,8):
            data = args[f"day{i}data"]
            #dynamically obtain passed arguments
            getattr(self, f"day{i}forecast").config(text=data)

            if "Clear" in data:
                getattr(self, f"day{i}image").config(image=self.clear_img)
            elif "Sunny" in data:
                getattr(self, f"day{i}image").config(image=self.sunny_img)
            elif "Hot" in data:
                getattr(self, f"day{i}image").config(image=self.hot_img)
            elif "Rain" in data:
                getattr(self, f"day{i}image").config(image=self.raining_img)
            elif "Snow" in data:
                getattr(self, f"day{i}image").config(image=self.snowing_img)
            #a bit arbitrary, but this seems to roughly match the APIs reporting schema

            if i == 1:
                getattr(self, f"day{i}text").config(text="Today")
            else:
                getattr(self, f"day{i}text").config(text=(datetime.now() + timedelta(days=i)).strftime('%a'))
            #as before, "Today" is "Today"
import tkinter as tk
import asyncio, APILink, json, os,sys, textwrap
from tkinter import messagebox, PhotoImage, ttk
from ttkthemes import ThemedTk
from datetime import datetime, timedelta
from idlelib.tooltip import Hovertip
from StateAbbreviationDict import state_abbreviations

class WeatherLightGui:
    def __init__(self):
        self.root = ThemedTk(className = "WeatherLight", theme = "blue")
        self.root.overrideredirect(True)
        self.root.geometry("800x150")
        self.root.attributes("-alpha", .9)
        self.root.resizable(False,False)
        self.root.geometry("-0-40")

        self.x = None
        self.y = None
        self.root.bind("<ButtonPress-1>", self.hold_click)
        self.root.bind("<ButtonRelease-1>", self.release_click)
        self.root.bind("<B1-Motion>", self.move_window)

        self.sunny_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gr1.png"))
        self.hot_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "gr2.png"))
        self.raining_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "ky1.png"))
        self.snowing_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "ky2.png"))
        self.clear_img = PhotoImage(file=os.path.join(os.path.dirname(__file__), "ra1.png"))

        self.current_location = APILink.get_user_location()

        current_datetime = datetime.now()
        #this is updated every time the API is called, so there's no reason to keep track of it

        for i in range(1,8):
            setattr(self, f"day{i}data", "No Data")
            setattr(self, f"day{i}detailed_data", "No Data")
            setattr(self, f"day{i}frame", ttk.Frame(self.root, width=114, height=150))
            setattr(self, f"day{i}image", ttk.Label(getattr(self, f"day{i}frame"), image=self.sunny_img))
            setattr(self, f"day{i}forecast", ttk.Label(getattr(self, f"day{i}frame"),
                                                      text=getattr(self, f"day{i}data"), wraplength=114,
                                                       justify="center"))
            setattr(self, f"day{i}detailed_forecast",
                    Hovertip(getattr(self, f"day{i}image"),
                             textwrap.fill(getattr(self, f"day{i}detailed_data"), width = 100)))
            if i == 1:
                setattr(self, f"day{i}text", ttk.Label(getattr(self, f"day{i}frame"),
                                                  text="Today"))
            else:
                setattr(self, f"day{i}text", ttk.Label(getattr(self, f"day{i}frame"),
                                                  text=(current_datetime + timedelta(days=i-1)).strftime('%a')))
            #it's customary for any weather report to explicitly indicate today as "Today" and not the day
            getattr(self, f"day{i}image").place(relx = .5, rely = .1, anchor = "n")
            getattr(self, f"day{i}forecast").place(relx = .5, rely = .48, anchor = "center")
            getattr(self, f"day{i}text").place(relx = .5, rely = .75, anchor = "s")
            getattr(self, f"day{i}frame").place(relx = (i-1)/7, relwidth = 1/7, rely = .5, anchor = "w")

        self.location_button = ttk.Button(text="Select Location")
        self.location_field = ttk.Label(text="Displaying Results for: None")
        self.refresh_button = ttk.Button(text="Refresh")
        self.close_button = ttk.Button(text="Close")

        self.location_button.place(relx=1/4, rely=.99, anchor="s")
        self.location_field.place(relx=2/4, rely=.99, anchor="s")
        self.refresh_button.place(relx=3/4, rely=.99, anchor="s")
        self.close_button.place(relx=.96, rely=.99, anchor="s")

        self.location_button.config(command=self.on_location_button_click)
        self.refresh_button.config(command=self.on_refresh_button_click)
        self.close_button.config(command=self.on_close_button_click)

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())
        #set window close protocol

    async def create_api_link(self, location):
#        while True:
        data = APILink.get_api_data("https://api.weather.gov", "weatherlighttestkey",
                                "/points/" + str(location["latitude"]) + "," + str(location["longitude"]))
        parsed_data = json.loads(data.text)
        forecast = APILink.get_api_data(parsed_data["properties"]["forecast"], "weatherlighttestkey")
        parsed_forecast = json.loads(forecast.text)
        if parsed_forecast["properties"]["periods"][0]["isDaytime"]:
            self.gui_update(parsed_forecast["properties"]["periods"][0]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][0]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][2]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][2]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][4]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][4]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][6]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][6]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][8]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][8]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][10]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][10]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][12]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][12]["detailedForecast"],
                                       location)
        elif parsed_forecast["properties"]["periods"][1]["name"] == datetime.now().strftime('%A'):
            self.gui_update(parsed_forecast["properties"]["periods"][1]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][1]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][3]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][3]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][5]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][5]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][7]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][7]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][9]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][9]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][1]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][1]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][13]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][13]["detailedForecast"],
                                       location)
        else:
            self.gui_update(parsed_forecast["properties"]["periods"][0]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][0]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][1]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][1]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][3]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][3]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][5]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][5]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][7]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][6]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][9]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][9]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][11]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][11]["detailedForecast"],
                                       location)
            # the API seems to provide 1-2 datasets for each day: "day" and "night". If it's night, the current day (and
            # only the current day) will only have a "night" entry. All other days will have both
#            await asyncio.sleep(3600)
            # once an hour seems like a reasonable (if arbitrary) wait time

    def on_cancel_button_click(self, window):
        window.destroy()

    def on_confirm_button_click(self, city, state, window):
        new_location = APILink.get_location("1 Main St., " + city.get() + ", " + state.get())
        if new_location["city"] == "Nowhere" and new_location["state"] == "Oklahoma":
            messagebox.showerror("Error", "No valid address found! Please try again.")
            return
        self.current_location = new_location
        self.root.after(100, lambda: asyncio.create_task(self.create_api_link(self.current_location)))
        window.destroy()

    def on_location_button_click(self):
        location_window = tk.Toplevel(self.root)
        location_window.title("Select Location")
        location_window.geometry("300x200")

        frame = ttk.Frame(location_window,width=300, height=200)
        header = ttk.Label(frame, text="Please enter a city and state")
        city = ttk.Entry(frame, width=20)
        city_label = ttk.Label(frame, text="City")
        state = ttk.Combobox(frame, state='readonly', justify="center", width=3)
        state["values"] = list(state_abbreviations.keys())
        state.current(0)
        state_label = ttk.Label(frame, text="State")
        confirm_button = ttk.Button(frame, text="Confirm")
        cancel_button = ttk.Button(frame, text="Cancel")

        frame.place(relx=.5, rely=.5, anchor="center")
        header.place(relx=.5, rely=.3, anchor="s")
        city.place(relx=1/4, rely=.65, anchor="s")
        city_label.place(relx=1/4, rely=.75, anchor="s")
        state.place(relx=3/4, rely=.65, anchor="s")
        state_label.place(relx=3/4, rely=.75, anchor="s")
        confirm_button.place(relx=1/4, rely=.95, anchor="s")
        cancel_button.place(relx=3/4, rely=.95, anchor="s")

        confirm_button.config(command=lambda: self.on_confirm_button_click(city, state, location_window))
        cancel_button.config(command=lambda: self.on_cancel_button_click(location_window))

        #todo: aesthetics/making work with any city/state combo (TIGERweb Map Service for street names?)

    def on_close_button_click(self):
        self.on_closing()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            sys.exit(0)
            #since asyncio is still waiting for APILink, this is needed for a window close to be "proper"

    def on_refresh_button_click(self):
        self.root.after(100, lambda: asyncio.create_task(self.create_api_link(self.current_location)))

    def gui_update(self, day1data = "No Data", day1detailed_data = "No Data",
                   day2data = "No Data", day2detailed_data = "No Data",
                   day3data = "No Data", day3detailed_data = "No Data",
                   day4data = "No Data", day4detailed_data = "No Data",
                   day5data = "No Data", day5detailed_data = "No Data",
                   day6data = "No Data", day6detailed_data = "No Data",
                   day7data = "No Data", day7detailed_data = "No Data",
                   current_location = "None"):
        args = locals()
        #for easy dynamic referencing

        self.location_field.config(text="Displaying Results for: "
                                        + current_location["city"] + ", " + current_location["state"])

        for i in range(1,8):
            data = args[f"day{i}data"]
            detailed_data = args[f"day{i}detailed_data"]
            #dynamically obtain passed arguments
            setattr(self, f"day{i}data", data),
            getattr(self, f"day{i}forecast").config(text=data)
            setattr(self, f"day{i}detailed_data", detailed_data),
            setattr(self, f"day{i}detailed_forecast",
                    Hovertip(getattr(self, f"day{i}image"),
                             textwrap.fill(getattr(self, f"day{i}detailed_data"), width = 100)))

            if "Snow" in data:
                getattr(self, f"day{i}image").config(image=self.snowing_img)
            elif "Rain" in data:
                getattr(self, f"day{i}image").config(image=self.raining_img)
            elif "Hot" in data:
                getattr(self, f"day{i}image").config(image=self.hot_img)
            elif "Sunny" in data:
                getattr(self, f"day{i}image").config(image=self.sunny_img)
            elif "Clear" in data:
                getattr(self, f"day{i}image").config(image=self.clear_img)
            #a bit arbitrary, but matching images to potential deviation from "nice out" is IMO very useful

            if i == 1:
                getattr(self, f"day{i}text").config(text="Today")
            else:
                getattr(self, f"day{i}text").config(text=(datetime.now() + timedelta(days=i-1)).strftime('%a'))
            #as before, "Today" is "Today"

    def hold_click(self, event):
        self.x = event.x
        self.y = event.y

    def release_click(self, event):
        self.x = None
        self.y = None

    def move_window(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.root.winfo_y() + event.y - self.y
        self.root.geometry(f"+{x}+{y}")
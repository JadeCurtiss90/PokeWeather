import APILink, asyncio, json, os.path, PIL.ImageTk, platform, sys, textwrap
import tkinter as tk
from datetime import datetime, timedelta
from idlelib.tooltip import Hovertip
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
from StateAbbreviationDict import state_abbreviations

#this allows the detailed forecast hovertip to stay on top of z-order, even though the GUI is always on top itself
class OnTopHovertip(Hovertip):
    def showtip(self):
        super().showtip()
        self.tipwindow.attributes('-topmost', True)
        self.tipwindow.attributes()

class PokeWeatherGUI:
    def __init__(self):
        self.root = ThemedTk(className = "PokeWeather", theme = "yaru")
        #set window size
        self.root.geometry("800x150")
        #set initial window position
        self.root.geometry("-0-40")
        #set all other miscellaneous window properties
        self.root.overrideredirect(True)
        self.root.attributes("-alpha", .9)
        self.root.resizable(False,False)
        self.root.attributes('-topmost', True)
        #force immediate implementation of new properties
        self.root.update()

        #allows the window to be moved via drag and drop
        self.x = None
        self.y = None
        self.root.bind("<ButtonPress-1>", self.hold_click)
        self.root.bind("<ButtonRelease-1>", self.release_click)
        self.root.bind("<B1-Motion>", self.move_window)

        #keeps images in memory
        self.bg = PIL.ImageTk.PhotoImage(file=self.resource_path("bg.png"))
        self.bg2 = PIL.ImageTk.PhotoImage(file=self.resource_path("bg2.png"))
        self.clear_img = PIL.ImageTk.PhotoImage(file=self.resource_path("clear.png"))
        self.clear_night_img = PIL.ImageTk.PhotoImage(file=self.resource_path("clear_night.png"))
        self.cloudy_img = PIL.ImageTk.PhotoImage(file=self.resource_path("cloudy.png"))
        self.cloudy_night_img = PIL.ImageTk.PhotoImage(file=self.resource_path("cloudy_night.png"))
        self.sunny_img = PIL.ImageTk.PhotoImage(file=self.resource_path("sunny.png"))
        self.rainy_img = PIL.ImageTk.PhotoImage(file=self.resource_path("rainy.png"))
        self.stormy_img = PIL.ImageTk.PhotoImage(file=self.resource_path("stormy.png"))
        self.snowy_img = PIL.ImageTk.PhotoImage(file=self.resource_path("snowy.png"))
        self.bg_label = ttk.Label(self.root, image=self.bg, borderwidth=1, relief="sunken")

        #user's current location is polled first (slightly inaccurate)
        self.current_location = APILink.get_user_location()
        self.current_location["state"] = state_abbreviations[self.current_location["state"]]

        #select a pretty font based on the user's OS
        current_os = platform.system()
        if current_os == "Windows":
            self.font =  ("Segoe UI", 8)
        elif current_os == "Darwin":
            self.font = ("San Francisco", 8)
        else:
            self.font = ("Roboto", 8)

        #this is updated every time the API is called, so there's no reason to keep track of it
        current_datetime = datetime.now()

        #place the background label first , as everything else will go overtop it
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        #iterate through each day and set up its constituent components
        for i in range(1,8):
            setattr(self, f"day{i}data", "No Data")
            setattr(self, f"day{i}detailed_data", "No Data")
            setattr(self, f"day{i}temperature", "No Data")
            setattr(self, f"day{i}color", "#FFFFFF")
            setattr(self, f"day{i}frame", tk.Frame(self.bg_label, width=120, height=120, bg=getattr(self, f"day{i}color")))
            setattr(self, f"day{i}image", ttk.Label(getattr(self, f"day{i}frame"), image=self.sunny_img, background=getattr(self, f"day{i}color")))
            setattr(self, f"day{i}forecast", ttk.Label(getattr(self, f"day{i}frame"),
                                                      text=getattr(self, f"day{i}data"), wraplength=90,
                                                       justify="center", font=(self.font[0],7),
                                                       background=getattr(self, f"day{i}color")))
            setattr(self, f"day{i}temperature_label", ttk.Label(getattr(self, f"day{i}frame"),
                                                      text=getattr(self, f"day{i}temperature") + "°F",
                                                        justify="center", font=self.font,
                                                        background=getattr(self, f"day{i}color")))
            setattr(self, f"day{i}detailed_forecast",
                    OnTopHovertip(getattr(self, f"day{i}image"),
                             textwrap.fill(getattr(self, f"day{i}detailed_data"), width = 100)))
            #it's customary for any weather report to explicitly indicate today as "Today" and not the day
            if i == 1:
                setattr(self, f"day{i}text", ttk.Label(getattr(self, f"day{i}frame"),
                                                  text="Today", font=self.font,
                                                       background=getattr(self, f"day{i}color")))
            else:
                setattr(self, f"day{i}text", ttk.Label(getattr(self, f"day{i}frame"),
                                                  text=(current_datetime + timedelta(days=i-1)).strftime('%a'),
                                                       font=self.font,
                                                       background=getattr(self, f"day{i}color")))

            #place all initialized components in the root frame
            getattr(self, f"day{i}image").place(relx = .5, rely = .275, anchor = "n")
            getattr(self, f"day{i}forecast").place(relx = .5, rely = .79, anchor = "center")
            getattr(self, f"day{i}text").place(relx = .5, rely = .01, anchor = "n")
            getattr(self, f"day{i}temperature_label").place(relx = .5, rely = .13, anchor = "n")
            getattr(self, f"day{i}frame").place(relx = ((i-1)*2/14)+.015, relwidth = (1/8)-.01,
                                                relheight= .81, rely = .43, anchor = "w")
        #set up buttons
        self.location_button = tk.Button(text="Select Location", relief="ridge", borderwidth=1)
        self.location_field = tk.Label(text="Displaying Results for: None", font=self.font)
        self.refresh_button = tk.Button(text="Refresh", relief="ridge", borderwidth=1)
        self.close_button = tk.Button(text="Close", relief="ridge", borderwidth=1)

        #place buttons
        self.location_button.place(relx=(1/4)+.0335, rely=.999, anchor="s")
        self.location_field.place(relx=.5, rely=.999, anchor="s")
        self.refresh_button.place(relx=(3/4)-.035, rely=.99, anchor="s")
        self.close_button.place(relx=.858, rely=.999, anchor="s")

        #set commands for buttons
        self.location_button.config(command=self.on_location_button_click)
        self.refresh_button.config(command=self.on_refresh_button_click)

        #this does the same thing as closing the window, so it can be linked to the same function
        self.close_button.config(command=self.on_closing)

        #set window close protocol
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())

    #connects to relevant APIs and polls data
    async def create_api_link(self, location):
        #get all weather data for area
        data = APILink.get_api_data("https://api.weather.gov", "pokeweatherkey",
                                "/points/" + str(location["latitude"]) + "," + str(location["longitude"]))
        parsed_data = json.loads(data.text)
        #get 7-day forecast for area
        forecast = APILink.get_api_data(parsed_data["properties"]["forecast"], "pokeweatherkey")
        parsed_forecast = json.loads(forecast.text)

        #the API provides 1-2 datasets for each day: "day" and "night". If it's currently night, the current day
        #(and only the current day) will only have a "night" entry. All other days will have both

        #if it's daytime, the same day will have a nighttime forecast
        if parsed_forecast["properties"]["periods"][0]["isDaytime"]:
            self.gui_update(parsed_forecast["properties"]["periods"][0]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][0]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][0]["temperature"],
                                       parsed_forecast["properties"]["periods"][2]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][2]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][2]["temperature"],
                                       parsed_forecast["properties"]["periods"][4]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][4]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][4]["temperature"],
                                       parsed_forecast["properties"]["periods"][6]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][6]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][6]["temperature"],
                                       parsed_forecast["properties"]["periods"][8]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][8]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][8]["temperature"],
                                       parsed_forecast["properties"]["periods"][10]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][10]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][10]["temperature"],
                                       parsed_forecast["properties"]["periods"][12]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][12]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][12]["temperature"],
                                       location, "day")
        #if there's at least two forecasts for the same first day in the forecast AND if it's not daytime,
        #it's very early in the morning, and therefore the first forecast can be skipped entirely
        elif parsed_forecast["properties"]["periods"][1]["name"] == datetime.now().strftime('%A'):
            self.gui_update(parsed_forecast["properties"]["periods"][1]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][1]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][1]["temperature"],
                                       parsed_forecast["properties"]["periods"][3]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][3]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][3]["temperature"],
                                       parsed_forecast["properties"]["periods"][5]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][5]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][5]["temperature"],
                                       parsed_forecast["properties"]["periods"][7]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][7]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][7]["temperature"],
                                       parsed_forecast["properties"]["periods"][9]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][9]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][9]["temperature"],
                                       parsed_forecast["properties"]["periods"][11]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][11]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][11]["temperature"],
                                       parsed_forecast["properties"]["periods"][13]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][13]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][13]["temperature"],
                                       location, "day")
        #otherwise, it's night and before midnight, so "Today" will get the first forecast, and "Tomorrow" the 2nd
        else:
            self.gui_update(parsed_forecast["properties"]["periods"][0]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][0]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][0]["temperature"],
                                       parsed_forecast["properties"]["periods"][1]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][1]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][1]["temperature"],
                                       parsed_forecast["properties"]["periods"][3]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][3]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][3]["temperature"],
                                       parsed_forecast["properties"]["periods"][5]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][5]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][5]["temperature"],
                                       parsed_forecast["properties"]["periods"][7]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][7]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][7]["temperature"],
                                       parsed_forecast["properties"]["periods"][9]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][9]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][9]["temperature"],
                                       parsed_forecast["properties"]["periods"][11]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][11]["detailedForecast"],
                                       parsed_forecast["properties"]["periods"][11]["temperature"],
                                       location, "night")

    def on_cancel_button_click(self, window):
        window.destroy()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            sys.exit(0)

    def on_confirm_button_click(self, city, state, window):
        new_coordinates = APILink.get_coordinates(city.get(), state.get())
        #if the default location is polled (likely due to an error), this catches it and aborts the GUI update
        if new_coordinates[0] is None:
            messagebox.showerror("Error", "No valid location found! Please try again.")
            return
        #some of this data is never used by this app, so dummy data is fine in those fields
        new_location =  {"country_code": "US",
                         "country_name": "United States",
                         "city": new_coordinates[0].title(),
                         "postal": "00000",
                         "latitude": new_coordinates[1],
                         "longitude": new_coordinates[2],
                         "IPv4": "0.0.0.0",
                         "state": state.get()}
        self.current_location = new_location
        self.root.after(100, lambda: asyncio.create_task(self.create_api_link(self.current_location)))
        window.destroy()

    def on_location_button_click(self):
        #create new window with location entry fields and buttons
        location_window = tk.Toplevel(self.root)
        location_window.overrideredirect(True)
        location_window.title("Select Location")
        location_window.geometry("300x200")
        location_window.attributes('-topmost', True)
        location_window.update()

        #place the window directly in the center of the screen, as ostensibly the user wants to use it right now
        location_window.update_idletasks()
        x = (location_window.winfo_screenwidth()//2) - (location_window.winfo_width()//2)
        y = (location_window.winfo_screenheight()//2) - (location_window.winfo_height()//2)
        location_window.geometry(f"+{x}+{y}")

        #initialize the constituent components of the select location window
        bg2_label = ttk.Label(location_window, image=self.bg2, borderwidth=1, relief="sunken")
        bg2_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        frame = tk.Frame(location_window,width=300, height=200)
        header = ttk.Label(frame, text="Select a city and state", font=(self.font[0], 20))
        city = ttk.Entry(frame, width=30, font=self.font)
        city_label = ttk.Label(frame, text="City", font=self.font)
        state = ttk.Combobox(frame, state='readonly', justify="center", width=3, font=self.font)
        state["values"] = list(state_abbreviations.keys())[:51]
        state.current(0)
        state_label = ttk.Label(frame, text="State", font=self.font)
        confirm_button = ttk.Button(frame, text="Confirm")
        cancel_button = ttk.Button(frame, text="Cancel")

        #place those components in their appropriate locations in the window
        frame.place(relx=.5, rely=.5, relwidth=.92, relheight=.92, anchor="center")
        header.place(relx=.5, rely=.1, anchor="n")
        city.place(relx=.37, rely=.55, anchor="s")
        city_label.place(relx=.37, rely=.65, anchor="s")
        state.place(relx=7/8, rely=.55, anchor="s")
        state_label.place(relx=7/8, rely=.65, anchor="s")
        confirm_button.place(relx=1/5, rely=.95, anchor="s")
        cancel_button.place(relx=4/5, rely=.95, anchor="s")

        #set up button commands
        confirm_button.config(command=lambda: self.on_confirm_button_click(city, state, location_window))
        cancel_button.config(command=lambda: self.on_cancel_button_click(location_window))

    def on_refresh_button_click(self):
        self.root.after(100, lambda: asyncio.create_task(self.create_api_link(self.current_location)))

    def gui_update(self, day1data = "No Data", day1detailed_data = "No Data", day1temperature = "No Data",
                   day2data = "No Data", day2detailed_data = "No Data", day2temperature = "No Data",
                   day3data = "No Data", day3detailed_data = "No Data", day3temperature = "No Data",
                   day4data = "No Data", day4detailed_data = "No Data", day4temperature = "No Data",
                   day5data = "No Data", day5detailed_data = "No Data", day5temperature = "No Data",
                   day6data = "No Data", day6detailed_data = "No Data", day6temperature = "No Data",
                   day7data = "No Data", day7detailed_data = "No Data", day7temperature = "No Data",
                   current_location = None, time_of_day = "day"):
        #for easy dynamic referencing
        args = locals()

        self.location_field.config(text="Displaying Results for: "
                                        + current_location["city"] + ", " + current_location["state"])
        #iterate through each day, one at a time
        for i in range(1,8):
            #dynamically obtain passed arguments
            data = args[f"day{i}data"]
            detailed_data = args[f"day{i}detailed_data"]
            temperature = args[f"day{i}temperature"]

            #set the local variables for each piece of information, then update the GUI to match
            setattr(self, f"day{i}data", data),
            getattr(self, f"day{i}forecast").config(text=data)
            setattr(self, f"day{i}temperature", temperature),
            getattr(self, f"day{i}temperature_label").config(text=str(temperature) + "°F"),
            setattr(self, f"day{i}detailed_data", detailed_data),
            setattr(self, f"day{i}detailed_forecast",
                    OnTopHovertip(getattr(self, f"day{i}image"),
                             textwrap.fill(getattr(self, f"day{i}detailed_data"), width = 100)))

            #iterate through the list linearly and choose an icon/color fitting the first keyword(s)
            #nighttime is only used for the current day, and is checked and assigned different icons/colors as relevant
            lowered_data_list = data.lower().split(" ")
            for word in lowered_data_list:
                if "rain" in word or "shower" in word:
                    #the notation for storms isn't uniform, so this just makes sure it's part of the first forecast
                    if data.rfind("storm") != -1 and not "then" in data[:data.rfind("storm")]:
                        if i == 1 and time_of_day == "night":
                            getattr(self, f"day{i}image").config(image=self.stormy_img)
                            setattr(self, f"day{i}color", "#DADAE4")
                            break
                        else:
                            getattr(self, f"day{i}image").config(image=self.stormy_img)
                            setattr(self, f"day{i}color", "#FBECCF")
                            break
                    else:
                        if i == 1 and time_of_day == "night":
                            getattr(self, f"day{i}image").config(image=self.rainy_img)
                            setattr(self, f"day{i}color", "#DADAE4")
                            break
                        else:
                            getattr(self, f"day{i}image").config(image=self.rainy_img)
                            setattr(self, f"day{i}color", "#D9EAF9")
                            break
                elif "snow" in word or "frost" in word:
                    if i == 1 and time_of_day == "night":
                        getattr(self, f"day{i}image").config(image=self.snowy_img)
                        setattr(self, f"day{i}color", "#DADAE4")
                        break
                    else:
                        getattr(self, f"day{i}image").config(image=self.snowy_img)
                        setattr(self, f"day{i}color", "#E9EEF7")
                        break
                elif "cloudy" in word or "fog" in word:
                    if i == 1 and time_of_day == "night":
                        getattr(self, f"day{i}image").config(image=self.cloudy_night_img)
                        setattr(self, f"day{i}color", "#DADAE4")
                        break
                    else:
                        getattr(self, f"day{i}image").config(image=self.cloudy_img)
                        setattr(self, f"day{i}color", "#EFF8E4")
                        break
                elif "sunny" in word:
                    if i == 1 and time_of_day == "night":
                        getattr(self, f"day{i}image").config(image=self.sunny_img)
                        setattr(self, f"day{i}color", "#DADAE4")
                        break
                    else:
                        getattr(self, f"day{i}image").config(image=self.sunny_img)
                        setattr(self, f"day{i}color", "#FBD9D7")
                        break
                elif "clear" in word:
                    if i == 1 and time_of_day == "night":
                        getattr(self, f"day{i}image").config(image=self.clear_night_img)
                        setattr(self, f"day{i}color", "#DADAE4")
                        break
                    else:
                        getattr(self, f"day{i}image").config(image=self.clear_img)
                        setattr(self, f"day{i}color", "#DDF4ED")
                        break

            #update the remaining GUI components
            getattr(self, f"day{i}frame").config(background=getattr(self, f"day{i}color"))
            getattr(self, f"day{i}image").config(background=getattr(self, f"day{i}color"))
            getattr(self, f"day{i}forecast").config(background=getattr(self, f"day{i}color"))
            getattr(self, f"day{i}text").config(background=getattr(self, f"day{i}color"))
            getattr(self, f"day{i}temperature_label").config(background=getattr(self, f"day{i}color"))

            #as before, "Today" is "Today"
            #by doing this again, the day displays should update properly on a new day on the next API poll"
            if i == 1:
                getattr(self, f"day{i}text").config(text="Today")
            else:
                getattr(self, f"day{i}text").config(text=(datetime.now() + timedelta(days=i-1)).strftime('%a'))

    #these three functions allow the window to be drag and dropped when clicked anywhere
    def hold_click(self, event):
        self.x = event.x
        self.y = event.y

    def release_click(self, _):
        self.x = None
        self.y = None

    def move_window(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.root.winfo_y() + event.y - self.y
        self.root.geometry(f"+{x}+{y}")

    #function to make standalone executable work with temporary filepath
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
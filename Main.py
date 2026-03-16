import APILink
from WeatherLightGui import WeatherLightGui
import asyncio, json
from async_tkinter_loop import async_mainloop

async def create_api_link(api, gui):
    while True:
        location = api.get_user_location()
        data = api.get_api_data("https://api.weather.gov", "weatherlighttestkey",
                                "/points/"+str(location["latitude"])+","+str(location["longitude"]))
        parsed_data = json.loads(data.text)
        forecast = api.get_api_data(parsed_data["properties"]["forecast"], "weatherlighttestkey")
        parsed_forecast = json.loads(forecast.text)
        if parsed_forecast["properties"]["periods"][0]["isDaytime"]:
            WeatherLightGui.gui_update(gui, parsed_forecast["properties"]["periods"][0]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][2]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][4]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][6]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][8]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][10]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][12]["shortForecast"])
        else:
            WeatherLightGui.gui_update(gui, parsed_forecast["properties"]["periods"][0]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][1]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][3]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][5]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][7]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][9]["shortForecast"],
                                       parsed_forecast["properties"]["periods"][11]["shortForecast"])
        #the API seems to provide 1-2 datasets for each day: "day" and "night". If it's night, the current day (and
        #only the current day) will only have a "night" entry. All other days will have both
        await asyncio.sleep(3600)
        #once an hour seems like a reasonable (if arbitrary) wait time
        #also this just instantiates everything again in the event the user physically moves in that hour

api = APILink
gui = WeatherLightGui()
gui.root.after(100, lambda: asyncio.create_task(create_api_link(api, gui)))
#running TKinter in parallel with other stuff is hard:(
async_mainloop(gui.root)
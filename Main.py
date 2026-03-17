import APILink
from WeatherLightGui import WeatherLightGui
import asyncio
from async_tkinter_loop import async_mainloop

gui = WeatherLightGui()
gui.root.after(100, lambda: asyncio.create_task(WeatherLightGui.create_api_link(gui,
 gui.current_location)))
#running TKinter in parallel with other stuff is hard:(
async_mainloop(gui.root)
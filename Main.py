import asyncio
from async_tkinter_loop import async_mainloop
from PokeWeatherGUI import PokeWeatherGUI

gui = PokeWeatherGUI()
gui.root.after(100, lambda: asyncio.create_task(PokeWeatherGUI.create_api_link(gui,
                                                                               gui.current_location)))
#running TKinter in parallel with other stuff is hard:(
async_mainloop(gui.root)
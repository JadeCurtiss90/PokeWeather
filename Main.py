import asyncio
from async_tkinter_loop import async_mainloop
from PokeWeatherGUI import PokeWeatherGUI

gui = PokeWeatherGUI()
#running TKinter in parallel with other stuff is hard:(
gui.root.after(100, lambda: asyncio.create_task(PokeWeatherGUI.create_api_link(gui,
                                                                               gui.current_location)))
async_mainloop(gui.root)
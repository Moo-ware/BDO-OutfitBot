import random
import asyncio
from resources.ui import *
from market.api_handler import APIHandler
import colorama

async def main():
    colorama.init()
    API = APIHandler()
    task_manager = backgroundTasks(API)
    await task_manager.initial_login_check()
    
    menu = mainMenu(task_manager, API)
    await menu.run()


if __name__ == "__main__":
    asyncio.run(main())
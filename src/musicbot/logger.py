import logging,sys,traceback,discord
from discord.ext import commands

date_format = '[%(asctime)s.%(msecs)03d][%(levelname)s] %(name)s - %(module)s - %(funcName)s: %(message)s'
root_logger = logging.getLogger()

if not "-l" in sys.argv: 
    with open("log.log","a") as log:log.write("")
    file_handler = logging.FileHandler("log.log","a",'utf-8')
    file_handler.setFormatter(logging.Formatter(date_format,'%y:%m:%d %H:%M:%S'))
    file_handler.setLevel(logging.INFO)
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

class error_handler():
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        def log_error(event_name,string):
            logging.error(f"\nIgnoring exception in {event_name}\n{string}")

        async def on_error(self, event_method: str, *args, **kwargs) -> None:
            event_method = f"{event_method} with arguments {args} | {kwargs}"
            log_error(event_method,traceback.format_exc())

logging.info("started")
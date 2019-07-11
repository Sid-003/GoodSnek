import config
from bot import GoodSnek

if __name__ == "__main__":
    bot = GoodSnek()
    bot.run(config.token)

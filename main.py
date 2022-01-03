from src.utils.configs.app_settings import get_settings
from src.controllers.bot import Bot

def main():
    Bot().run(get_settings().TOKEN)

if __name__ == "__main__":
    main()
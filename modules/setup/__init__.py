import os
import configparser
import sys


class Setup:
    def __init__(self) -> None:
        pass

    def start_config(self, config):
        default = 'default'
        config.add_section('default')

        bot_name = str(input("Enter Bot name (default=jarvis): ") or "jarvis")
        user_name = str(input("Enter User name (default=vivek): ") or "vivek")

        config[default]['bot_name'] = bot_name
        config[default]['user_name'] = user_name

        with open('./JARVIS/config/config.ini', 'w') as configfile:
            config.write(configfile)

        print("Setup Done")
        return True

    def setup_assistant(self):
        if not os.path.exists('config'):
            os.makedirs('./JARVIS/config')
        config = configparser.ConfigParser()

        if os.path.exists('config'):
            sure = str(
                input("Your current configuration will be deleted, are you sure (y/n): ") or "n")
            if sure == "n":
                print("No changes done")
                return False
            else:
                self.start_config(config)
        else:
            self.start_config(config)
        print("Setup DONE")
        print("Exiting from program, need restart after setup")
        sys.exit()

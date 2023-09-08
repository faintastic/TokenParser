from colorama import Fore, Style, init
from datetime import datetime
import time
import os
import ctypes

s = Fore.LIGHTBLUE_EX
r = Fore.WHITE
init(convert=True)

class Logger:
    def Sprint(tag: str, content: str, color):
        ts = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET}"
        print(Style.BRIGHT + ts + color + f" [{tag}] " + Fore.RESET + content + Fore.RESET)
    
    def Ask(tag: str, content: str, color):
        ts = f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{datetime.now().strftime('%H:%M:%S')}{Fore.RESET}"
        return input(Style.BRIGHT + ts + color + f" [{tag}] " + Fore.RESET + content + Fore.RESET)

class Parser:
    @staticmethod
    def findObject(object: str, seperator: str):
        if ":" in object:
            chosen = None
            split = object.split(seperator)
            for thing in split:
                if "@" not in thing and "." in thing and len(thing) > 30:
                    chosen = thing
                    break
            
            if chosen == None:
                Logger.Sprint("ERROR", f"Could not find token in object {s}input={r}{object}")
                return None
            else:
                return chosen
        else:
            return object
    
    @staticmethod
    def getAllContent(filename: str, seperator: str):
        value = []
        with open(filename, "r") as file:
            for line in file.readlines():
                content = line.strip()
                token = Parser.findObject(content, seperator)
                if token is not None:
                    value.append(token)
        return value
    
    @staticmethod
    def main():
        ctypes.windll.kernel32.SetConsoleTitleW("Token Parser | Developed by kova / api")
        seperator = Logger.Ask("INPUT", "What seperator are the tokens formatted in? (:, |, etc): ", Fore.CYAN)
        content = Parser.getAllContent("input.txt", seperator)
        filename = f"sorted-{datetime.now().strftime('%m.%d.%y-%H.%M')}.txt"
        hits = 0
        start = time.time()
        for data in content:
            Logger.Sprint("SUCCESS", f"Pulled token {s}token={r}{data[:25]}*****", Fore.GREEN)
            hits += 1
            with open(f"output/{filename}", "a") as file:
                file.write(data + "\n")
                file.close()
        with open("input.txt", "a") as file:
            file.truncate(0)
            file.close()
        end = time.time()
        elapsed = round(end - start, 2)
        Logger.Sprint("FINISHED", f"Finished parsing tokens {s}elapsed_time={r}{elapsed}s {s}hits={r}{hits}", Fore.YELLOW)

        Logger.Ask("EXIT", "Please press the \"Enter\" key to close the application", Fore.MAGENTA)
        os._exit(1)

if __name__ == "__main__":
    Parser.main()
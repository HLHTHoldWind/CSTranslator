import googletrans as tran
import keyboard
from httpcore import SyncHTTPProxy
import time
import pyperclip
import os
import urllib
import threading

BASE_PATH = "D:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\game\\csgo"

LOG_PATH = f"{BASE_PATH}\\csdm\\console.log"
if not os.path.exists(f"{BASE_PATH}\\csdm"):
    print("INGAME MODE")
    LOG_PATH = f"{BASE_PATH}\\console.log"
else:
    print("DEMO MODE")

KEY_W = ["[ALL]", "[CT]", "[T]"]

proxies = urllib.request.getproxies()
h_address = proxies["http"]

head = h_address.split("//")[0].rstrip(":")
a_p = h_address.split("//")[1]
address = a_p.split(":")[0]
port = a_p.split(":")[1]

http_proxy = SyncHTTPProxy((head.encode(), address.encode(), int(port), b''))
proxies = {'http': http_proxy, 'https': http_proxy}
trans = tran.Translator(service_urls=["translate.google.com"], proxies=proxies)
t_dsc = "en"
t_dsc2 = "zh-tw"
in_game = "en"

LANGUAGE_CODES = {"english": "en", "japanese": "ja", "chinese": "zh-cn", "zchinese": "zh-tw", "latin": "la",
                  "italian": "it", "french": "fr", "korean": "ko"}


def convert_en(string: str):
    translated = trans.translate(string, dest=t_dsc)
    translated2 = trans.translate(string, dest=t_dsc2)
    # src = translated.src
    # dest = translated.dest
    return translated, translated2


def translate(string):
    try:
        translated = trans.translate(string, dest=in_game)

        text = translated.text
        return text
    except ValueError:
        return ""


def self_translation():
    while True:
        if keyboard.is_pressed("f7"):
            keyboard.press_and_release("Ctrl+a")
            keyboard.press_and_release("Ctrl+c")
            time.sleep(0.05)
            text = pyperclip.paste()
            content = translate(text)
            pyperclip.copy(content)
            keyboard.press_and_release("Ctrl+v")

        time.sleep(0.1)


def main():
    global in_game
    content = ["awa"]
    tran_lines = []
    while True:
        with open(LOG_PATH, "rb") as file:
            f_content = file.readlines()
            if content[-1] != f_content[-1]:
                new_lines = f_content[len(content):]
                content = f_content

                for i in new_lines:
                    for x in KEY_W:
                        try:
                            texts = i.decode()
                            if x in texts:
                                text = ""
                                for a in texts.split(": ")[1:]:
                                    text += a
                                title = texts.split(": ")[0]
                                text = text.rstrip()

                                if "HoldWind" in title:
                                    if "/cmd" in text:
                                        command = text.split(" ")[1]
                                        if command == "set_lang":
                                            lang = text.split(" ")[2].strip().lower()
                                            if lang in LANGUAGE_CODES.keys():
                                                lang = LANGUAGE_CODES[lang]
                                            in_game = lang
                                    t_content = translate(text)
                                    pyperclip.copy(t_content)
                                    tran_text = title + ": " + text + "\n" + t_content
                                    print(tran_text)

                                else:

                                    tran1, tran2 = convert_en(text)
                                    tran_text = f"{title} (From {tran1.src}): {tran1.text}\n{tran2.text}"

                                    tran_lines.append(tran_text)
                                    print(tran_text)
                        except UnicodeDecodeError:
                            continue

        time.sleep(1)


if __name__ == '__main__':
    threading.Thread(target=self_translation).start()
    main()

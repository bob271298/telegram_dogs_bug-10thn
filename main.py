from linecache import cache
import time
from telegram import TelegramAppHOT, TelegramDogs
from loguru import logger
import random


def main_hot():
    telegram_app = TelegramAppHOT('D:\\DATA\\Python\\Tdata_unpack\\all_telegrams\\172\\+6283176166127\\Telegram.exe')
    # telegram_app.turn_on_webview_inspecting()
    telegram_app.launch_hot(10)
    telegram_app.open_dev_tools(10)


def main_dogs():
    TRIES_COUNT = 3
    
    
    with open('all_refs.txt', 'r', encoding='utf-8') as fileobj:
        ref_links = fileobj.readlines()

    with open('all_pathes.txt', 'r', encoding='utf-8') as fileobj:
        pathes_list = fileobj.readlines()

    for path in pathes_list:
        for i in range(TRIES_COUNT):
            try:
                if path.find('all_telegrams') != -1:
                    short_path = path[path.index('all_telegrams')+13:].strip()
                else:
                    short_path = path[-40:]

                if TelegramDogs.is_proxifier_running():
                    logger.info(f"Start account ...{short_path}")

                    ref_link = random.choice(ref_links).strip()
                    logger.info(f"Account referal: {ref_link[ref_link.index('?'):]}")

                    TelegramDogs.stop_telegram_processes()
                    time.sleep(1)
                    telegramDogs = TelegramDogs(path.strip())
                    telegramDogs.set_random_nicknames(10)
                    telegramDogs.launch_dogs(ref_link)
                    telegramDogs.work_with_dogs()
                    time.sleep(0.3)
                    telegramDogs.quit_telegram()
                    time.sleep(1)
                    break
                else:
                    logger.warning('Launch proxyfier firstly')
                    return 0
            except Exception as e:
                logger.error(f'Error: {str(e).strip()}')
                logger.warning(f"TRY {i+1}/{TRIES_COUNT}")
                if i+1 < TRIES_COUNT:
                    continue
                else:
                    with open('bad_accounts.txt', 'a', encoding='utf-8') as fileobj:
                        fileobj.write(path + '\n')
            finally:
                logger.info(f"Finish account ...{short_path}\n")
    input()



if __name__ == '__main__':
    logger.add("file.log", level="DEBUG")
    main_dogs()



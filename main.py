import time
from telegram import TelegramAppHOT, TelegramDogs


def main_hot():
    telegram_app = TelegramAppHOT('D:\\DATA\\Python\\Tdata_unpack\\all_telegrams\\172\\+6283176166127\\Telegram.exe')
    print('start')
    # telegram_app.turn_on_webview_inspecting()
    telegram_app.launch_hot(10)
    telegram_app.open_dev_tools(10)


def main_dogs():
    REF_LINK = 'https://t.me/dogshouse_bot/join?startapp=BZcgz52zTZGjJQQfe9NlPw'

    with open('all_pathes.txt', 'r', encoding='utf-8') as fileobj:
        pathes_list = fileobj.readlines()

    for i in pathes_list:
        if TelegramDogs.is_proxifier_running():
            TelegramDogs.stop_telegram_processes()
            telegramDogs = TelegramDogs(i.strip())
            telegramDogs.set_random_nicknames(10)
            telegramDogs.launch_dogs(REF_LINK)
            telegramDogs.work_with_dogs()
            time.sleep(0.3)
            telegramDogs.quit_telegram()
            time.sleep(1)
        else:
            print('launch proxyfier firstly')



if __name__ == '__main__':
    main_dogs()



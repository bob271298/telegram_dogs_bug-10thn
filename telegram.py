from pywinauto import Application
from pywinauto.mouse import scroll
from pywinauto import mouse
from pywinauto.keyboard import send_keys
from img_detection import *
import time
from random_word import RandomWords
import pyperclip
import psutil
from loguru import logger


class TelegramApp:
    x, y = 100, 100
    width, height = 800, 600

    def __init__(self, exe_path, wait_network_loading=True, time_to_wait=60):
        self.app = Application().start(exe_path)
        self.app.wait_cpu_usage_lower(threshold=5)

        self.main_window = self.app.top_window()

        self.main_window.move_window(x=self.x, y=self.y, width=self.width, height=self.height, repaint=True)

        if wait_network_loading:
            time.sleep(0.2)
            if not wait_while_img_dissapear(self.main_window, 'templates\\telegram\\network_loading.png', 0.5, time_to_wait*2, 0.95):
                raise Exception(f'Telegram not loaded in {time_to_wait} sec')
            logger.info('Telegram loaded successfully!')


    def get_window_center_coords(self, window):
        rect = window.rectangle()
        x = rect.left
        y = rect.top
        width = rect.width()
        height = rect.height()

        x_center = int(x + width / 2)
        y_center = int(y + height / 2)

        return x_center, y_center

    
    def scroll_to_click(self, dist, window, template_path, delay, tries_count, threshold, click=True):
        x, y = self.get_window_center_coords(self.main_window)

        window.set_focus()

        time.sleep(0.2)
        mouse.move(coords=(x, y))
        time.sleep(0.2)

        for i in range(dist):
            if i % 5 == 0:
                if click:
                    if click_on_img(window, template_path, delay, tries_count, threshold):
                        return True
                else:
                    if get_img_coords(window, template_path, delay, tries_count, threshold):
                        return True
            send_keys('{DOWN}')
            time.sleep(0.01)
        return False


    def key_cycle(self, window, key, count, delay):
        window.set_focus()
        for i in range(count):
            send_keys(key)
            time.sleep(delay)


    def turn_on_webview_inspecting(self):
        click_on_img(self.main_window, 'templates\\telegram\\burger_menu.png', 0.5, 5, 0.7)
        click_on_img(self.main_window, 'templates\\telegram\\settings.png', 0.5, 5, 0.7)
        click_on_img(self.main_window, 'templates\\telegram\\advanced.png', 0.5, 5, 0.9)

        self.scroll_to_click(60, self.main_window, 'templates\\telegram\\exp_settings.png', 0, 1, 0.9)

        if self.scroll_to_click(50, self.main_window, 'templates\\telegram\\inspection.png', 0, 1, 0.9, click=False):
            if click_on_img(self.main_window, 'templates\\telegram\\inspection_off.png', 0.5, 5, 0.9):
                logger.info('Webview inspecction ON!')
            elif get_img_coords(self.main_window, 'templates\\telegram\\inspection_on.png', 0.5, 5, 0.9):
                logger.info('Webview inspecction already ON!')
            else:
                logger.info('Inspection not found!')

        self.key_cycle(self.main_window, '{ESC}', 4, 0.05)


    def enter_new_text(self, nickname, delay=0.2):
        time.sleep(delay)
        send_keys("^a")
        time.sleep(delay)
        send_keys("{BACKSPACE}")
        time.sleep(delay)
        send_keys(nickname)


    def set_nickname(self, nickname, delay=0.2, change_if_already_set=False):
        click_on_img(self.main_window, 'templates\\telegram\\burger_menu.png', 0.5, 5, 0.7)
        click_on_img(self.main_window, 'templates\\telegram\\settings.png', 0.5, 5, 0.7)
        click_on_img(self.main_window, 'templates\\telegram\\my_account.png', 0.5, 5, 0.9)
        click_on_img(self.main_window, 'templates\\telegram\\change_username.png', 0.5, 5, 0.9)

        if not change_if_already_set and not get_img_coords(self.main_window, 'templates\\telegram\\empty_username.png', 0.5, 5, 0.9):
            logger.info('Username already setted!')
            self.key_cycle(self.main_window, '{ESC}', 4, 0.05)
            return True

        self.enter_new_text(nickname, delay)
        time.sleep(delay * 3)

        if get_img_coords(self.main_window, 'templates\\telegram\\username_available.png', 0.5, 10, 0.9):
            if click_on_img(self.main_window, 'templates\\telegram\\save.png', 0.5, 5, 0.8):
                logger.info('Username successfully setted!')
                self.key_cycle(self.main_window, '{ESC}', 4, 0.05)
                return True
        
        raise Exception('Username do not setted!')
    

    def write_to_saved_messages(self, message, delay=0.2):
        time.sleep(delay)
        send_keys("^0")
        pyperclip.copy(message)
        time.sleep(delay)
        send_keys("^v")
        time.sleep(delay)
        send_keys("{ENTER}")

    def quit_telegram(self):
        self.main_window.set_focus()
        time.sleep(0.5)
        send_keys('^q')
        logger.info("Telegram closed with ^q.")

    
    @staticmethod
    def stop_telegram_processes():
        for process in psutil.process_iter(['pid', 'name']):
            try:
                if 'Telegram' in process.info['name']:
                    p = psutil.Process(process.info['pid'])
                    p.terminate()
                    p.wait()
                    logger.warning(f"Telegram process - PID {process.info['pid']} was stopped.")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    
    @staticmethod
    def is_proxifier_running():
        for process in psutil.process_iter(['name']):
            if process.info['name'] == 'Proxifier.exe':
                return True
        return False


class TelegramDogs(TelegramApp):
    def __init__(self, exe_path):
        super().__init__(exe_path)
        self.dogs_window = None


    def get_random_word_with_length(self, min_length, max_length):
        r = RandomWords()
        while True:
            word = r.get_random_word()
            if min_length <= len(word) <= max_length:
                return word


    def get_nickname(self):
        word1 = self.get_random_word_with_length(3,5)
        word2 = self.get_random_word_with_length(3,5)
        nickname = f"{word1}{word2}"
        return nickname
    

    def set_random_nicknames(self, tries_count=5, delay=0.2):
        for i in range(tries_count):
            if self.set_nickname(self.get_nickname(),delay):
                break

    
    def launch_dogs(self, link, sleep_before_launch=3, tries_count=30):
        time.sleep(2)
        old_windows = list(self.app.windows())

        for i in range(tries_count):
            self.write_to_saved_messages(link)
            time.sleep(sleep_before_launch)
            if click_on_img(self.main_window, 'templates\\dogs\\launch.png', 0.5, 2, 0.9):
                break

        for i in range(tries_count):
            if get_img_coords(self.main_window, 'templates\\dogs\\allow_msg.png', 0.5, 10, 0.9):
                click_on_img(self.main_window, 'templates\\dogs\\OK.png', 0.5, 5, 0.9)

            new_windows = list(self.app.windows())
            if len(new_windows) > len(old_windows):
                unique_windows = [w for w in new_windows if w not in old_windows]
                self.dogs_window = unique_windows[0]
                if self.dogs_window:
                    logger.info('Dogs window successfully launched!')
                    return True
            time.sleep(1)

        raise Exception('Dogs window do not launched.')
    

    def work_with_dogs(self):
        if not click_on_img(self.dogs_window, 'templates\\dogs\\start_dogs.png', 0.5, 60, 0.9):
            raise Exception('First button on Dogs not found!')
        time.sleep(8)
        click_on_img(self.dogs_window, 'templates\\dogs\\continue_blue.png', 0.5, 40, 0.9)
        click_on_img(self.dogs_window, 'templates\\dogs\\continue_white.png', 0.5, 40, 0.9)
        if not click_on_img(self.dogs_window, 'templates\\dogs\\continue_white.png', 0.5, 40, 0.9):
            raise Exception('Last button on Dogs not found!')
        logger.info('Dogs successfully claimed!')





class TelegramAppHOT(TelegramApp):
    def __init__(self, exe_path):
        super().__init__(exe_path)
        self.hot_window = None
        self.dev_tools_window = None


    def launch_hot(self, tries_count):
        time.sleep(2)
        old_windows = list(self.app.windows())

        for i in range(tries_count):
            send_keys("HOT{SPACE}Wallet")
            time.sleep(0.5)
            send_keys("{ENTER}")
            time.sleep(0.5)
            if click_on_img(self.main_window, 'templates\\hot\\launch_hot.png', 0.5, 5, 0.9):
                break
            send_keys("{ESC}")
            time.sleep(1)

        for i in range(tries_count):
            new_windows = list(self.app.windows())

            if len(new_windows) > len(old_windows):
                unique_windows = [w for w in new_windows if w not in old_windows]
                self.hot_window = unique_windows[0]
                if self.hot_window:
                    print('HOT launched successfully!')
                    break
            time.sleep(1)


    def open_dev_tools(self, wait):         #do not work
        if self.hot_window is None:
            print('No HOT window!')
            return 0
        
        old_windows = list(self.app.windows())
        # self.get_windows_print()

        click_on_img(self.hot_window, 'templates\\hot\\main_page_arrow.png', 0.5, 5, 0.9)   #mb hot_window problem
        time.sleep(0.5)
        send_keys("{F12}")
        time.sleep(1)

        
        # self.dev_tools_window = self.app.top_window()
        # print('-'*30)
        # self.get_windows_print()
        print('-'*30)
        childrens = self.hot_window.children()
        for window in childrens:
            if window.class_name() == "Chrome_WidgetWin_1":
                devtools_window = window
                break

        if devtools_window:
            print(f"DevTools window found: {devtools_window.window_text()}")
            devtools_window.move_window(x=100, y=100, width=800, height=600, repaint=True)

        # for i in range(wait):                     
        #     new_windows = list(self.app.windows())
        #     if len(new_windows) > len(old_windows):
        #         print('+1 window')
        #         unique_windows = [w for w in new_windows if w not in old_windows]
        #         self.dev_tools_window = unique_windows[0]
        #         if self.dev_tools_window:
        #             print('Dev Tools launched successfully!')
        #             break
        #     time.sleep(1)
        

    def get_windows_print(self):
        for i in self.app.windows():
            print(f"Title: {i.window_text()}")
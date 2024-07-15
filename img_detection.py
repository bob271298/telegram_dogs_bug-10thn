from asyncio.windows_events import NULL
from re import L
import time
from PIL import ImageGrab
import numpy as np
import cv2
import random


def get_window_screenshot(window_rect):
    x, y = window_rect.left, window_rect.top
    width, height = window_rect.width(), window_rect.height()

    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    return screenshot


def get_search_on_image(screenshot, template_path, threshold):
    img_np = np.array(screenshot)

    # Завантаження шаблону і конвертація до потрібного формату
    template_rgb = cv2.imread(template_path, cv2.IMREAD_COLOR)
    template = cv2.cvtColor(template_rgb, cv2.COLOR_RGB2BGR)

    # Пошук відповідностей шаблону
    res = cv2.matchTemplate(img_np, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(res >= threshold)

    # Масив для зберігання координат знайдених збігів
    match_coordinates = []

    # Маска для відстеження знайдених збігів
    match_mask = np.zeros_like(res, dtype=np.uint8)

    # Проходимо по всім знайденим збігам
    for pt in zip(*loc[::-1]):
        x, y = pt

        # Визначаємо ROI (регіон інтересу) для перевірки наявності збігів
        roi = match_mask[y:y+template.shape[0], x:x+template.shape[1]]

        # Перевіряємо, чи є вже знайдений збіг в ROI
        if np.any(roi):
            # Якщо так, переходимо до наступного збігу
            continue

        # Додаємо знайдений збіг до списку координат
        bottom_right = (x + template.shape[1], y + template.shape[0])
        match_coordinates.append((pt, bottom_right))

        # Позначаємо знайдений збіг на масці
        match_mask[y:y+template.shape[0], x:x+template.shape[1]] = 255

    # # Малюємо прямокутники на оригінальному скріншоті
    # result_img = img_np.copy()
    # for pt1, pt2 in match_coordinates:
    #     cv2.rectangle(result_img, pt1, pt2, (0, 0, 255), 1)

    # print(len(match_coordinates))

    # # Відображаємо скріншот з результатами
    # cv2.imshow('Result', result_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return match_coordinates


def get_lt_rb_center_point(points_tuple):
    lt, rb = points_tuple

    x = (rb[0] - lt[0]) / 2 + lt[0]
    y = (rb[1] - lt[1]) / 2 + lt[1]
    return (x, y)


def get_img_coords(window, template_path, delay, tries_count, threshold, return_random=False):
    for i in range(tries_count):
        window_screenshot = get_window_screenshot(window.rectangle())
        data = get_search_on_image(window_screenshot, template_path, threshold)
        if data is None or len(data) <= 0:
            time.sleep(delay)
            continue
        else:
            if len(data) > 1 and return_random:
                button_points = data[random.randint(0, len(data)-1)]
            else:
                button_points = data[0]
            x, y = get_lt_rb_center_point(button_points)
            return (x, y)
        
    return False


def wait_while_img_dissapear(window, template_path, delay, tries_count, threshold):
    for i in range(tries_count):
        if not get_img_coords(window, template_path, 0, 1, threshold):
            return True
        time.sleep(delay)
    return False


def click_on_img(window, template_path, delay, tries_count, threshold) -> None:
    point = get_img_coords(window, template_path, delay, tries_count, threshold)
    if point:
        window.click_input(coords=(int(point[0]), int(point[1])))
        return True
    return False


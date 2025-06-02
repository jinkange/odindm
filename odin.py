import win32gui
import win32con
import time
import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab

def enum_windows_by_class_and_title(class_name, title):
    hwnds = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            window_class = win32gui.GetClassName(hwnd)
            window_title = win32gui.GetWindowText(hwnd)
            if window_class == class_name and window_title == title:
                hwnds.append(hwnd)

    win32gui.EnumWindows(callback, None)
    return hwnds

def move_resize_window(hwnd, x, y, width, height):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.MoveWindow(hwnd, x, y, width, height, True)

def click_on_window(hwnd, rel_x, rel_y):
    rect = win32gui.GetWindowRect(hwnd)
    abs_x = rect[0] + rel_x
    abs_y = rect[1] + rel_y
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    pyautogui.click(abs_x, abs_y)

def mouse_drag(start_x, start_y, end_x, end_y, duration=0.2):
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=duration)
    pyautogui.mouseUp()
    
def click_image(image_path, confidence=0.8):
    location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
    if location:
        pyautogui.click(location)
        print(f"이미지 클릭 성공: {location}")
    else:
        print("이미지 찾지 못함.")

def scroll_on_window(hwnd, amount):
    rect = win32gui.GetWindowRect(hwnd)
    center_x = rect[0] + (rect[2] - rect[0]) // 2
    center_y = rect[1] + (rect[3] - rect[1]) // 2

    pyautogui.moveTo(center_x, center_y)
    pyautogui.scroll(amount)  # 양수: 위로, 음수: 아래로

region = (0, 0, 960, 540)
# region = (960, 0, 960, 540)
def image_exists_at_region(template_path, region, threshold=0.9):
    """
    특정 좌표(region) 내에서 이미지(template_path)가 존재하는지 판별
    :param template_path: 찾을 이미지 경로 (예: "dungeon_icon.png")
    :param region: (x, y, width, height) 영역
    :param threshold: 유사도 임계값 (0~1 사이, 높을수록 정밀)
    :return: True (존재함) / False (존재 안 함)
    """
    # 화면에서 특정 영역만 캡처
    x, y, w, h = region
    screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    screenshot_np = np.array(screenshot.convert("RGB"))
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

    # 템플릿 이미지 불러오기 및 흑백 변환
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"템플릿 이미지 로드 실패: {template_path}")
        return False

    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    return len(loc[0]) > 0

def click_if_image_found(template_path, region, threshold=0.9, delay=0.3):
    """
    특정 화면 영역(region)에서 이미지가 있으면 클릭
    :param template_path: 비교할 이미지 파일 경로
    :param region: (x, y, width, height) - 검색 범위
    :param threshold: 매칭 유사도 (0~1), 높을수록 정확
    :param delay: 클릭 후 대기 시간
    :return: True (찾아서 클릭함), False (못 찾음)
    """
    x, y, w, h = region
    # 지정 범위 스크린샷
    screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    screenshot_np = np.array(screenshot.convert("RGB"))
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

    # 템플릿 이미지 로드
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"[오류] 이미지 불러오기 실패: {template_path}")
        return False

    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        click_x = x + max_loc[0] + template.shape[1] // 2
        click_y = y + max_loc[1] + template.shape[0] // 2
        pyautogui.moveTo(click_x, click_y)
        pyautogui.click()
        time.sleep(delay)
        return True
    return False
# 정확한 제목: 띄어쓰기 포함 "ODIN  "
odin_windows = enum_windows_by_class_and_title("UnrealWindow", "ODIN  ")

if len(odin_windows) >= 2:
    move_resize_window(odin_windows[0], 0, 0, 960, 540)
    # move_resize_window(odin_windows[1], 960, 0, 960, 540)
    print("ODIN 창 위치 조정 완료")
    # mouse_drag(472, 263, 763, 252)
    # time.sleep(1)
    # pyautogui.click(923, 43)
    # time.sleep(1)
    # pyautogui.click(801, 365)
    # scroll_on_window(odin_windows[1], -500)
    # 예시 클릭 (첫 번째 클라이언트의 300,400 위치)
    # click_on_window(odin_windows[0], 300, 400)
    template_path = "dungeon_icon.png"
    if image_exists_at_region(template_path, region):
        print("던전 아이콘이 존재합니다.")
    else:
        print("던전 아이콘이 없습니다.")
    
    print("클릭 완료")

coords = {
    "메뉴": (923, 43),
    "캐릭터선택": {
        "버튼": (801, 365),
        "1번": (838, 79),
        "2번": (840, 152),
        "3번": (831, 197),
        "4번": (834, 262),
        "5번": (845, 321),
        "게임시작": (851, 499)
    },
    "팝업확인": (518, 331),
    "홈버튼": (20, 187),
    "은총의 순간이동": (25, 133),
    "메뉴-던전": (761, 258),
    "정예던전": (166, 77),
    "장비": (881, 43),
    "모두해제버튼": (899, 510),
    "창고": {
        "버튼": (752, 491),
        "보관버튼": (None, None)  # 좌표 없음 - 필요시 채우세요
    },
    "인벤토리아이템": [
        (730, 125), (778, 125), (823, 125), (869, 125), (920, 125),
        (730, 174), (778, 174), (823, 174), (869, 174), (920, 174),
        (730, 217), (778, 217), (823, 217), (869, 217), (920, 217),
        (730, 267), (778, 267), (823, 267), (869, 267), (920, 267),
    ],
    "창고아이템": [
        (39, 160), (87, 160), (140, 160), (176, 160),
        (45, 212), (94, 212), (133, 212), (185, 212),
        (34, 257), (94, 257), (133, 257), (185, 257),
        (34, 308), (94, 308), (133, 308), (185, 308),
        (34, 351), (94, 351), (133, 351), (185, 351),
    ]
}

MAX_CHARACTERS = 5
current_char_index = 0

def main():
    wake_up_if_sleep_mode()
    ensure_in_game_mode()

    while True:
        move_to_character_select_screen()

        for i in range(MAX_CHARACTERS):
            current_char_index = i + 1
            move_to_character_slot(current_char_index)

            if has_dungeon_time():
                if has_items():
                    enter_dungeon_and_auto_hunt()
                    while not is_out_of_dungeon():
                        wait(60)
                    continue  # 던전 끝나면 다시 3.1로 돌아감
                else:
                    return_to_town()
                    open_storage()
                    if storage_has_equipment():
                        retrieve_and_equip_equipment()
                        continue  # 다시 3.1.1로
                    else:
                        stop_macro("장비 없음")
                        return
            else:  # 던전 시간 없음
                if has_items():
                    return_to_town()
                    unequip_all()
                    open_storage()
                    store_equipment()
                    continue  # 다음 조건 확인 (3.2로)
                else:
                    if current_char_index < MAX_CHARACTERS:
                        continue  # 다음 캐릭터로 (3.2.2.1)
                    else:
                        break  # 모든 캐릭터 순회 완료

        # 5번째 캐릭터까지 완료 후 루프
        move_to_character_slot(1)
        open_storage()
        retrieve_hunting_equipment()
        move_to_hunting_spot()
        start_auto_hunt()

        # 필요시 wait 또는 break 넣기
        wait(600)  # 10분마다 루프 또는 조건에 따라 종료

# === 기능 구현 자리 (좌표 기반 구현 필요) ===
def wake_up_if_sleep_mode():
    if(image_exists_at_region('./images/절전모드.png', region)):
        mouse_drag(472, 263, 763, 252)
    pass

def ensure_in_game_mode():
    if(image_exists_at_region('./images/ingame.png', region)):
        return True
    else: return False
    
def in_game_waiting():
    while True:
        if(image_exists_at_region('./images/ingame.png', region)):
            break
        time.sleep(1)
        
def move_to_character_select_screen():
    if(not image_exists_at_region('./images/메뉴창켜짐확인.png', region)):
        click(coords["메뉴"])
    
    click(coords["캐릭터선택"])
    click(coords["팝업"])
    pass

def move_to_character_slot(index):
    print(f"{index}번째 캐릭터로 이동")
    click(coords["캐릭터선택"][f"{index}번"])
    click(coords["캐릭터선택"]["선택"])
    in_game_waiting()
    
def has_dungeon_time():
    if(not image_exists_at_region('./images/메뉴창켜짐확인.png', region)):
        click(coords["메뉴"])
    click(coords["메뉴-던전"])
    click(coords["정예던전"])
    #마우스 스크롤 필요할수 있음
    if(not image_exists_at_region('./images/난쟁이 비밀통로 소모.png', region)):
        click(coords["메뉴"])
        return True
    if(not image_exists_at_region('./images/공허의유적소모.png', region)):
        click(coords["메뉴"])
        return True
    click(coords["메뉴"])
    return False

def has_items():
    click(coords["장비"])
    if(not image_exists_at_region('./images/장비 미장착확인1.png', region)):
        click(coords["메뉴"])
        return True
    if(not image_exists_at_region('./images/장비 미장착확인2.png', region)):
        click(coords["메뉴"])
        return True
    click(coords["메뉴"])
    return False

def enter_dungeon_and_auto_hunt():
    click("enter_dungeon_button")
    wait(3)
    click("start_auto_hunt")

def is_out_of_dungeon():
    return image_exists("out_of_dungeon_ui")

def return_to_town():
    click("return_town_button")
    wait(3)

def open_storage():
    click("open_storage_button")
    wait(2)

def storage_has_equipment():
    return image_exists("storage_equipment_icon")

def retrieve_and_equip_equipment():
    click("equipment_in_storage")
    click("equip_button")
    wait(1)

def stop_macro(reason):
    print(f"[작동 중지] {reason}")

def unequip_all():
    click("character_panel")
    click("unequip_all_button")

def store_equipment():
    click("equipment")
    click("store_to_storage_button")

def retrieve_hunting_equipment():
    click("storage_hunting_equipment")
    click("equip_button")

def move_to_hunting_spot():
    click("map_icon")
    click("hunting_spot_location")

def start_auto_hunt():
    click("auto_hunt_button")

def click(button_name):
    print(f"{button_name} 클릭")  # 실제 좌표 클릭 함수로 구현
    time.sleep(0.5)

def image_exists(image_name):
    # 실제 이미지 탐지 로직 구현 필요
    return True  # 테스트용 기본값

def wait(seconds):
    import time
    time.sleep(seconds)

# === 시작 ===
if __name__ == "__main__":
    main()


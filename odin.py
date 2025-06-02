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

def scroll_on_window(x, y, amount):
    pyautogui.moveTo(x, y)
    pyautogui.scroll(amount)  # 양수: 위로, 음수: 아래로

region = (0, 0, 960, 540)
# region = (960, 0, 960, 540)
def image_exists_at_region(template_path, region, threshold=0.98):
    """
    template_path: 찾을 이미지 파일 경로
    region: (x, y, width, height)1281 631
    threshold: 일치 정도 (0.0 ~ 1.0)
    """
    screenshot = pyautogui.screenshot(region=region)
    # screenshot = screenshot_all_monitors()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    max_val = np.max(result)
    print(f"{template_path}찾기 :{max_val}")
    return max_val >= threshold
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


coords = {
    "메뉴": (923, 43),
    "메뉴-캐릭터변경": (798,364),
    "1번": (838, 79),
    "2번": (840, 152),
    "3번": (831, 197),
    "4번": (834, 262),
    "5번": (845, 321),
    "게임시작": (851, 499),
    "팝업확인": (518, 331),
    "마을귀환": (30, 187),
    "순간이동": (378, 494),
    "은총의 순간이동":(424,495),
    "은총첫번쨰사냥터": (199, 173),
    "자동사냥": (904,430),
    "메뉴-던전": (761, 258),
    "정예던전": (166, 77),
    "정예던전스크롤위치": (315,183),
    "공허의유적": (401, 296),
    "공허의유적5단계": (135,239),
    "난쟁이비밀통로": (614,270),
    "난쟁이비밀통로5단계": (101,243),
    "던전이동": (855,499),
    "던전이동확인팝업": (514,332),
    "장비창": (881, 43),
    "모두해제버튼": (899, 510),
    "창고바로가기": (752, 491),
    "창고보관버튼": (881,508),
    "창고꺼내기버튼": (170,506),
    "자동장착": (902,511),
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

MAX_CHARACTERS = 2
current_char_index = 0

def main():
    wake_up_if_sleep_mode()
    ensure_in_game_mode()
    
    isFine = True
    isNext = False
    for i in range(MAX_CHARACTERS):
        if(not isFine): break
        False = True
        current_char_index = i + 1
        move_to_character_select_screen()
        move_to_character_slot(current_char_index)
        while isNext:
            if has_dungeon_time(): #3.1
            # if not has_dungeon_time(): #3.1 던전 시간있어도 없게 테스트
                if has_items():
                    while has_dungeon_time():
                        enter_dungeon_and_auto_hunt()
                        while not is_out_of_dungeon():
                            wait(60)
                        continue  # 던전 끝나면 다시 3.1로 돌아감
                    break
                else:
                    open_storage()
                    if retrieve_and_equip_equipment():
                        continue  # 다시 3.1.1로
                    else:
                        #아이템 없음 찾기실패 매크로 종료
                        print("아이템 찾기 실패 매크로 종료")
                        isFine = False
                        break
                
            else:  # 던전 시간 없음
                if has_items():
                    return_to_town()
                    unequip_all()
                    open_storage()
                    store_equipment()
                    continue  # 다음 조건 확인 (3.2로)
                else:
                    if current_char_index < MAX_CHARACTERS:
                        isNext = False
                        continue  # 다음 캐릭터로 (3.2.2.1)
                    else:
                        break  # 모든 캐릭터 순회 완료
    # 5번째 캐릭터까지 완료 후 루프
    if(isFine):
        move_to_character_select_screen()
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
    
    click(coords["마을귀환"])
    click(coords["팝업확인"])
    
    while True:
        if(image_exists_at_region('./images/ingame.png', region)):
            break
        time.sleep(1)
        
def move_to_character_select_screen():
    if(not image_exists_at_region('./images/메뉴창켜짐확인.png', region)):
        click(coords["메뉴"])
    
    click(coords["메뉴-캐릭터변경"])
    click(coords["팝업확인"])

def move_to_character_slot(index):
    while True:
        if(image_exists_at_region('./images/캐릭터선택화면.png', region)):
            break
        time.sleep(1)
        
    print(f"{index}번째 캐릭터로 이동")
    click(coords[f"{index}번"])
    click(coords["게임시작"])
    in_game_waiting()
    
def has_dungeon_time():
    if(not image_exists_at_region('./images/메뉴창켜짐확인.png', region)):
        click(coords["메뉴"])
    click(coords["메뉴-던전"])
    click(coords["정예던전"])
    #마우스 스크롤 필요할수 있음
    scroll_on_window(*coords["정예던전스크롤위치"], -1500)
    
    if(not image_exists_at_region('./images/난쟁이 비밀통로 소모.png', region)):
        click(coords["메뉴"])
        return True
    if(not image_exists_at_region('./images/공허의유적소모.png', region)):
        click(coords["메뉴"])
        return True
    click(coords["메뉴"])
    return False

def has_items():
    click(coords["장비창"])
    if(not image_exists_at_region('./images/장비 미장착확인1.png', region)):
        click(coords["메뉴"])
        return True
    if(not image_exists_at_region('./images/장비 미장착확인2.png', region)):
        click(coords["메뉴"])
        return True
    click(coords["메뉴"])
    return False

def enter_dungeon_and_auto_hunt():
    if(not image_exists_at_region('./images/메뉴창켜짐확인.png', region)):
        click(coords["메뉴"])
    click(coords["메뉴-던전"])
    click(coords["정예던전"])
    scroll_on_window(*coords["정예던전스크롤위치"], -1500)
    if(not image_exists_at_region('./images/난쟁이 비밀통로 소모.png', region)):
        click(coords["난쟁이비밀통로"])
        click(coords["난쟁이비밀통로5단계"])
        click(coords["던전이동"])
        click(coords["던전이동확인팝업"])
        while True:
            if(image_exists_at_region('./images/난쟁이5단계확인.png', region)):
                break
            time.sleep(1)

    if(not image_exists_at_region('./images/공허의유적소모.png', region)):
        click(coords["공허의유적"])
        click(coords["공허의유적5단계"])
        click(coords["던전이동"])
        click(coords["던전이동확인팝업"])    
        while True:
            if(image_exists_at_region('./images/공허5단계확인.png', region)):
                break
            time.sleep(1)
    
    click(coords["자동사냥"])
    click(coords["순간이동"])
    
    
    
def is_out_of_dungeon():
    return image_exists_at_region('./images/던전끝 확인.png', region)

def return_to_town():
    click(coords["마을귀환"])
    click(coords["팝업확인"])
    
    while True:
        if(image_exists_at_region('./images/ingame.png', region)):
            break
        time.sleep(1)

def open_storage():
    click(coords["창고바로가기"])
    while True:
        if(image_exists_at_region('./images/창고확인.png', region)):
            break
        time.sleep(1)
    

def storage_has_equipment():
    return image_exists("storage_equipment_icon")

def retrieve_and_equip_equipment():
    for pos in coords["창고아이템"]:
        pyautogui.click(*pos)
        time.sleep(0.3)
    time.sleep(1)
    click(coords["창고꺼내기버튼"])
    click(coords["메뉴"])
    click(coords["장비창"])
    click(coords["자동장착"])
    time.sleep(1)
    if(not image_exists_at_region('./images/장비 미장착확인1.png', region)):
        click(coords["메뉴"])
        return False
    if(not image_exists_at_region('./images/장비 미장착확인2.png', region)):
        click(coords["메뉴"])
        return False
    click(coords["메뉴"])
    return True

def stop_macro(reason):
    print(f"[작동 중지] {reason}")

def unequip_all():
    click(coords["장비창"])
    if(image_exists_at_region('./images/장비모두해제.png', region)):
        click(coords["모두해제버튼"])
    click(coords["메뉴"])

def store_equipment():
    for pos in coords["인벤토리아이템"]:
        pyautogui.click(*pos)
        time.sleep(0.3)
    time.sleep(1)
    click(coords["창고보관버튼"])
    click(coords["메뉴"])

def retrieve_hunting_equipment():
    for pos in coords["창고아이템"]:
        pyautogui.click(*pos)
        time.sleep(0.3)
    time.sleep(1)
    click(coords["창고꺼내기버튼"])
    click(coords["메뉴"])
    click(coords["장비창"])
    if(image_exists_at_region('./images/자동장착.png', region)):
        click(coords["자동장착"])
    click(coords["메뉴"])

def move_to_hunting_spot():
    
    click(coords["은총의 순간이동"])
    click(coords["은총 첫번쨰 사냥터"])


def start_auto_hunt():
    while True:
        if(image_exists_at_region('./images/ingame.png', region)):
            break
        time.sleep(1)
    click(coords["자동사냥"])

def click(button_name):
    print(f"{button_name} 클릭")  # 실제 좌표 클릭 함수로 구현
    x, y = button_name
    pyautogui.click(x, y)
    time.sleep(1)

def image_exists(image_name):
    # 실제 이미지 탐지 로직 구현 필요
    return True  # 테스트용 기본값

def wait(seconds):
    import time
    time.sleep(seconds)

# === 시작 ===
if __name__ == "__main__":
    main()


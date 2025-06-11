try:
    import win32gui
    import win32con
    import time
    import pyautogui
    import cv2
    import numpy as np
    import random
    from PIL import ImageGrab
    import os
    import datetime
    import time
    import re
except Exception as e:
    print(e)
def wait_until_time():
    while True:
        user_input = input("실행 시간을 입력하세요 (예: 16:47 또는 엔터로 바로 실행): ").strip()

        if not user_input:
            print("입력 없음. 실행.")
            return

        # 형식 검사: HH:MM, H:M 등 허용
        match = re.match(r"^(\d{1,2}):(\d{1,2})$", user_input)
        if not match:
            print("⚠️ 유효하지 않은 형식입니다. 예: 3:7 또는 16:47")
            continue

        hour, minute = int(match.group(1)), int(match.group(2))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            print("⚠️ 시간은 0~23, 분은 0~59 사이여야 합니다.")
            continue

        # 유효한 시간 형식이 입력되었을 경우
        break

    # 현재 시각과 비교하여 대기
    now = datetime.datetime.now()
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= target_time:
        target_time += datetime.timedelta(days=1)

    print(f"⏳ {target_time.strftime('%H:%M')}까지 대기 중...")

    while datetime.datetime.now() < target_time:
        time.sleep(1)

    print("✅ 시간 도달. 실행 시작")

STATUS_FILE = "status.txt"


# 파일이 없으면 기본 Y로 생성
def init_status_file():
    if not os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "w") as f:
            f.write("N")

# 상태 읽기 (Y/N)
def read_status():
    with open(STATUS_FILE, "r") as f:
        return f.read().strip()
    
# 상태 갱신
def update_status(new_status):
    with open(STATUS_FILE, "w") as f:
        f.write(new_status)
        

init_status_file()


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

# 1번
# region = (0, 0, 960, 540)
# coords = {
#     "메뉴": (923, 43),
# "드레그시작": (472,263),
#     "드레그끝": (763,252),
#     "메뉴-캐릭터변경": (798,364),
#     "1번": (838, 79),
#     "2번": (840, 152),
#     "3번": (831, 197),
#     "4번": (834, 262),
#     "5번": (845, 321),
#     "게임시작": (851, 499),
#     "팝업확인": (518, 331),
#     "마을귀환": (30, 187),
#     "순간이동": (378, 494),
#     "은총의 순간이동":(424,495),
#     "은총첫번쨰사냥터": (199, 173),
#     "자동사냥": (904,430),
#     "메뉴-던전": (761, 258),
#     "정예던전": (166, 77),
#     "정예던전스크롤위치": (315,183),
#     "공허의유적": (401, 296),
#     "공허의유적5단계": (135,239),
#     "난쟁이비밀통로": (614,270),
#     "난쟁이비밀통로5단계": (101,243),
#     "던전이동": (855,499),
#     "던전이동확인팝업": (514,332),
#     "장비창": (881, 43),
#     "모두해제버튼": (899, 510),
#     "창고바로가기": (752, 491),
#     "창고보관버튼": (881,508),
#     "창고꺼내기버튼": (170,506),
#     "자동장착": (902,511),
#     "절전모드": (25,268),
#     "작은움직임": (543,326),
#     "인벤토리아이템": [
#         (730, 125), (778, 125), (823, 125), (869, 125), (920, 125),
#         (730, 174), (778, 174), (823, 174), (869, 174), (920, 174),
#         (730, 217), (778, 217), (823, 217), (869, 217), (920, 217),
#         (730, 267), (778, 267), (823, 267), (869, 267), (920, 267),
#     ],
#     "창고아이템": [
#         (39, 160), (87, 160), (140, 160), (176, 160),
#         (45, 212), (94, 212), (133, 212), (185, 212),
#         (34, 257), (94, 257), (133, 257), (185, 257),
#         (34, 308), (94, 308), (133, 308), (185, 308),
#         (34, 351), (94, 351), (133, 351), (185, 351),
#     ]
# }

#2번매크로
region = (960, 0, 960, 540)
coords = {
    "드레그시작": (1432,263),
    "드레그끝": (1015,252),
    "메뉴": (1883, 43),
    "메뉴-캐릭터변경": (1758, 364),
    "1번": (1798, 79),
    "2번": (1800, 152),
    "3번": (1791, 197),
    "4번": (1794, 262),
    "5번": (1805, 321),
    "게임시작": (1811, 499),
    "팝업확인": (1478, 331),
    "마을귀환": (990, 187),
    "순간이동": (1338, 494),
    "은총의 순간이동": (1384, 495),
    "은총첫번쨰사냥터": (1159, 173),
    "자동사냥": (1864, 430),
    "메뉴-던전": (1721, 258),
    "정예던전": (1126, 77),
    "정예던전스크롤위치": (1275, 183),
    "공허의유적": (1361, 296),
    "공허의유적5단계": (1095, 239),
    "난쟁이비밀통로": (1574, 270),
    "난쟁이비밀통로5단계": (1061, 243),
    "던전이동": (1815, 499),
    "던전이동확인팝업": (1474, 332),
    "장비창": (1841, 43),
    "모두해제버튼": (1859, 510),
    "창고바로가기": (1712, 491),
    "창고보관버튼": (1841, 508),
    "창고꺼내기버튼": (1130, 506),
    "자동장착": (1862, 511),
    "절전모드": (985,268),
    "작은움직임": (1503,326),
    "인벤토리아이템": [
        (1690, 125), (1738, 125), (1783, 125), (1829, 125), (1880, 125),
        (1690, 174), (1738, 174), (1783, 174), (1829, 174), (1880, 174),
        (1690, 217), (1738, 217), (1783, 217), (1829, 217), (1880, 217),
        (1690, 267), (1738, 267), (1783, 267), (1829, 267), (1880, 267),
    ],
    "창고아이템": [
        (999, 160), (1047, 160), (1100, 160), (1136, 160),
        (1005, 212), (1054, 212), (1093, 212), (1145, 212),
        (994, 257), (1054, 257), (1093, 257), (1145, 257),
        (994, 308), (1054, 308), (1093, 308), (1145, 308),
        (994, 351), (1054, 351), (1093, 351), (1145, 351),
    ]
}

def image_exists_at_region(template_path, region, threshold=0.93):
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

def get_window_rect(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    return rect  # (left, top, right, bottom)
def get_sorted_odin_windows():
    odin_windows = enum_windows_by_class_and_title("UnrealWindow", "ODIN  ")
    odin_windows = sorted(odin_windows, key=lambda hwnd: get_window_rect(hwnd)[0])  # 좌측 기준 정렬
    return odin_windows

###
###창조절#
###
# 콘솔창: 이름이 "odin_1번"인 창 찾기

def enum_windows_by_title(title):
    """특정 창 제목과 일치하는 핸들을 반환"""
    hwnds = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
            hwnds.append(hwnd)
    win32gui.EnumWindows(callback, None)
    return hwnds

def move_resize_window(hwnd, x, y, width, height):
    """창 위치와 크기 조절"""
    win32gui.MoveWindow(hwnd, x, y, width, height, True)

MAX_CHARACTERS = 5
current_char_index = 0
pyautogui.FAILSAFE = False
def main():
    odin_windows = get_sorted_odin_windows()
    # console_windows = enum_windows_by_title("odin_1번")# 1번
    console_windows = enum_windows_by_title("odin_2번")# 2번

    if len(odin_windows) >= 1:
        # move_resize_window(odin_windows[0], 0, 0, 960, 540)# 1번
        # move_resize_window(console_windows[0], 0, 550, 960, 200)# 1번
        move_resize_window(odin_windows[1], 960, 0, 960, 540)# 2번
        move_resize_window(console_windows[0], 960, 550, 960, 200) #2번
        print("ODIN 창 위치 조정 완료")
    try:
        wait_until_time()
    except Exception as e:
        print(e)
        input()
    isFine = True
    isNext = False
    isDone = False
    for i in range(MAX_CHARACTERS):
        if(not isFine): break
        if(isDone): break
        isNext = True
        current_char_index = i + 1
        # 실행 루프
        print("작동 대기")
        while True:
            status = read_status()
            if status == "N":
                update_status('Y')
                break
            time.sleep(1)
        print("작동 시작. 마우스 작동시 미동작.")
        wake_up_if_sleep_mode()
        click(coords["메뉴"])
        click(coords["메뉴"])
        # ensure_in_game_mode()
        time.sleep(1)
        while True:
            move_to_character_select_screen()
            if(move_to_character_slot(current_char_index)):
                break
            
        while isNext:
            if has_dungeon_time(): #3.1
            # if not has_dungeon_time(): #3.1 던전 시간있어도 없게 테스트
                if has_items():
                    while has_dungeon_time():
                        enter_dungeon_and_auto_hunt()
                        update_status('N')
                        while not is_out_of_dungeon():
                            wait(10)
                        continue  # 던전 끝나면 다시 3.1로 돌아감
                else:
                    open_storage()
                    if retrieve_and_equip_equipment():
                        continue  # 다시 3.1로
                    else:
                        #아이템 없음 찾기실패 종료
                        print("아이템 찾기 실패 종료")
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
                        print("캐릭터 작업완료")
                        update_status('N')
                        isNext = False
                        break
                    else:
                        print("모든 캐릭터 작업완료")
                        isDone = True
                        break  # 모든 캐릭터 순회 완료
    # 5번째 캐릭터까지 완료 후 루프
    if(isFine):
        while True:
            move_to_character_select_screen()
            if(move_to_character_slot(1)):
                break
        open_storage()
        retrieve_hunting_equipment()
        move_to_hunting_spot()
        start_auto_hunt()
        
    update_status('N')
    print("작동완료")
    input("")

# === 기능 구현 자리 (좌표 기반 구현 필요) ===
def wake_up_if_sleep_mode():
    if(image_exists_at_region('./images/juljun.png', region)):
        mouse_drag(*coords["드레그시작"], *coords["드레그끝"])
    time.sleep(1)

def ensure_in_game_mode():
    while True:
        if(image_exists_at_region('./images/ingame.png', region)):
            break
        time.sleep(1)
    
def in_game_check():
    i = 0
    while True:
        if(image_exists_at_region('./images/ingame.png', region)):
            break
        time.sleep(1)
        i += 1
        if(i > 30):
            i = 0
            click(coords["메뉴"])
            break
        
        
        
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
    if(not image_exists_at_region('./images/menucheck.png', region)):
        click(coords["메뉴"])
    
    click(coords["메뉴-캐릭터변경"])
    click(coords["팝업확인"])

def move_to_character_slot(index):
    i=0
    isFailedCharacter = False
    while True:
        if(image_exists_at_region('./images/charactercheck.png', region)):
            break
        i += 1
        if(i > 60):
            isFailedCharacter = True
            break
        time.sleep(1)
        
    if(isFailedCharacter):
        print(f"캐릭터창 찾기 실패로 이동")    
        return False
    print(f"{index}번째 캐릭터로 이동")
    click(coords[f"{index}번"])
    click(coords["게임시작"])
    in_game_waiting()
    return True
def has_dungeon_time():
    if(not image_exists_at_region('./images/menucheck.png', region)):
        click(coords["메뉴"])
    click(coords["메뉴-던전"])
    click(coords["정예던전"])
    #마우스 스크롤 필요할수 있음
    scroll_on_window(*coords["정예던전스크롤위치"], -1500)
    time.sleep(1)
    
    if(not image_exists_at_region('./images/nanend.png', region)):
        click(coords["메뉴"])
        in_game_check()
        return True
    if(not image_exists_at_region('./images/gonghuend.png', region)):
        click(coords["메뉴"])
        in_game_check()
        return True
    click(coords["메뉴"])
    in_game_check()
    return False

def has_items():
    click(coords["장비창"])
    time.sleep(1)
    if(not image_exists_at_region('./images/jangbeno1.png', region)):
        click(coords["메뉴"])
        in_game_check()
        return True
    if(not image_exists_at_region('./images/jangbeno2.png', region)):
        click(coords["메뉴"])
        in_game_check()
        return True
    click(coords["메뉴"])
    in_game_check()
    return False

def enter_dungeon_and_auto_hunt():
    isAutoPlay = True
    isFailed1 = False
    while True:
        if(not image_exists_at_region('./images/menucheck.png', region)):
            click(coords["메뉴"])
        click(coords["메뉴-던전"])
        time.sleep(1)
        if(image_exists_at_region('./images/isdungeon.png', region)):
            click(coords["정예던전"])
            time.sleep(1)
            scroll_on_window(*coords["정예던전스크롤위치"], -1500)
            time.sleep(1)
        else:
            click(coords["메뉴"])
            click(coords["메뉴"])
            click(coords["메뉴"])
            click(coords["메뉴"])
            continue
        
        
        if(not image_exists_at_region('./images/nanend.png', region)):
            click(coords["난쟁이비밀통로"])
            click(coords["난쟁이비밀통로"])
            click(coords["난쟁이비밀통로5단계"])
            click(coords["난쟁이비밀통로5단계"])
            click(coords["던전이동"])
            click(coords["던전이동확인팝업"])
            i = 0
            while True:
                if(image_exists_at_region('./images/nancheck.png', region)):
                    isFailed1 = False
                    break
                i += 1
                if(i > 60):
                    isFailed1 = True
                    break
                time.sleep(1)
        elif(not image_exists_at_region('./images/gonghuend.png', region)):
            click(coords["공허의유적"])
            click(coords["공허의유적"])
            click(coords["공허의유적5단계"])
            click(coords["공허의유적5단계"])
            click(coords["던전이동"]) 
            click(coords["던전이동확인팝업"])    
            i = 0
            while True:
                if(image_exists_at_region('./images/gonghu5.png', region)):
                    isFailed1 = False
                    break
                i += 1
                if(i > 60):
                    isFailed1 = True
                    break
                time.sleep(1)
        if(not isFailed1): 
            while True:
                click(coords["자동사냥"])
                click(coords["순간이동"])
                while True:
                    if(image_exists_at_region('./images/ingame.png', region)):
                        break
                    time.sleep(1)
                    
                click(coords["작은움직임"])
                click(coords["절전모드"])
                i = 0
                while True:
                    if(image_exists_at_region('./images/nonplaying.png', region)):
                        isAutoPlay = False
                        break
                    i += 1
                    if(i > 10):
                        isAutoPlay = True
                        break
                    time.sleep(1)
                #자동사냥중이아님
                if(not isAutoPlay):
                    wake_up_if_sleep_mode()
                    time.sleep(3)
                    continue
                else:
                    break
            break
            
        
    

def is_out_of_dungeon():
    return image_exists_at_region('./images/dunendcheck.png', region)

def return_to_town():
    click(coords["마을귀환"])
    click(coords["팝업확인"])
    in_game_check()

def open_storage():
    i = 0
    isOpenStorage = True
    while True:
        click(coords["창고바로가기"])
        while True:
            if(image_exists_at_region('./images/storecheck.png', region)):
                isOpenStorage = True
                break
            i += 1
            if(i > 60):
                i = 0
                isOpenStorage = False
                break
            time.sleep(1)
        if(isOpenStorage):
            break

def retrieve_and_equip_equipment():
    for pos in coords["창고아이템"]:
        pyautogui.click(*pos)
        time.sleep(0.2)
    time.sleep(1)
    click(coords["창고꺼내기버튼"])
    click(coords["창고꺼내기버튼"])
    click(coords["메뉴"])
    in_game_check()
    click(coords["장비창"])
    time.sleep(1)
    click(coords["자동장착"])
    time.sleep(1)
    if(image_exists_at_region('./images/jangbeno1.png', region)):
        click(coords["메뉴"])
        in_game_check()
        return False
    if(image_exists_at_region('./images/jangbeno2.png', region)):
        click(coords["메뉴"])
        in_game_check()
        return False
    click(coords["메뉴"])
    in_game_check()
    return True

def stop_macro(reason):
    print(f"[작동 중지] {reason}")

def unequip_all():
    click(coords["장비창"])
    if(image_exists_at_region('./images/jangunset.png', region)):
        click(coords["모두해제버튼"])
    click(coords["메뉴"])
    in_game_check()

def store_equipment():
    for pos in coords["인벤토리아이템"]:
        pyautogui.click(*pos)
        time.sleep(0.2)
    time.sleep(1)
    click(coords["창고보관버튼"])
    click(coords["창고보관버튼"])
    time.sleep(1)
    click(coords["메뉴"])
    in_game_check()

def retrieve_hunting_equipment():
    for pos in coords["창고아이템"]:
        pyautogui.click(*pos)
        time.sleep(0.2)
    time.sleep(1)
    click(coords["창고꺼내기버튼"])
    click(coords["창고꺼내기버튼"])
    time.sleep(1)
    click(coords["메뉴"])
    in_game_check()
    click(coords["장비창"])
    time.sleep(1)
    if(image_exists_at_region('./images/autose.png', region)):
        click(coords["자동장착"])
    click(coords["메뉴"])
    in_game_check()

def move_to_hunting_spot():
    
    click(coords["은총의 순간이동"])
    click(coords["은총첫번쨰사냥터"])


def start_auto_hunt():
    while True:
        if(image_exists_at_region('./images/ingame.png', region)):
            break
        time.sleep(1)
    click(coords["자동사냥"])


def click(pos):
    x, y = pos
    # -2 ~ +2 범위의 무작위 좌표 흔들기
    rand_x = x + random.randint(-2, 2)
    rand_y = y + random.randint(-2, 2)

    print(f"클릭 위치: ({rand_x}, {rand_y})")  # 로그 출력
    pyautogui.moveTo(rand_x, rand_y)
    pyautogui.click()
    time.sleep(1)
    
def wait(seconds):
    import time
    time.sleep(seconds)
# === 시작 ===
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("종료되었습니다. (Ctrl+C)")

    finally:
        update_status("N")

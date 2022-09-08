import pyautogui as pya
from pynput import mouse
import re
import time

pos1, pos2, entered = [], [], 0

def get_pos(x, y, btn, pressed):
    global pos1
    global pos2
    global entered

    if len(pos1) == 0 and entered == 0: 
        pos1 = [x, y]
        entered = 1
    if len(pos2) == 0 and entered == 0:
        pos2 = [x, y]
        entered = 1

file_name = input('Переместите файл в папку со скриптом, напишите сюда его название и нажмите Enter:::')

listener = mouse.Listener(
    on_click = get_pos
)
listener.start()

input('Наведите курсор на поле ввода и кликните правой кнопкой, после нажмите Enter:::')
print(f'[+] Координаты поля: {pos1[0], pos1[1]}')

entered = 0

input('Наведите курсор на поле кнопку ввода и кликните правой кнопкой, после нажмите Enter:::')
print(f'[+] Координаты кнопки: {pos2[0], pos2[1]}')

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
            pattern = r"=+|\n"
            if len(parsed)>0:
                arr = []
                result = re.split(pattern, parsed)
                for x in result:
                    if(x.strip().startswith('Password')):
                        arr.append(x.split(':', 1)[1].strip())

                if len(arr) > 0: 
                    if len(pos1) == 2 and len(pos2) == 2:
                        for x in arr: 
                            print('[+] Ввожу значение')
                            pya.moveTo(pos1[0], pos1[1])
                            time.sleep(.2)
                            pya.click()
                            time.sleep(.2)
                            pya.write(x, interval=0.01)
                            time.sleep(.2)
                            pya.moveTo(pos2[0], pos2[1])
                            time.sleep(.2)
                            pya.click()
                            time.sleep(.2)
                            print('[+] Кнопка нажата. Перезапуск цикла')
                else:
                    print('[-] Произошла ошибка. Не удалось извлечь значения.')
                #print(arr) 
            else:
                print('[-] Файл пуст')
    except FileNotFoundError:
        print(f'[-] Файл {file_name} не найден')
    except:
       print('[-] Произошла ошибка')
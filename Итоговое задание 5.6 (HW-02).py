import time

pole = [
     [' ', 0, 1, 2]
    ,[0,'-','-','-']
    ,[1,'-','-','-']
    ,[2,'-','-','-'] 
    ]

def pole_print():
    for row in pole:
        for element in row:
            print(element, end = " ")
        print()

def game(player, value):
    x_row = input(f'{player}, Введите номер СТОЛБЦА от 0 до 2, куда ставим "{value}": ')
    x_element = input(f'{player}, Введите номер СТРОКИ от 0 до 2, куда ставим "{value}": ') 
    print()
    if x_row.isdigit() and x_element.isdigit() and int(x_row) in (0,1,2) and int(x_element) in (0,1,2):
        x_row, x_element = int(x_row) + 1, int(x_element) + 1
        if pole [x_element][x_row] == '-':
            pole [x_element][x_row] = value
            pole_print()
            print()
        else:
            print(f'{player}, эта ячейка занята! Попробуйте выбрать другую!')
            game(player, value)
    else:
        print(f'{player}, Вы ввели не верные координаты! Необходимо ввести цифру от 0 до 2. Попробуйте еще раз!')
        game(player, value)

def win(value):
    for i in range(1,4):
        if any([pole[i][1] == pole[i][2] == pole[i][3] == value,
                pole[1][i] == pole[2][i] == pole[3][i] == value]):
            return 'win'
        else:
            continue
    if any([pole[1][1] == pole[2][2] == pole[3][3] == value,
            pole[1][3] == pole[2][2] == pole[3][1] == value,
            ]):
        return 'win'
    if pole[1].count('-') == pole[2].count('-') == pole[3].count('-') == 0:
        return 'no_win'
            
player_1 = input('Игрок №1, добро пожаловать в игру "Крестики-нолики"! Введите Ваше имя: ')
print()
player_2 = input('Игрок №2, добро пожаловать в игру "Крестики-нолики"! Введите Ваше имя: ')
players = {player_1 : 'x', player_2 : 'o'}
print('Поле для игры выглядит таким образом:','\n')
pole_print()
print('\n'
      ,'Вам нужно будет вводить поочередно номер столбца и номер строки.'
      ,'\n'
      ,f'{player_1}, Вы будете играть за крестики "х" и Ваш ход будет первым! Приготовьтесь...')
for i in reversed(range(1,4)):
    time.sleep(2)
    print(i)
print('Погнали!')

while True:
    for player, value in players.items():
        game(player, value) 
        win(value)
        if win(value) == 'win':
            print(f'Поздравляю,{player}, Вы выиграли!')
            break
        if win(value) == 'no_win':
            print('Игра закончена в ничью!')
            break
    if win(value):
            break

time.sleep(60)
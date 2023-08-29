from random import randint # для игрока-компьютера импорт библиотеки рандомного выбора

# координаты точек
class  Dot: 
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):  # проверка совпадений точек на поле
        return self.x == other.x and self.y == other.y
    def __repr__(self) -> str:  #  вывод введенных точек
        return f"Dot({self.x}, {self.y})"

# классы исключений (ошибок)
class AllException(Exception): # общий класс включает все классы исключений
    pass

class BoardOutException(AllException): # подкласс исключений, который конкретизирует из общей ошибки ошибку выхода за пределы поля
    def __str__(self) -> str:
        return "Доска имеет поле 6*6, стреляйте в нее, а не за ее пределы!"
    
class BoardUseException(AllException): # подкласс исключений, который конкретизирует из общей ошибки ошибку выбора ячейки, в которую уже стрелял
    def __str__(self) -> str:
        return "В эту ячейку уже стреляли! Стреляйте в другую!"    
    
class BoardWrongShipException(AllException):
    pass

      
    
# класс корабль
class Ship:
    def __init__(self, dot, leght, direction):
        self.dot = dot
        self.leght = leght
        self.direction = direction
        self.lives = leght

    @property   # ментор не объяснил зачем здесь этот декоратор и вообще тут для него все ПРОСТО!!! декоратор @property используется для преобразования метода в атрибут только для чтения. Это позволяет вам получить значение метода, как если бы это был атрибут, без необходимости вызывать его как функцию с ().
    def dots(self):
        ship_dots = []
        for i in range(self.leght):
            ship_x = self.dot.x  # ментор не объяснил каким образом идет подстановка координаты из класса Dot!!!
            ship_y = self.dot.y

            if self.direction == 0:
                ship_x += i
            elif self.direction == 1:
                ship_y += i
            
            ship_dots.append(Dot(ship_x, ship_y))
        return ship_dots
    
    def shooten(self, shot):
        return shot in self.dots()  # добавил скобки, чтобы можно было напечатать проверку s = Dot(5, 3) print(a_ship.shooten(s)) без использования декоратора @property. Что касается метода, который принимает аргументы, такой метод не может быть преобразован в свойство с помощью @property. 

# класс игровое поле
class Board:
    def __init__(self, hid = False, size = 6):  # по умолчанию поле 6*6, задается в классе Game
        self.size = size  # размер поля (обязательный параметр)
        self.hid = hid # скрыть или показать (обязательный параметр)

        self.count = 0 # количество пораженных кораблей
        self.field = [ ["O"]*size for _ in range(size) ]  # нижнее подчеркивание - это такая же переменная как i или x, но по традиции она нигде далее не применяется
        self.busy = [] # список занятых точек где находятся корабли и которые с ним соседствуют из near (около)
        self.ships = [] # список кораблей

    def __str__(self):   # вывод на печать доски print(Board)
        res = "\n" + "  |"
        for w in range(1, self.size + 1):  # создание нумерации столбцов в зависимости от size
            res += f" {w} |"
        
        for i, row in enumerate(self.field):                # Если range() позволяет получить только индексы элементов списка, то enumerate() – сразу индекс элемента и его значение.
            res += f"\n{i+1} | " + " | ".join(row) + " |"
        
        if self.hid:
            res = res.replace("■", "O") # если поле нужно скрыть (hide = True), то корабли заменяются на O
        return res
    
    def out_dot(self, dot):  # функция проверки выхода точки за границы поля, если  True - значит точка выходит за границы
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def contour(self, ship, verb = False): # функция добавления контура точек корабля
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)] # около, список координат вокруг точки
        for d in ship.dots: # проходимся циклом for по списку точек 
            for dx, dy in near: # проходимся циклом for по списку near и сдвигаем исходную точку d на dx и dy
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out_dot(cur)) and cur not in self.busy: # если точка не выходит за границы доски (метод out) и если она не находится в списке занятых точек(self.busy), то мы ставим на её месте знак  "-" и заносим её в список busy.
                    if verb:
                        self.field[cur.x][cur.y] = "-"  # Если verb = True, то точки countour становятся видны пользователю. Т.е. потопленный корабль обводится по периметру точками (типа туда уже не надо стрелять).
                    self.busy.append(cur) # добавляем точку окружения корабля в список занятых точек

    def add_ship(self, ship):  # функция добавления корабля
        for d in ship.dots: # проходимся циклом for по списку точек
            if self.out_dot(d) or d in self.busy:  # если точка за пределами поля или есть в вписке занятых точек
                raise BoardWrongShipException()  # вызываем исключение 
        for d in ship.dots: # если исключение не срабатывает, то отрисовываем точку на поле и добавляем в список занятых busy 
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship) # добавляем корабль в список кораблей
        self.contour(ship) # добавляем контур корабля на доску и в список занятых точек  busy

    def shot(self, dot): # функция стрельбы
        if self.out_dot(dot):
            raise BoardOutException() # если точка за пределами поля вызываем исключение
        if dot in self.busy:
            raise BoardUseException() # если точка есть в списке занятых точек то вызываем исключение
        
        self.busy.append(dot) # если условия не выполнились добавляем точку с список занятых точек

        for ship in self.ships:  # для корабля в списке кораблей
            if dot in ship.dots: # если точка выстрела есть в списке точек кораблей
                ship.lives -= 1 # убираем единицу из длинны его точек 
                self.field[dot.x][dot.y] = "X" # отмечаем на поле точку как подбитую
                if ship.lives == 0:  # если количество жизней у корабля равно нулю, то корабль уничтожен
                    self.count += 1 # добавляем единицу корабля в счетчик пораженных кораблей
                    self.contour(ship, verb= True) # делаем для уничтоженного 
                    print("Корабль уничтожен!") 
                    return False  #  возвращаем False для перехода хода
                else:
                    print("Корабль ранен!")
                    return True  #  возвращаем True для повтора хода этим же игроком
        self.field[dot.x][dot.y] = "Т" # если точка выстрела не находится в списке точек кораблей, то отмечаем на поле точку как мимо и никуда ее не заносим
        print("Мимо!")
        return False # переход хода

    def begin(self): # функция обнуления списка занятых точек для новой игры
        self.busy = []

#  класс игроков
class Player:
    def __init__(self, board, enemy):   # инициализация принимает поле игрока и поле соперника
        self.board = board
        self.enemy = enemy
     
    #def ask(self):  # вообще не понятно для чего это исключение. оставлено для будущего кода, который ещё не реализован. Фактически, оно не ничего не меняет, это скорее образец хорошего кода или, своего рода, заглушка на будущее.
        #raise NotImplementedError()  # Пока мы делаем общий для AI и пользователя класс, этот метод мы описать
                                        # не можем. Оставим этот метод пустым. Тем самым обозначим, что потомки
                                        # должны реализовать этот метод.

    def move(self): # "двигаться", 
        while True:
            try:
                target = self.ask() # просим пользователя сделать ход
                repeat = self.enemy.shot(target) # применяем метод shot к доске соперника enemy. смотря какой выстрел, то вернется True или False или исключение
                return repeat
            except AllException as e: # если вернется исключение, печатаем это исключение, но цикл продолжается
                print(e)

# наследуемый класс игрока - компьютер
class Comp(Player):
    def ask(self): # функция рандомного выстрела
        d = Dot(randint(0,5), randint(0,5)) # точка с рандомными координатами от 0 до 5 , так как индексы поля у нас от 0 до size-1
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d  # возвращаем точку, чтобы потом ее проверить

# наследуемый класс игрока - пользователь
class User(Player):
    def ask(self):
        while True:
            d = input("Ваш ход: ").split()  # в цикле запрос двух цифр координат и их соединение в строку
            

            if len(d) != 2:                      # если введено не две координаты, то цикл повторяется
                print("Введите две координаты через пробел!")
                continue
            
            x, y = d  # множественное присвоение строк x и y  из строки d
            
            if not(x.isdigit()) or not(y.isdigit()):   # проверка , является ли координата числом
                print(" Введите числа через пробел! ")
                continue

            x, y = int(x)-1, int(y)-1  # отнимаем единицу из введенной координаты, потому что у поля индексы
           
            return Dot(x, y)  #  возвращаем точку с координатами

# Класс "игра" и генерация досок
class Game:
    def __init__(self, size = 6):
        self.lens = [3, 2, 2, 1, 1, 1, 1] # количество кораблей с указанием их длинны
        self.size = size
        board = self.random_board()
        enemy = self.random_board()
        enemy.hid = True
        
        self.comp = Comp(enemy, board)
        self.user = User(board, enemy)

    def try_board(self):
        board = Board(size = self.size)  # это не понял
        attempts = 0 # попытки создать доску
        for lengt in self.lens:  # для каждой длинны корабля
            while True:
                attempts += 1 # считаем попытки постановки корабля на доску
                if attempts > 2000:  # если больше 2000 попыток, то возвращаем None , так как доска не создалась
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), lengt, randint(0,1))  # создается корабль с рандомными координатами Dot, длинной leght и рандомным направлением 0 или 1
                try:
                    board.add_ship(ship) # добавляем рандомный корабль на поле, если ошибка то вызывается исключение и цикл начинается заново
                    break
                except BoardWrongShipException:
                    pass
        board.begin()  # функция обнуления списка занятых точек для новой игры
        return board
    
    def random_board(self): # гарантированное создание доски, так как случай с None будет сам еще раз запускать в цикле функцию try_board
        board = None
        while board is None:
            board = self.try_board()
        return board
    
    def greet(self):  # функция приветствия с рекомендациями ввода
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):  # петля, цикл игры, преходы между игроками, если num четное или не четное
        num = 0
        while True:
            print("-"*20)
            print("Доска пользователя:")
            print(self.user.board)
            #print(self.user.board.busy)
            
            print("-"*20)
            print("Доска компьютера:")
            print(self.comp.board)
            #print(self.comp.board.busy)
            
            print("-"*20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.user.move()
            else:
                print("Ходит компьютер!")
                repeat = self.comp.move()
            if repeat:
                num -= 1
            
            if self.comp.board.count == len(self.lens):  # если количество очков равно количеству кораблей, то выигрыш
                print("-"*20)
                print("Пользователь выиграл!")
                break
            
            if self.user.board.count == len(self.lens):
                print("-"*20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()







# a = Dot(2, 2)
# a_ship = Ship(a, 3, 0)

# c = Dot(2, 0)
# c_ship = Ship(c, 4, 0)

#print(a_ship.dots)
#print(a_ship.shooten(s))

# b = Game()
# b.size = 10
# print(b.try_board())





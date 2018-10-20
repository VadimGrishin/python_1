#!/usr/bin/python3

"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 11     - 14    87      
      16 49    55 77    88    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://docs.python.org/3/library/random.html

"""
import random
Nmax = 90
class player_card():
    def __init__(self, usertype='user'):
        if usertype == 'comp':
            self.title = '{:-^28}'.format('Карточка компьютера')
            self.indent = ''
        else:
            self.title = '{:-^28}'.format('Ваша карточка')
            self.indent = ' '* 28
        self.bag = set(range(1,Nmax + 1))
        self.card = []
        for i in range(3):
            self.card.append(self._write_line())
        self.rest = 15
    def _write_line(self):
        line = sorted(random.sample(self.bag,5))
        for n in line:
            self.bag.remove(n)
        line_inds = sorted(random.sample(range(9),5))
        a = ['']*9
        for i, n in enumerate(line_inds):
            a[n] = line[i]
        return(a)
    def erase(self,num):
        for i, row in enumerate(self.card):
            for j, col in enumerate(row):
                if num == col:
                    self.card[i][j] ='-'
                    self.rest -= 1
                    return True
        return False       
    def show(self):
        print(self.indent + self.title)
        for i in range(3):
            print(self.indent + '|{:>2}|{:>2}|{:>2}|{:>2}|{:>2}|{:>2}|{:>2}|{:>2}|{:>2}|'.format(*self.card[i]))
        print(self.indent + '-'*28)
        return self.rest
    
def ball_gen():
    bg = set(range(1,Nmax +1))
    while len(bg):
        b = random.sample(bg,1)
        bg.remove(b[0])
        yield (b[0],len(bg))

user_card = player_card()
comp_card = player_card('comp')
move = ball_gen()

while True:
    indent = ' '*14
    u = user_card.show()
    c = comp_card.show()
    if not u * c:
        if (u + c):
            if not u:
                print(indent + 'Вы выиграли')
            else:
                print(indent + 'Вы проиграли')
        else:
            print(indent + 'Ничья')
        break
    
    try:
        state = next(move) # state[0] - номер бочонка, state[1] - осталось в мешке
    except StopIteration:
        print(indent + 'Мешок пуст')
        break
    
    print(indent + 'Новый бочонок: {} (осталось {})'.format(*state))

    a = input(indent + 'Зачеркнуть цифру? (y/n) ')
    if a == 'y':
        if not user_card.erase(state[0]):
            print(indent + 'Вы проиграли')
            break
    elif a == 'n':
        if user_card.erase(state[0]):
            print(indent + 'Вы проиграли')
            break
    elif a == 'q':
        break
    comp_card.erase(state[0])





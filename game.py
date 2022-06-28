
import tkinter as tk
import random
import operator
from time import time

class Player(object):

    def __init__(self, score=0, level=1, name='Player'):
        self.score = score
        self.level = level
        self.name = name
        self.fails = 0

    def set_level(self):
        user_level = int(input("""
            Choose level:
            1. Easy
            2. Medium
            3. Hard\n
            >>>   """))
        self.level = user_level

    def update_score(self):
        self.score += 1

    def update_fails(self):
        self.fails += 1

class Game(Player):

    def __init__(self, Player, flag=True):
        self.level = Player.level
        self.flag = flag
        self.result = 0
        self.start = time()

    def rand_operation(self):
        operations = [
            'S',
            'add',
            'sub',
            # 'mul',
            # 'truediv',
        ]
        operation = operations[random.randint(1, 2)]
        return operation

    def add_call(self):
        if self.level == 1:
            numbers = random.sample(range(2, 99), 2)
            result = operator.add(numbers[0], numbers[1])

        return numbers, result

    def sub_call(self):
        if self.level == 1:
            numbers = sorted(random.sample(range(2, 99), 2))
            result = operator.sub(numbers[1], numbers[0])
            numbers.reverse()

        return numbers, result

    def publish_question(self, numbers, sym):
        user_input = input('\n::: {first_num} {sym} {second_num}\n >>> '.format(
            first_num = numbers[0],
            second_num = numbers[1],
            sym = sym
        ))
        self.result = user_input

    def generate_question(self, Player):
        operation = self.rand_operation()

        if operation == 'add':
            numbers, sol = self.add_call()
            sym = '+'
            self.publish_question(numbers, sym)
        elif operation == 'sub':
            numbers, sol = self.sub_call()
            sym = '-'
            self.publish_question(numbers, sym)

        return self.check_result(Player, sol, numbers, sym)

    def check_result(self, Player, sol, numbers, sym):
        if self.result == 'S' or self.result == 's' or Player.fails == 2 or self.out_of_time():
            print("Your Score: {}\n".format(Player.score))
            self.update_flag()
        elif sol == int(self.result):
            Player.update_score()
        else:
            Player.update_fails()
            return self.generate_question(Player)
            # self.publish_question(numbers, sym)
            # return self.check_result(Player, sol, numbers, sym)

    def update_flag(self):
        self.flag = False

    def out_of_time(self):
        minutes, rem = divmod(time() - self.start, 60)
        if minutes > 1:
            return False

class App:

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("500x500+100+100")
        self.window.resizable(0, 0)
        self.window.title("Arithematic Game")

    def ask_for_level(self):

        level_text = tk.Label(self.window, text='Select level:', font=('arial', 14, 'bold'))
        level_text.pack(side=TOP, padx=5, pady=5)
        lowButton = tk.Button(self.window, text='Low', font=('arial', 12, 'bold'))
        lowButton.pack(side=TOP, padx=5, pady=5)
        mediumButton = tk.Button(self.window, text='Medium', font=('arial', 12, 'bold'))
        mediumButton.pack(side=TOP, padx=5, pady=5)
        highButton = tk.Button(self.window, text='High', font=('arial', 12, 'bold'))
        highButton.pack(side=TOP, padx=5, pady=5)

    def question_frame(self):

        frame = tk.Frame(self.window, width=500, height=50)
        frame.pack(fill=X)

        lbl = tk.Label(frame, text="Title", font=('arial', 12, 'bold'))
        lbl.pack(side=LEFT, padx=5, pady=5)

        entry = tk.Entry(frame, font=('arial', 12, 'bold'))
        entry.pack(side=RIGHT, padx=5, expand=True)


if __name__ == '__main__':

    print("""
    *** You have 1 minute or 3 trials before the game ends. ***

    *** Press 'S' to stop the game anytime. ***\n
    """)

    player = Player()
    player.set_level()

    game_instance = Game(player)

    while game_instance.flag:
        game_instance.generate_question(player)

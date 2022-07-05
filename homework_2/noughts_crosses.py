import random
import tkinter.messagebox as mb
from tkinter import Tk, Button


class Game:
    def __init__(self, rows, cols):
        self.field_rows = rows
        self.field_columns = cols
        self.fields_count = rows * cols
        self.game_run = True
        self.cross_count = 0
        self.field = []
        self.root = Tk()
        self.root.title('XO')
        self.final_message = ''
        for row in range(self.field_rows):
            line = []
            for col in range(self.field_columns):
                button = Button(self.root, text=' ', width=4, height=1,
                                font=('Verdana', 20, 'bold'),
                                background='lavender',
                                command=lambda row=row, col=col: self.click(row, col))
                button.grid(row=row, column=col, sticky='nsew')
                line.append(button)
            self.field.append(line)
            new_button = Button(self.root, text='new game', command=self.new_game)
            new_button.grid(
                row=self.field_rows + 1,
                column=0,
                columnspan=self.field_columns + 1,
                sticky='nsew'
            )

    def start_game(self):
        self.root.mainloop()

    def new_game(self):
        for row in range(self.field_rows):
            for col in range(self.field_columns):
                self.field[row][col]['text'] = ' '
                self.field[row][col]['background'] = 'lavender'
        # global game_run
        self.game_run = True
        # global cross_count
        self.cross_count = 0

    def click(self, row, col):
        if self.game_run and self.field[row][col]['text'] == ' ':
            self.field[row][col]['text'] = 'X'
            self.cross_count += 1
            self.check_state(row, col, 'X')
            if self.game_run and self.cross_count < int(
                    self.fields_count / 2) + 1:  # так как возможный максимум крестиков 50
                comp_row, comp_col = self.computer_move()
                self.check_state(comp_row, comp_col, 'O')

    def check_state(self, row, col, smb):
        self.check_all_lines(row, col, smb)

    def check_all_lines(self, row, col, smb):  # horizontal, vertical, main and secondary diagonals
        # Vertical
        line_coords = []
        ways = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([1, 1], [-1, -1]), ([1, -1], [-1, 1])]
        for way in ways:
            counter = 1
            line_coords = [(row, col)]
            for i in way:
                cur_row = row
                cur_col = col
                val_row = i[0]
                val_col = i[1]
                while True:
                    next_row = cur_row + val_row
                    next_col = cur_col + val_col
                    if 0 <= next_row < self.field_rows \
                            and 0 <= next_col < self.field_columns:
                        next_field_val = self.field[next_row][next_col]['text']
                        if next_field_val == smb:
                            counter += 1
                            line_coords.append((next_row, next_col))
                            if counter == 5:
                                break
                        else:
                            break
                    else:
                        break
                    cur_row = next_row
                    cur_col = next_col
            if counter == 5:
                self.game_run = False
                self.final_message = "Lose:(" if smb == 'X' else "Win!"
                for i in line_coords:
                    self.field[i[0]][i[1]]['background'] = 'pink'
                self.show_info()
                return
        # draw check
        if self.fields_count % 2 == 0:
            if self.cross_count == int(self.fields_count / 2) and smb == 'O':
                self.draw()
        else:
            if (self.cross_count == int(self.fields_count / 2) + 1) and smb == 'X':
                self.draw()

    def computer_move(self):
        while True:
            row = random.randint(0, self.field_rows - 1)
            col = random.randint(0, self.field_columns - 1)
            if self.field[row][col]['text'] == ' ':
                self.field[row][col]['text'] = 'O'
                break
        return row, col

    def show_info(self):
        msg = self.final_message
        mb.showinfo("Информация", msg)

    def draw(self):
        self.game_run = False
        self.final_message = "Товарищеская ничья!"
        self.show_info()


g = Game(10, 10)
g.start_game()

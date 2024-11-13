from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import random

class MinesweeperSquare(Label):
    '''object for a Minesweeper cell'''

    def __init__(self, master, coord):
        '''MinesweeperSquare(master, coord) -> MinesweeperSquare
        creates a new blank with (row, column) coord'''
        Label.__init__(self, master, relief='raised', height=1, width=2)
        self.coord = coord
        self.number = 0  
        self.readOnly = False 
        self.exposed = False
        self.bomb = False 
        self.flagged = False
        self.touching = 0
        self.bind('<Button-1>', self.exposeSquare) 
        self.bind('<Button-2>', self.changeFlag)
        self.bind('<Button-3>', self.changeFlag)

    def changeFlag(self, event=None):
        '''MinesweeperSquare.changeFlag()
        turns the flag on or off'''
        if not self.exposed:
            if not self.flagged and self.master.flagCount > 0:
                self.flagged = True
                self.config(text='*')
                self.master.flagCount -= 1
            elif self.flagged:
                self.flagged = False
                self.config(text='')
                self.master.flagCount += 1
            self.master.changeFlagCounter()

    def exposeSquare(self, event=None):
        '''MinesweeperSquare.exposeSquare()
        exposes the square'''
        if not (self.flagged or self.exposed):
            self.exposed = True
            self.config(relief='sunken')
            if self.bomb:
                self.config(text='*', bg='red')
                self.master.gameDone(False)
            else:
                if self.touching > 0:
                    self.config(text=str(self.touching), fg=self.master.colormap[self.touching], bg='dark gray')
                else:
                    self.config(text='', bg='dark gray')
                if self.touching == 0:
                    self.master.exposeTouching(self.coord)
            self.master.changeFlagCounter()
            self.master.checkWin()

    def exposeBomb(self):
        '''MinesweeperSquare.exposeBomb()
        exposes the square if it's a bomb, marks flagged ones in red'''
        self.exposed = True
        self.config(relief='sunken', text='*', bg='red')

    def getBomb(self):
        '''MinesweeperSquare.getBomb() -> self.bomb
        returns whether the square is a bomb'''
        return self.bomb

    def setBomb(self):
        '''MinesweeperSquare.setBomb()
        sets the square as a bomb'''
        self.bomb = True

    def increaseBombs(self):
        '''MinesweeperSquare.increaseBombs()
        increases the amount of bombs'''
        self.touching += 1

class MinesweeperGrid(Frame):
    '''object for a Minesweeper grid'''

    def __init__(self, master, width, height, bombAmount):
        '''MinesweeperGrid(master, width, height, bombAmount)
        creates a new blank Minesweeper grid'''
        Frame.__init__(self, master, bg='black')
        self.grid()
        self.width = width
        self.height = height
        self.bombAmount = bombAmount
        self.flagCount = bombAmount
        self.squares = {}
        self.colormap = ['', 'blue', 'darkgreen', 'red', 'purple', 'maroon', 'cyan', 'black', 'dim gray']
        self._game_done = False

        for eachRow in range(self.height):
            for eachCol in range(self.width):
                coordinate = (eachRow, eachCol)
                square = MinesweeperSquare(self, coordinate)
                square.grid(row=eachRow, column=eachCol)
                self.squares[coordinate] = square

        bombCoord = random.sample(list(self.squares.keys()), self.bombAmount)
        for position in bombCoord:
            self.squares[position].setBomb()
            self.changeTouching(position)

        self.flagLabel = Label(self, text=str(self.flagCount))
        self.flagLabel.grid(row=self.height, column=0, columnspan=self.width)
        self.changeFlagCounter()

    def changeFlagCounter(self):
        '''MinesweeperGrid.changeFlagCounter()
        keeps the flag counter accurate'''
        self.flagLabel.config(text=str(self.flagCount))

    def changeTouching(self, coordinate):
        '''MinesweeperGrid.changeTouching()
        increases the amount of bombs in surrounding if the current is a bomb'''
        for directionRow in [-1, 0, 1]:
            for directionColumn in [-1, 0, 1]:
                if not (directionRow == 0 and directionColumn == 0):
                    touching = (coordinate[0] + directionRow, coordinate[1] + directionColumn)
                    if 0 <= touching[0] < self.height and 0 <= touching[1] < self.width:
                        self.squares[touching].increaseBombs()

    def exposeTouching(self, coordinate):
        '''MinesweeperGrid.exposeTouching()
        exposes touching squares if not bombs'''
        for directionRow in [-1, 0, 1]:
            for directionColumn in [-1, 0, 1]:
                if not (directionRow == 0 and directionColumn == 0):
                    touching = (coordinate[0] + directionRow, coordinate[1] + directionColumn)
                    if 0 <= touching[0] < self.height and 0 <= touching[1] < self.width:
                        touchingSquare = self.squares[touching]
                        if not touchingSquare.exposed and not touchingSquare.flagged:
                            touchingSquare.exposeSquare()

    def checkWin(self):
        '''MinesweeperGrid.checkWin()
        checks if the player has won the game'''
        for square in self.squares.values():
            if not square.getBomb() and not square.exposed:
                return False
        self.gameDone(True)
        return True

    def gameDone(self, winner):
        '''MinesweeperGrid.gameDone(winner)
        game is over'''
        if not self._game_done:
            self._game_done = True
            if winner:
                messagebox.showinfo('Minesweeper', 'Congratulations -- you won!', parent=self)
            else:
                for square in self.squares.values():
                    if square.getBomb():
                        square.exposeBomb()
                messagebox.showerror('Minesweeper', 'KABOOM! You lose.', parent=self)
            self.update_idletasks()  # Ensure all GUI updates are processed
            self.quit()

def play_minesweeper(width, height, bombAmount): 
    root = Tk()
    root.title('Minesweeper')
    mg = MinesweeperGrid(root, width, height, bombAmount)
    root.mainloop()

play_minesweeper(12, 10, 15)

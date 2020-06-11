import chess
import chess.svg
import chess.polyglot
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtSvg
import random
from evaluation import *
from search import *
import time




global board
svg_to_load = "move.svg"

def update_svg(svg):
    f = open("move.svg", "w")
    f.write(svg)
    f.close()

def computer_move():

    possible_moves = []
    with chess.polyglot.open_reader("data/Performance.bin") as reader:
        for entry in reader.find_all(board):
            #print(entry.move, entry.weight, entry.learn)
            possible_moves.append(entry.move)


    # play book move

    # play book move if possible

    if len(possible_moves) > 0:
        ind = random.randint(0, len(possible_moves) - 1)
        move = possible_moves[ind]
        board.push(move)
        svg = chess.svg.board(board=board)
        update_svg(svg)

    # otherwise search the best move
    else:
        start_time = time.time()
        max_depth = 5
        # iterative deepening
        #for d in range(1, depth_+1):
        bestval, pv_moves = search(board, -9999999, 9999999, depth=max_depth, ply=0, max_depth=max_depth, null_move=False)
        print(pv_moves)
        print("--- %s seconds ---" % (time.time() - start_time))
        #print(pv.PVlist)
        #print(len(flatten(pv.PVlist)))
        board.push(pv_moves[0])
        #print(bestval)

        svg = chess.svg.board(board=board)
        update_svg(svg)
    if (board.is_game_over()):
        print("GAME OVER!")

def make_move(move):
    move = chess.Move.from_uci(move)
    if (move in board.legal_moves):
        board.push(move)  # Make the move
        svg = chess.svg.board(board=board)
        update_svg(svg)
    else:
        print("Illegal move!")

def undo_move():
    board.pop()
    svg = chess.svg.board(board=board)
    update_svg(svg)


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Chess'
        self.left = 0
        self.top = 0
        self.width = 400
        self.height = 140
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #visualize board
        self.viewer = QtSvg.QSvgWidget()
        self.viewer.load("board_init.svg")
        self.viewer.show()

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)

        # Create a button in the window
        self.button_move = QPushButton('Move', self)
        self.button_move.move(20, 80)

        self.button_undo = QPushButton('Undo Move', self)
        self.button_undo.move(120, 80)

        self.button_computer = QPushButton('Computer Move', self)
        self.button_computer.move(220, 80)

        self.button_fen= QPushButton('Parse FEN', self)
        self.button_fen.move(320, 80)

        # connect button to function on_click
        self.button_move.clicked.connect(self.on_click_move)
        self.button_undo.clicked.connect(self.on_click_undo)
        self.button_computer.clicked.connect(self.on_click_computer)
        self.button_fen.clicked.connect(self.on_click_fen)

        self.show()

    @pyqtSlot()
    def on_click_move(self):
        move = self.textbox.text()
        make_move(move)
        self.viewer.load(svg_to_load)
        self.viewer.show()
        self.textbox.setText("")

    def on_click_fen(self):
        fen = self.textbox.text()
        board.set_fen(fen)
        svg = chess.svg.board(board=board)
        update_svg(svg)
        self.viewer.load(svg_to_load)
        self.viewer.show()
        self.textbox.setText("")


    def on_click_computer(self):
        computer_move()
        self.viewer.load(svg_to_load)
        self.viewer.show()

    def on_click_undo(self):
        undo_move()
        self.viewer.load(svg_to_load)
        self.viewer.show()

if __name__ == '__main__':

    board = chess.Board()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

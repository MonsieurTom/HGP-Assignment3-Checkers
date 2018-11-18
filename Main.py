from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QWidget, QHBoxLayout, QVBoxLayout, \
    QAction, QDialog, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QPainter, QColor, QIcon, QFont, QPixmap
import sys


class PlayerInfo:  # hold information of the player
    remaining = 20
    jumps = 0
    timer = QBasicTimer()
    playing = False

    def __init__(self, playing):
        self.playing = playing


class Piece:
    x = 0
    y = 0
    king = False
    alive = True
    team = ""

    def __init__(self, team, x, y):
        self.x = x
        self.y = y
        self.team = team


class Board(QFrame):
    gridSize = 10
    redPiecesList = []
    whitePiecesList = []
    player1 = None
    player2 = None
    x_translation = 0
    y_translation = 0

    def __init__(self, parent=None):
        super(Board, self).__init__(parent)

        self.setMinimumWidth(600)
        self.setMinimumHeight(600)

        self.x_translation = self.width() / 10
        self.y_translation = self.height() / 10

        self.initBoard()
        self.update()

    def initBoard(self):
        self.initPieceDictionaries()
        self.initPlayers()

    def initPlayers(self):
        self.player2 = None
        self.player1 = None

        self.player2 = PlayerInfo(False)
        self.player1 = PlayerInfo(True)

    def initPieceDictionaries(self):
        self.whitePiecesList = []
        self.redPiecesList = []

        pair = True

        i = 0
        redX = 0
        redY = 0
        whiteX = 1
        whitey = 9
        while i < 20:
            self.redPiecesList.append(Piece("red", redX, redY))
            self.whitePiecesList.append(Piece("white", whiteX, whitey))
            i = i + 1
            redX = redX + 2
            whiteX = whiteX + 2
            if redX >= 10 or whiteX >= 10:
                redY = redY + 1
                whitey = whitey - 1
                if pair:
                    redX = 1
                    whiteX = 0
                    pair = False
                else:
                    redX = 0
                    whiteX = 1
                    pair = True

    def paintEvent(self, event):
        painter = QPainter(self)

        self.drawBoard(painter)

        for red_piece in self.redPiecesList:
            if red_piece.alive:
                self.drawPiece(painter, red_piece)
        for white_piece in self.whitePiecesList:
            if white_piece.alive:
                self.drawPiece(painter, white_piece)

    def drawBoard(self, painter):
        white = True
        pair = False
        for x in range(self.gridSize):
            for y in range(self.gridSize):
                if pair is True:
                    if white is True:
                        color = QColor(255, 255, 255)
                        white = False
                    else:
                        color = QColor(0, 0, 0)
                        white = True
                if pair is False:
                    if white is True:
                        color = QColor(0, 0, 0)
                        white = False
                    else:
                        color = QColor(255, 255, 255)
                        white = True

                painter.setPen(color)
                painter.setBrush(color)
                painter.drawRect(int(x * self.x_translation), int(y * self.y_translation), int(self.x_translation),
                                 int(self.y_translation))
            if pair is True:
                pair = False
            else:
                pair = True

    def drawPiece(self, painter, piece):
        if piece.alive:
            rect = QRect(piece.x * self.x_translation + 5, piece.y * self.y_translation + 5,
                         int(self.x_translation) - 10, int(self.y_translation) - 10)
            if piece.team == "red":
                image = QPixmap("./img/checkers_red_token_normal.png")
            elif piece.team == "white":
                image = QPixmap("./img/checkers_white_token_normal.png")
            painter.drawPixmap(rect, image)

    def resizeEvent(self, event):
        self.x_translation = self.width() / 10
        self.y_translation = self.height() / 10


class ToolBar(QWidget):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)

        self.setMaximumWidth(200)
        self.setMinimumWidth(200)
        self.setMinimumHeight(600)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        # generals widgets
        self.toolbar_title = QLabel("Game Panel")
        self.toolbar_title.setFont(QFont("Times", 10, QFont.Bold))
        self.toolbar_title.setAlignment(Qt.AlignTop)

        # player1 widgets
        self.player1_icon = QLabel()
        self.player1_icon.setPixmap(QPixmap('./img/checkers_red_token_normal.png'))
        self.player1_icon.setFixedWidth(30)
        self.player1_icon.setFixedHeight(30)
        self.player1_your_turn = QLabel("Your turn")

        self.player1_header = QHBoxLayout()
        self.player1_header.addWidget(self.player1_icon)
        self.player1_header.addWidget(self.player1_your_turn)

        self.player1_name = QLabel("Player")
        self.player1_time = QLabel("Time Passed: 00:00")
        self.player1_remaining = QLabel("Remaining: 20")
        self.player1_jumps = QLabel("Jumps: 0")

        self.player1_toolbar = QVBoxLayout()
        self.player1_toolbar.setSpacing(2)
        self.player1_toolbar.addLayout(self.player1_header)
        self.player1_toolbar.addWidget(self.player1_name)
        self.player1_toolbar.addWidget(self.player1_time)
        self.player1_toolbar.addWidget(self.player1_remaining)
        self.player1_toolbar.addWidget(self.player1_jumps)
        self.player1_toolbar.setAlignment(Qt.AlignTop)

        # player2 widgets
        self.player2_icon = QLabel()
        self.player2_icon.setPixmap(QPixmap('./img/checkers_white_token_normal.png'))
        self.player2_icon.setFixedWidth(30)
        self.player2_icon.setFixedHeight(30)
        self.player2_your_turn = QLabel("Your turn")
        self.player2_header = QHBoxLayout()
        self.player2_header.addWidget(self.player2_icon)
        self.player2_header.addWidget(self.player2_your_turn)

        self.player2_name = QLabel("Opponent")
        self.player2_time = QLabel("Time Passed: 00:00")
        self.player2_remaining = QLabel("Remaining: 20")
        self.player2_jumps = QLabel("Jumps: 0")

        self.player2_toolbar = QVBoxLayout()
        self.player2_toolbar.setSpacing(2)
        self.player2_toolbar.addLayout(self.player2_header)
        self.player2_toolbar.addWidget(self.player2_name)
        self.player2_toolbar.addWidget(self.player2_time)
        self.player2_toolbar.addWidget(self.player2_remaining)
        self.player2_toolbar.addWidget(self.player2_jumps)
        self.player2_toolbar.setAlignment(Qt.AlignTop)

        # orginize in layout
        self.layout.addWidget(self.toolbar_title)
        self.layout.addLayout(self.player1_toolbar)
        self.layout.addLayout(self.player2_toolbar)

        self.setLayout(self.layout)
        self.layout.setSpacing(30)

    def resizeEvent(self, event):
        print('')


class MainWidget(QWidget):  # Central widget of the MainWindow, hold the toolbar and the board
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.layout = QHBoxLayout()
        self.toolBar = ToolBar(self)
        self.board = Board(self)

        self.layout.addWidget(self.toolBar)
        self.layout.addWidget(self.board)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def resizeEvent(self, event):
        print('')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Size of the window
        self.top = 400
        self.left = 400
        self.width = 800
        self.height = 600

        self.setWindowTitle("Draughts Game")
        self.setGeometry(self.top, self.left, self.width, self.height)

        # windows version
        self.setWindowIcon(QIcon("./img/chess_board_icon.png"))

        # Initialization Layouts and Widgets
        self.mainWidget = MainWidget(self)
        self.setCentralWidget(self.mainWidget)

        # Menu initialization
        mainMenu = self.menuBar()  # get the menuBar from the MainWindow

        # create some subMenu in it
        GameMenu = mainMenu.addMenu(" Game")
        HelpMenu = mainMenu.addMenu(" Help")

        #  reset
        ResetAction = QAction("Reset", self)
        ResetAction.setShortcut("Ctrl+S")
        GameMenu.addAction(ResetAction)
        ResetAction.triggered.connect(
            self.reset)  # when the menu option is selected or the shortcut is used the save menu is triggered

        #  help
        HelpAction = QAction("Help", self)
        HelpAction.setShortcut("Ctrl+H")
        HelpMenu.addAction(HelpAction)
        HelpAction.triggered.connect(
            self.help)  # when the menu option is selected or the shortcut is used the clear menu is triggered

    def reset(self):
        print("reset")

    def help(self):
        dialog = QDialog()
        dialog.setWindowTitle("Help")
        layout = QVBoxLayout()

        labelAuthors = QLabel("Authors: Lenormand Tom - Habchi Salim")
        labelAuthors.setFont(QFont('Times', 10))
        labelAuthors.setAlignment(Qt.AlignBottom)

        layout.addWidget(labelAuthors)

        dialog.setLayout(layout)

        dialog.exec_()

    def resizeEvent(self, event):
        print('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
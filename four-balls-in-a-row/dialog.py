import sys, random
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QRect, QTimer

class DifficultyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор сложности")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout(self)
        
        title = QLabel("Выберите уровень сложности")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.combo = QComboBox()
        self.combo.addItems(["Легкий", "Средний", "Высокий"])
        
        start_btn = QPushButton("Начать игру")
        
        layout.addWidget(title)
        layout.addWidget(self.combo)
        layout.addWidget(start_btn)
        
        start_btn.clicked.connect(self.accept)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                border-radius: 15px;
            }
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                min-height: 40px;
                font-size: 16px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
            QPushButton {
                background-color: #5c90ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #4a7ae0;
            }
            QPushButton:pressed {
                background-color: #3e68c7;
            }
        """)

class Game:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[0] * cols for _ in range(rows)]
        self.current_player = 1

    def drop_piece(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return True
        return False

    def check_winner(self):
        # Проверка горизонтали и вертикали
        for row in range(self.rows):
            for col in range(self.cols-3):
                if all(self.board[row][col+i] == self.current_player for i in range(4)):
                    return True
                if row < self.rows-3 and all(self.board[row+i][col] == self.current_player for i in range(4)):
                    return True
        
        # Проверка диагоналей
        for row in range(self.rows-3):
            for col in range(self.cols-3):
                if all(self.board[row+i][col+i] == self.current_player for i in range(4)):
                    return True
                if all(self.board[row+i][col+3-i] == self.current_player for i in range(4)):
                    return True
        return False

    def ai_move(self, difficulty):
        if difficulty == "Легкий":
            cols = [c for c in range(self.cols) if self.board[0][c] == 0]
            return random.choice(cols) if cols else None
        
        # Для остальных уровней - простая блокировка и победа
        for col in range(self.cols):
            if self.board[0][col] == 0:
                self.board[self._get_row(col)][col] = 2
                if self.check_winner():
                    self.board[self._get_row(col)][col] = 0
                    return col
                self.board[self._get_row(col)][col] = 0
                
                self.board[self._get_row(col)][col] = 1
                if self.check_winner():
                    self.board[self._get_row(col)][col] = 0
                    return col
                self.board[self._get_row(col)][col] = 0
        
        for col in [3, 2, 4, 1, 5, 0, 6]:
            if self.board[0][col] == 0:
                return col
        return None

    def _get_row(self, col):
        for row in reversed(range(self.rows)):
            if self.board[row][col] == 0:
                return row
        return -1

class GameBoard(QWidget):
    def __init__(self, game, on_click):
        super().__init__()
        self.game = game
        self.on_click = on_click
        self.cell_size = 80
        self.setMinimumSize(600, 500)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.cell_size * self.game.cols
        height = self.cell_size * self.game.rows
        start_x = (self.width() - width) // 2
        start_y = (self.height() - height) // 2

        painter.setBrush(QBrush(QColor("#2d2d2d")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(start_x-5, start_y-5, width+10, height+10, 15, 15)

        for row in range(self.game.rows):
            for col in range(self.game.cols):
                x = start_x + col * self.cell_size
                y = start_y + row * self.cell_size
                
                painter.setBrush(QBrush(QColor("#1a1a1a")))
                painter.drawRoundedRect(x+5, y+5, self.cell_size-10, self.cell_size-10, 10, 10)
                
                if self.game.board[row][col] != 0:
                    painter.setBrush(QBrush(QColor("#ff5252" if self.game.board[row][col] == 1 else "#5c90ff")))
                    painter.drawEllipse(x+10, y+10, self.cell_size-20, self.cell_size-20)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            width = self.cell_size * self.game.cols
            start_x = (self.width() - width) // 2
            col = int((event.position().x() - start_x) // self.cell_size)
            if 0 <= col < self.game.cols:
                self.on_click(col)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Четыре в ряд")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #5c90ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #4a7ae0;
            }
            QMessageBox {
                background-color: #1a1a1a;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 16px;
            }
            QMessageBox QPushButton {
                min-width: 100px;
                margin: 10px;
            }
        """)
        
        self.game = Game()
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)
        
        self.status = QLabel("Ваш ход")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        reset_btn = QPushButton("Новая игра")
        reset_btn.clicked.connect(self.reset_game)
        
        self.board = GameBoard(self.game, self.on_column_click)
        
        layout.addWidget(self.status)
        layout.addWidget(reset_btn)
        layout.addWidget(self.board)
        
        self.ai_timer = QTimer()
        self.ai_timer.timeout.connect(self.ai_turn)
        
        self.show_difficulty_dialog()

    def show_difficulty_dialog(self):
        dialog = DifficultyDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.difficulty = dialog.combo.currentText()
        else:
            self.difficulty = "Легкий"

    def on_column_click(self, col):
        if self.game.board[0][col] == 0 and self.game.current_player == 1:
            if self.game.drop_piece(col):
                self.board.update()
                if self.game.check_winner():
                    self.show_winner("Вы победили!")
                else:
                    self.game.current_player = 2
                    self.status.setText("Ход ИИ")
                    self.ai_timer.start(1000)

    def ai_turn(self):
        self.ai_timer.stop()
        col = self.game.ai_move(self.difficulty)
        if col is not None:
            self.game.drop_piece(col)
            self.board.update()
            if self.game.check_winner():
                self.show_winner("ИИ победил!")
            else:
                self.game.current_player = 1
                self.status.setText("Ваш ход")

    def show_winner(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle("Игра окончена")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        self.reset_game()

    def reset_game(self):
        self.show_difficulty_dialog()
        self.game = Game()
        self.game.current_player = 1
        self.status.setText("Ваш ход")
        self.board.game = self.game
        self.board.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
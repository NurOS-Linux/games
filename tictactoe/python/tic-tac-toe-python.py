import sys
import random
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont
from PyQt6.QtCore import Qt, QRect, QTimer

class DifficultyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Выбор сложности")
        self.setFixedSize(300, 250)
        layout = QVBoxLayout(self)
        
        title = QLabel("Выберите уровень сложности")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title)
        
        for difficulty in ["Легкий", "Средний", "Сложный"]:
            btn = QPushButton(difficulty)
            btn.clicked.connect(lambda x, d=difficulty: self.choose_difficulty(d))
            layout.addWidget(btn)
        
        self.selected_difficulty = "Легкий"
        
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                border-radius: 15px;
            }
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 15px;
                font-size: 16px;
                margin: 10px 20px;
            }
            QPushButton:hover {
                background-color: #5c90ff;
            }
            QPushButton:pressed {
                background-color: #4a7ae0;
            }
        """)

    def choose_difficulty(self, difficulty):
        self.selected_difficulty = difficulty
        self.accept()

class TicTacToeBoard(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.cell_size = 150
        self.setFixedSize(450, 450)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), QColor("#1a1a1a"))

        painter.setPen(QColor("#2d2d2d"))
        for i in range(1, 3):
            painter.drawLine(i * self.cell_size, 0, i * self.cell_size, 450)
            painter.drawLine(0, i * self.cell_size, 450, i * self.cell_size)

        for row in range(3):
            for col in range(3):
                if self.game.board[row][col]:
                    rect = QRect(col * self.cell_size, row * self.cell_size,
                               self.cell_size, self.cell_size)
                    painter.setFont(QFont(None, 60))
                    if self.game.board[row][col] == 'X':
                        painter.setPen(QColor("#ff5252"))
                    else:
                        painter.setPen(QColor("#5c90ff"))
                    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, 
                                   self.game.board[row][col])

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.game.game_over:
            col = int(event.position().x() // self.cell_size)
            row = int(event.position().y() // self.cell_size)
            if self.game.make_move(row, col):
                self.update()
                self.parent().parent().check_game_state()

class TicTacToeGame:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.difficulty = "Легкий"
        self.game_over = False

    def make_move(self, row, col):
        if not self.game_over and 0 <= row < 3 and 0 <= col < 3 and not self.board[row][col]:
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        # Проверка строк и столбцов
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return self.board[0][i]
        
        # Проверка диагоналей
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return self.board[0][2]
        
        # Проверка на ничью
        if all(all(cell != '' for cell in row) for row in self.board):
            return 'Draw'
        return None

    def ai_move(self):
        if self.difficulty == "Легкий":
            self.ai_move_easy()
        elif self.difficulty == "Средний":
            self.ai_move_medium()
        else:
            self.ai_move_hard()

    def ai_move_easy(self):
        """Случайный ход с приоритетом центра и углов"""
        priority_moves = [
            (1, 1),  # центр
            (0, 0), (0, 2), (2, 0), (2, 2),  # углы
            (0, 1), (1, 0), (1, 2), (2, 1)  # стороны
        ]
        
        # Пробуем приоритетные позиции
        for row, col in priority_moves:
            if self.board[row][col] == '':
                if random.random() < 0.7:  # 70% шанс выбрать приоритетную позицию
                    self.board[row][col] = 'O'
                    self.current_player = 'X'
                    return

        # Если не выбрали приоритетную, выбираем случайную
        empty_cells = [(r, c) for r in range(3) for c in range(3) 
                      if self.board[r][c] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = 'O'
            self.current_player = 'X'

    def ai_move_medium(self):
        """Улучшенный средний уровень"""
        if random.random() < 0.2:  # 20% шанс на ошибку
            self.ai_move_easy()
            return

        # Проверка на победу ИИ
        if self._try_winning_move('O'):
            return

        # Блокировка победы игрока
        if self._try_winning_move('X'):
            return

        # Создание или блокировка вилки
        if self._try_fork():
            return

        self.ai_move_easy()

    def _try_winning_move(self, player):
        """Проверяет возможность победы"""
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = player
                    if self.check_winner() == player:
                        if player == 'O':
                            self.current_player = 'X'
                        else:
                            self.board[row][col] = 'O'
                            self.current_player = 'X'
                        return True
                    self.board[row][col] = ''
        return False

    def _try_fork(self):
        """Создание или блокировка вилки"""
        corner_pairs = [(0,0,0,2), (0,0,2,0), (0,2,2,2), (2,0,2,2)]
        for c1_row, c1_col, c2_row, c2_col in corner_pairs:
            if (self.board[c1_row][c1_col] == self.board[c2_row][c2_col] == 'X' and
                self.board[1][1] == ''):
                self.board[1][1] = 'O'
                self.current_player = 'X'
                return True

        if self.board[1][1] == 'X':
            if self.board[0][0] == self.board[2][2] == '':
                self.board[0][0] = 'O'
                self.current_player = 'X'
                return True
            if self.board[0][2] == self.board[2][0] == '':
                self.board[0][2] = 'O'
                self.current_player = 'X'
                return True
        return False

    def ai_move_hard(self):
        """Непобедимый AI используя минимакс"""
        best_score = float('-inf')
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    self.board[row][col] = 'O'
                    score = self.minimax(False)
                    self.board[row][col] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move:
            self.board[best_move[0]][best_move[1]] = 'O'
            self.current_player = 'X'

    def minimax(self, is_maximizing):
        result = self.check_winner()
        if result == 'O':
            return 1
        elif result == 'X':
            return -1
        elif result == 'Draw':
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == '':
                        self.board[row][col] = 'O'
                        score = self.minimax(False)
                        self.board[row][col] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == '':
                        self.board[row][col] = 'X'
                        score = self.minimax(True)
                        self.board[row][col] = ''
                        best_score = min(score, best_score)
            return best_score

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Крестики-нолики")
        self.setStyleSheet("background-color: #1a1a1a;")
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.status = QLabel("Ваш ход")
        self.status.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin: 20px;
        """)
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.game = TicTacToeGame()
        self.board = TicTacToeBoard(self.game)
        
        reset_btn = QPushButton("Новая игра")
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #5c90ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                margin: 20px 50px;
            }
            QPushButton:hover {
                background-color: #4a7ae0;
            }
        """)
        reset_btn.clicked.connect(self.reset_game)
        
        layout.addWidget(self.status)
        layout.addWidget(self.board)
        layout.addWidget(reset_btn)
        
        self.setCentralWidget(widget)
        
        self.ai_timer = QTimer()
        self.ai_timer.timeout.connect(self.ai_turn)
        
        self.show_difficulty_dialog()

    def show_difficulty_dialog(self):
        dialog = DifficultyDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.game.difficulty = dialog.selected_difficulty

    def ai_turn(self):
        self.ai_timer.stop()
        if not self.game.game_over:
            self.game.ai_move()
            self.board.update()
            self.check_game_state()

    def check_game_state(self):
        winner = self.game.check_winner()
        if winner:
            self.game.game_over = True
            if winner == 'Draw':
                msg = "НИЧЬЯ!"
                color = "#FFA500"
            else:
                msg = "ВЫ ПОБЕДИЛИ!" if winner == 'X' else "ИИ ПОБЕДИЛ!"
                color = "#32CD32" if winner == 'X' else "#FF4444"
            
            result_dialog = QDialog(self)
            result_dialog.setWindowTitle("Игра окончена")
            result_dialog.setFixedSize(400, 200)
            
            layout = QVBoxLayout(result_dialog)
            
            result_label = QLabel(msg)
            result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            result_label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    font-size: 32px;
                    font-weight: bold;
                    padding: 20px;
                }}
            """)
            
            play_again_btn = QPushButton("Играть снова")
            play_again_btn.clicked.connect(lambda: [result_dialog.accept(), self.reset_game()])
            play_again_btn.setStyleSheet("""
                QPushButton {
                    background-color: #5c90ff;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 15px;
                    font-size: 18px;
                    margin: 20px 50px;
                }
                QPushButton:hover {
                    background-color: #4a7ae0;
                }
            """)
            
            layout.addWidget(result_label)
            layout.addWidget(play_again_btn)
            
            result_dialog.setStyleSheet("""
                QDialog {
                    background-color: #1a1a1a;
                    border: 2px solid #2d2d2d;
                    border-radius: 15px;
                }
            """)
            
            result_dialog.exec()
        elif self.game.current_player == 'O':
            self.status.setText("Ход ИИ")
            self.ai_timer.start(800)  # Уменьшенная задержка для более динамичной игры
        else:
            self.status.setText("Ваш ход")

    def reset_game(self):
        self.show_difficulty_dialog()
        self.game = TicTacToeGame()
        self.game.difficulty = self.game.difficulty
        self.status.setText("Ваш ход")
        self.board.game = self.game
        self.board.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
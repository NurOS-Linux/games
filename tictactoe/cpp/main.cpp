#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QWidget>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QDialog>
#include <QtCore/QTimer>
#include <random>

class TicTacToe : public QMainWindow {
    Q_OBJECT
private:
    QLabel* statusLabel;
    QPushButton* buttons[3][3];
    char board[3][3];
    char currentPlayer = 'X';
    bool gameOver = false;
    QString difficulty = "Легкий";
    QTimer* aiTimer;

public:
    TicTacToe(QWidget* parent = nullptr) : QMainWindow(parent) {
        setWindowTitle("Крестики-нолики");
        setFixedSize(450, 550);
        setStyleSheet("background-color: #1a1a1a;");

        auto* centralWidget = new QWidget(this);
        auto* layout = new QVBoxLayout(centralWidget);

        statusLabel = new QLabel("Ваш ход");
        statusLabel->setStyleSheet("color: white; font-size: 24px; font-weight: bold; margin: 20px;");
        statusLabel->setAlignment(Qt::AlignCenter);
        layout->addWidget(statusLabel);

        auto* grid = new QGridLayout();
        grid->setSpacing(10);

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                buttons[i][j] = new QPushButton();
                buttons[i][j]->setFixedSize(120, 120);
                buttons[i][j]->setStyleSheet(
                    "QPushButton {"
                    "   background-color: #2d2d2d;"
                    "   color: white;"
                    "   border: none;"
                    "   border-radius: 10px;"
                    "   font-size: 48px;"
                    "   font-weight: bold;"
                    "}"
                    "QPushButton:hover { background-color: #3d3d3d; }"
                );
                connect(buttons[i][j], &QPushButton::clicked, [=]{ handleClick(i, j); });
                grid->addWidget(buttons[i][j], i, j);
                board[i][j] = ' ';
            }
        }
        layout->addLayout(grid);

        auto* resetBtn = new QPushButton("Новая игра");
        resetBtn->setStyleSheet(
            "QPushButton {"
            "   background-color: #5c90ff;"
            "   color: white;"
            "   border: none;"
            "   border-radius: 5px;"
            "   padding: 15px;"
            "   font-size: 16px;"
            "   margin: 20px 50px;"
            "}"
            "QPushButton:hover { background-color: #4a7ae0; }"
        );
        connect(resetBtn, &QPushButton::clicked, this, &TicTacToe::resetGame);
        layout->addWidget(resetBtn);

        setCentralWidget(centralWidget);
        
        aiTimer = new QTimer(this);
        aiTimer->setSingleShot(true);
        connect(aiTimer, &QTimer::timeout, this, &TicTacToe::aiMove);

        showDifficultyDialog();
    }

private slots:
    void handleClick(int row, int col) {
        if (board[row][col] == ' ' && !gameOver && currentPlayer == 'X') {
            makeMove(row, col, 'X');
            if (!checkGameEnd()) {
                currentPlayer = 'O';
                statusLabel->setText("Ход ИИ");
                aiTimer->start(800);
            }
        }
    }

    void aiMove() {
        if (!gameOver) {
            if (difficulty == "Легкий") makeRandomMove();
            else if (difficulty == "Средний") makeMediumMove();
            else makeSmartMove();

            currentPlayer = 'X';
            if (!checkGameEnd()) 
                statusLabel->setText("Ваш ход");
        }
    }

private:
    void showDifficultyDialog() {
        QDialog dialog(this);
        dialog.setWindowTitle("Выбор сложности");
        dialog.setFixedSize(300, 200);
        dialog.setStyleSheet("background-color: #1a1a1a;");

        auto* layout = new QVBoxLayout(&dialog);
        
        for (const QString& diff : {"Легкий", "Средний", "Сложный"}) {
            auto* btn = new QPushButton(diff);
            btn->setStyleSheet(
                "QPushButton {"
                "   background-color: #2d2d2d;"
                "   color: white;"
                "   border: none;"
                "   padding: 15px;"
                "   font-size: 16px;"
                "   margin: 5px 20px;"
                "}"
                "QPushButton:hover { background-color: #5c90ff; }"
            );
            connect(btn, &QPushButton::clicked, [&, diff]{ 
                difficulty = diff; 
                dialog.accept(); 
            });
            layout->addWidget(btn);
        }
        dialog.exec();
    }

    void makeMove(int row, int col, char player) {
        board[row][col] = player;
        buttons[row][col]->setText(QString(player));
        buttons[row][col]->setStyleSheet(
            buttons[row][col]->styleSheet() +
            QString("color: %1;").arg(player == 'X' ? "#ff5252" : "#5c90ff")
        );
    }

    bool checkGameEnd() {
        char winner = checkWinner();
        if (winner != ' ') {
            gameOver = true;
            QString msg = winner == 'X' ? "Вы победили!" : "ИИ победил!";
            QString color = winner == 'X' ? "#32CD32" : "#FF4444";
            showResult(msg, color);
            return true;
        }
        
        bool isDraw = true;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                if (board[i][j] == ' ') 
                    isDraw = false;

        if (isDraw) {
            gameOver = true;
            showResult("Ничья!", "#FFA500");
            return true;
        }
        return false;
    }

    char checkWinner() {
        for (int i = 0; i < 3; i++) {
            if (board[i][0] != ' ' && board[i][0] == board[i][1] && board[i][1] == board[i][2])
                return board[i][0];
            if (board[0][i] != ' ' && board[0][i] == board[1][i] && board[1][i] == board[2][i])
                return board[0][i];
        }
        if (board[0][0] != ' ' && board[0][0] == board[1][1] && board[1][1] == board[2][2])
            return board[0][0];
        if (board[0][2] != ' ' && board[0][2] == board[1][1] && board[1][1] == board[2][0])
            return board[0][2];
        return ' ';
    }

    void makeRandomMove() {
        std::vector<std::pair<int, int>> empty;
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                if (board[i][j] == ' ') 
                    empty.push_back({i, j});

        if (!empty.empty()) {
            auto [row, col] = empty[rand() % empty.size()];
            makeMove(row, col, 'O');
        }
    }

    void makeMediumMove() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == ' ') {
                    board[i][j] = 'O';
                    if (checkWinner() == 'O') {
                        board[i][j] = ' ';
                        makeMove(i, j, 'O');
                        return;
                    }
                    board[i][j] = ' ';
                }
            }
        }
        makeRandomMove();
    }

    void makeSmartMove() {
        if (board[1][1] == ' ') {
            makeMove(1, 1, 'O');
            return;
        }
        makeMediumMove();
    }

    void showResult(const QString& msg, const QString& color) {
        QDialog dialog(this);
        dialog.setFixedSize(300, 150);
        dialog.setStyleSheet("background-color: #1a1a1a;");

        auto* layout = new QVBoxLayout(&dialog);
        auto* label = new QLabel(msg);
        label->setStyleSheet(QString("color: %1; font-size: 24px; font-weight: bold;").arg(color));
        label->setAlignment(Qt::AlignCenter);
        layout->addWidget(label);

        auto* btn = new QPushButton("OK");
        btn->setStyleSheet(
            "background-color: #5c90ff; color: white; padding: 10px;"
            "border: none; border-radius: 5px;"
        );
        connect(btn, &QPushButton::clicked, &dialog, &QDialog::accept);
        layout->addWidget(btn);

        dialog.exec();
    }

    void resetGame() {
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++) {
                board[i][j] = ' ';
                buttons[i][j]->setText("");
            }
        gameOver = false;
        currentPlayer = 'X';
        statusLabel->setText("Ваш ход");
        showDifficultyDialog();
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    TicTacToe game;
    game.show();
    return app.exec();
}

#include "main.moc"
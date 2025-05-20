<?php
$sections = [0, 0, 0, 0, 0, 0, 0, 0, 0];
$player = 1; // Игрок начинает первым

function printGame($array) {
    $i = 0;
    foreach ($array as $elem) {
        $i++;
        switch ($elem) {
            case 0:
                print(". ");
                break;
            case 1:
                print("o ");
                break;
            case 2:
                print("x ");
                break;
        }
        if ($i % 3 == 0) print("\n");
    }
}

function playerEnter($array, $player) {
    if ($player == 1) { // Игрок
        $enter = readline("Ваш ход (введите номер клетки от 0 до 8): ");
        if ($array[$enter] == 0) {
            $array[$enter] = $player;
            return $array;
        } else {
            echo "Клетка занята! Попробуйте снова.\n";
            return -1;
        }
    } else { // ИИ
        echo "Ход компьютера...\n";
        $array = makeAiMove($array);
        return $array;
    }
}

function changePlayer($player) {
    return ($player == 1) ? 2 : 1;
}

function checkWin($array) {
    $winningCombinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ];

    foreach ($winningCombinations as $combination) {
        if ($array[$combination[0]] == $array[$combination[1]] &&
            $array[$combination[1]] == $array[$combination[2]] &&
            $array[$combination[0]] != 0) {
            return $array[$combination[0]];
        }
    }
    return 0;
}

function makeAiMove($array) {
    // Проверяем, есть ли возможность выиграть
    for ($i = 0; $i < 9; $i++) {
        if ($array[$i] == 0) {
            $array[$i] = 2; // Попробуем поставить "x"
            if (checkWin($array) == 2) {
                return $array;
            }
            $array[$i] = 0; // Возвращаем клетку в исходное состояние
        }
    }

    // Проверяем, нужно ли блокировать игрока
    for ($i = 0; $i < 9; $i++) {
        if ($array[$i] == 0) {
            $array[$i] = 1; // Попробуем поставить "o"
            if (checkWin($array) == 1) {
                $array[$i] = 2; // Блокируем игрока
                return $array;
            }
            $array[$i] = 0; // Возвращаем клетку в исходное состояние
        }
    }

    // Если нет выигрышных комбинаций, делаем случайный ход
    do {
        $move = rand(0, 8);
    } while ($array[$move] != 0);

    $array[$move] = 2;
    return $array;
}

while (true) {
    printGame($sections);
    $pl = playerEnter($sections, $player);
    if ($pl == -1) continue;
    else $sections = $pl;

    $player = changePlayer($player);

    if (checkWin($sections) != 0) {
        printGame($sections);
        echo "Игрок " . checkWin($sections) . " победил!\n";
        break;
    }

    // Проверка на ничью
    if (!in_array(0, $sections)) {
        printGame($sections);
        echo "Ничья!\n";
        break;
    }
}
?>

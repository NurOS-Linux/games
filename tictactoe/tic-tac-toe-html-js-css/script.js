// Получаем все ячейки игры
const cells = document.querySelectorAll('.cell');
const currentPlayerDisplay = document.getElementById('current-player');
const resetButton = document.getElementById('reset-button');
let currentPlayer = 'X'; // Игрок всегда начинает с X
let gameActive = true;
let gameState = ['', '', '', '', '', '', '', '', ''];

// Выигрышные комбинации
const winningCombinations = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6]
];

// Функция для проверки победителя
function checkWinner() {
  for (let combination of winningCombinations) {
    const [a, b, c] = combination;
    if (gameState[a] && gameState[a] === gameState[b] && gameState[a] === gameState[c]) {
      gameActive = false;
      return gameState[a];
    }
  }
  if (!gameState.includes('')) {
    gameActive = false;
    return 'draw';
  }
  return null;
}

// Обработчик клика по ячейке
function handleCellClick(event) {
  const cell = event.target;
  const index = cell.dataset.index;

  if (gameState[index] !== '' || !gameActive || currentPlayer !== 'X') return; // Игрок может ходить только за X

  gameState[index] = currentPlayer;
  cell.textContent = currentPlayer;

  const winner = checkWinner();
  if (winner) {
    if (winner === 'draw') {
      alert('Ничья!');
    } else {
      alert(`Игрок ${winner} победил!`);
    }
    gameActive = false;
    return;
  }

  currentPlayer = 'O'; // Передаём ход ИИ
  currentPlayerDisplay.textContent = currentPlayer;

  // Если игра активна, запускаем ход ИИ
  if (gameActive) {
    setTimeout(aiMove, 500); // ИИ делает ход через 500 мс
  }
}

// Функция хода ИИ
function aiMove() {
  if (!gameActive) return;

  // Простая логика ИИ: выбираем случайную свободную ячейку
  const availableCells = gameState.map((cell, index) => (cell === '' ? index : null)).filter(index => index !== null);
  const randomIndex = availableCells[Math.floor(Math.random() * availableCells.length)];

  gameState[randomIndex] = 'O';
  cells[randomIndex].textContent = 'O';

  const winner = checkWinner();
  if (winner) {
    if (winner === 'draw') {
      alert('Ничья!');
    } else {
      alert(`Игрок ${winner} победил!`);
    }
    gameActive = false;
    return;
  }

  currentPlayer = 'X'; // Передаём ход игроку
  currentPlayerDisplay.textContent = currentPlayer;
}

// Функция сброса игры
function resetGame() {
  gameState = ['', '', '', '', '', '', '', '', ''];
  gameActive = true;
  currentPlayer = 'X';
  currentPlayerDisplay.textContent = currentPlayer;
  cells.forEach(cell => cell.textContent = '');
}

// Назначаем обработчики событий
cells.forEach(cell => cell.addEventListener('click', handleCellClick));
resetButton.addEventListener('click', resetGame);

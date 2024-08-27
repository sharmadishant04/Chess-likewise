const gameState = {
    currentPlayer: 'A',
    selectedPiece: null,
    board: Array(25).fill(null),
    moveHistory: [],
    killedPieces: { A: [], B: [] }
};

function renderBoard() {
    const gameBoard = document.getElementById('game-board');
    gameBoard.innerHTML = '';

    for (let i = 0; i < 25; i++) {
        const cell = document.createElement('div');
        cell.dataset.index = i;
        const piece = gameState.board[i];
        if (piece) {
            cell.textContent = piece;
        }
        cell.addEventListener('click', () => handleCellClick(i));
        gameBoard.appendChild(cell);
    }
}

function initializeGame() {
    gameState.board[0] = 'A-P1';
    gameState.board[1] = 'A-P2';
    gameState.board[2] = 'A-P3';
    gameState.board[3] = 'A-P4';
    gameState.board[4] = 'A-P5';
    gameState.board[20] = 'B-P1';
    gameState.board[21] = 'B-P2';
    gameState.board[22] = 'B-P3';
    gameState.board[23] = 'B-P4';
    gameState.board[24] = 'B-P5';
    renderBoard();
}

function handleCellClick(index) {
    const piece = gameState.board[index];
    if (gameState.selectedPiece === null) {
        if (piece && piece.startsWith(gameState.currentPlayer)) {
            gameState.selectedPiece = index;
        }
    } else {
        if (isValidMove(gameState.selectedPiece, index)) {
            makeMove(gameState.selectedPiece, index);
        }
        gameState.selectedPiece = null;
    }
    renderBoard();
}

function isValidMove(fromIndex, toIndex) {
    const piece = gameState.board[fromIndex];
    const targetPiece = gameState.board[toIndex];
    const rowDifference = Math.abs(Math.floor(fromIndex / 5) - Math.floor(toIndex / 5));
    const colDifference = Math.abs((fromIndex % 5) - (toIndex % 5));

    if (piece.includes('P') && rowDifference <= 1 && colDifference <= 1) {
        if (targetPiece && targetPiece.startsWith(gameState.currentPlayer)) {
            return false;
        }
        return true;
    }
    return false;
}

function makeMove(fromIndex, toIndex) {
    const piece = gameState.board[fromIndex];
    const targetPiece = gameState.board[toIndex];

    if (targetPiece && !targetPiece.startsWith(gameState.currentPlayer)) {
        gameState.killedPieces[gameState.currentPlayer].push(targetPiece);
        updateKilledPieces();
    }

    gameState.board[toIndex] = piece;
    gameState.board[fromIndex] = null;
    gameState.moveHistory.push(`${piece} moved from ${fromIndex} to ${toIndex}`);
    updateMoveHistory();
    gameState.currentPlayer = gameState.currentPlayer === 'A' ? 'B' : 'A';
}

function updateMoveHistory() {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = '';
    gameState.moveHistory.forEach(move => {
        const li = document.createElement('li');
        li.textContent = move;
        historyList.appendChild(li);
    });
}

function updateKilledPieces() {
    const killedPiecesP1 = document.getElementById('killed-pieces-p1');
    const killedPiecesP2 = document.getElementById('killed-pieces-p2');
    killedPiecesP1.innerHTML = '';
    killedPiecesP2.innerHTML = '';
    gameState.killedPieces.A.forEach(piece => {
        const li = document.createElement('li');
        li.textContent = piece;
        killedPiecesP1.appendChild(li);
    });
    gameState.killedPieces.B.forEach(piece => {
        const li = document.createElement('li');
        li.textContent = piece;
        killedPiecesP2.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initializeGame();
});

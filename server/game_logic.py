class Game:
    def __init__(self):
        self.board = [['' for _ in range(5)] for _ in range(5)]
        self.killed_pieces = {'Player 1': [], 'Player 2': []}
        self.setup_board()

    def setup_board(self):
        self.board[0] = ['P1', 'H1', 'H2', '', '']
        self.board[4] = ['P2', 'H2', 'H1', '', '']

    def process_move(self, move, row, col):
        character = self.board[row][col]
        if not character:
            return {'valid': False, 'error': 'Invalid move: No character at selected position'}

        player = 'Player 1' if character.endswith('1') else 'Player 2'
        opponent = 'Player 2' if player == 'Player 1' else 'Player 1'
        target_row, target_col = self.calculate_target(move, row, col)

        if not self.is_within_bounds(target_row, target_col):
            return {'valid': False, 'error': 'Invalid move: Out of bounds'}

        target_character = self.board[target_row][target_col]
        if target_character:
            if target_character.endswith(player[-1]):
                return {'valid': False, 'error': 'Invalid move: Cannot target own piece'}
            else:
                self.killed_pieces[opponent].append(target_character)
                self.board[target_row][target_col] = character
                self.board[row][col] = ''
                return {'valid': True, 'killed': target_character}
        else:
            self.board[target_row][target_col] = character
            self.board[row][col] = ''
            return {'valid': True}

    def calculate_target(self, move, row, col):
        if move == 'L':
            return row, col - 1
        elif move == 'R':
            return row, col + 1
        elif move == 'F':
            return row - 1, col
        elif move == 'B':
            return row + 1, col

    def is_within_bounds(self, row, col):
        return 0 <= row < 5 and 0 <= col < 5

    def get_killed_pieces(self):
        return self.killed_pieces

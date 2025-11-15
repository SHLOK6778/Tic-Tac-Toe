import math

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.human = 'O'
        self.ai = 'X'

    def print_board(self):
        for row in [self.board[i * 3 : (i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # tells what number corresponds to what box
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check row
        row_ind = square // 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([s == letter for s in row]):
            return True
        # check column
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([s == letter for s in column]):
            return True
        # check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diagonal2]):
                return True
        return False

    def minimax(self, state, player):
        max_player = self.ai
        other_player = 'O' if player == 'X' else 'X'

        # check if the previous move is a winner
        if self.current_winner == other_player:
            return {
                'position': None,
                'score': 1 * (self.num_empty_squares() + 1) if other_player == max_player else -1 * (self.num_empty_squares() + 1)
            }
        elif not self.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in self.available_moves():
            # make a move
            self.board[possible_move] = player
            if self.winner(possible_move, player):
                self.current_winner = player
            sim_score = self.minimax(state, other_player)

            # undo the move
            self.board[possible_move] = ' '
            self.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best

    def play_game(self):
        print("Welcome to Tic Tac Toe!")
        self.print_board_nums()

        letter = 'O'  # Human always starts first
        while self.empty_squares():
            if letter == self.human:
                square = int(input('Your move (0-8): '))
                if not self.make_move(square, letter):
                    print('Invalid move. Try again.')
                    continue
            else:
                print('AI is making a move...')
                square = self.minimax(self.board, self.ai)['position']
                self.make_move(square, letter)

            self.print_board()
            print('')

            if self.current_winner:
                if letter == self.human:
                    print('You win!')
                else:
                    print('AI wins!')
                return

            letter = 'O' if letter == 'X' else 'X'
        print('It\'s a tie!')

if __name__ == '__main__':
    t = TicTacToe()
    t.play_game()

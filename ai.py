import numpy as np
from easyAI import TwoPlayersGame


class SeptTurn(TwoPlayersGame):
    def __init__(self, players, board_size=12):
        self.players = players
        self.board_size = board_size
        self.board = np.zeros(board_size, dtype=int)
        self.board[[0, 6]] = 1
        self.board[[1, 7]] = 2
        self.board[[3, 9]] = -1
        self.board[[4, 10]] = -2
        self.nplayer = 1  # player 1 starts.

    def possible_moves(self):
        possible_step_posi = np.where(np.absolute(self.board) == self.nplayer)
        moves = []
        for ind in possible_step_posi[0]:
            if self.board[(self.board[ind]/self.nplayer + ind) % self.board_size] == 0:
                moves.extend(["%d,%d" % (ind, j) for j in possible_step_posi[0] if j != ind])
        return moves

    def make_move(self, move):
        move = list(map(int, move.split(',')))
        self.board[move[1]] = -self.board[move[1]]
        self.board[(self.board[move[0]]/self.nplayer + move[0]) % self.board_size] = self.board[move[0]]
        self.board[move[0]] = 0

    def show(self):
        print(self.board)

    def lose(self):
        return self.possible_moves() == []

    def scoring(self):
        return -100 if (self.possible_moves() == []) else 0

    def is_over(self):
        return self.lose()


if __name__ == "__main__":
    from easyAI import Human_Player, AI_Player, Negamax

    ai_algo = Negamax(11)
    game = SeptTurn([AI_Player(ai_algo), AI_Player(ai_algo)])
    game.play()
    print("player %d loses" % game.nplayer)

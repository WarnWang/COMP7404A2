#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: COMP7404A2
# File name: solveTicTacToe
# Date: 1/4/2016

"""
Support any number of board, and both first player and second player can be set as AI.
Default setting is player1 is AI, and there are 3 boards

Enjoy it!

Reference
    (1) Plambeck, Thane E., and Greg Whitehead. "The Secrets of Notakto: Winning at X-only Tic-Tac-Toe." arXiv preprint
    arXiv:1301.1672 (2013).

"""

# The following variables are used in evaluation board function
P_POSITION = ['a', 'bb', 'bc', 'cc']
Q = [1, 'a', 'b', 'ab', 'bb', 'abb', 'c', 'ac', 'bc', 'abc', 'cc', 'acc', 'bcc', 'abcc', 'd', 'ad', 'bd', 'abd']
EVALUATE_BOARD_DICT = {
    'a': ['X1234567X', '0X2X45678', '0X23456X8', 'XX2345X78', 'X1X3X5678', 'X1X3456X8', 'X123XX678', 'XX2XX5678',
          'XX2X4X678', 'XX2X4567X', 'XX23456XX', 'X1X345X7X', '0X2X4X6X8', 'XX23XXX78', 'XX234XXX8', 'XX234XX7X',
          'XX2X4X6XX'],
    'ab': ['XX23X5678', 'X1X345X78', '0X2XX5678', 'XX234X6X8', 'XX234X67X'],
    'ad': ['XX2345678'],
    'b': ['X1X345678', 'X123X5678', 'X1234X678', '0X23X5678', 'XX2X45678', '0X2X4X678', 'XX23XX678', 'XX23X5X78',
          'XX234XX78', 'XX2345XX8', 'XX2345X7X', 'X1X3X56X8', 'X123XX6X8', 'XX2X4X6X8', 'XX2X4X67X'],
    'c': ['012345678'],
    'cc': ['0123X5678'],
    'd': ['XX234X678', 'XX23456X8', 'XX234567X']
}


class GameBoard(object):
    """ Use to store the date of current game board """

    def __init__(self, board=None):
        if board is None:
            self.__board = [str(i) for i in range(9)]

        else:
            self.__board = board

    def __getitem__(self, item):
        return self.__board[item]

    def __setitem__(self, key, value):
        self.__board[key] = value

    def __len__(self):
        return len(self.__board)

    def __contains__(self, item):
        return item in self.__board

    def __reversed__(self):
        return reversed(self.__board)

    def __iter__(self):
        return self.__board.__iter__()

    def __repr__(self):
        return ''.join(self.__board)

    def __str__(self):
        board = "{}\n{}\n{}".format(' '.join(self.__board[:3]),
                                    ' '.join(self.__board[3:6]),
                                    ' '.join(self.__board[6:9]))
        return board

    def __eq__(self, other):
        """ Check whether two board are equal """
        str1 = {''.join(self)}
        if isinstance(other, str):
            str2 = other
        else:
            str2 = ''.join(other)
        str_list = self.__rotate_board()
        for board in str_list:
            str1.add(''.join(board))
        return str2 in str1

    def __hash__(self):
        return tuple(self.__board).__hash__()

    def copy(self):
        """ Get a copy of current board """
        new_board = self.__board[:]
        return GameBoard(new_board)

    def is_dead(self):
        """ Check whether current board can be played any more """
        possible_lines = ['012', '345', '678', '036', '147', '258', '048', '246']
        for i in possible_lines:
            for j in i:
                if j in self.__board:
                    break
            else:
                return True
        return False

    def is_valid_move(self, pos):
        """ Check whether current position can be set to X """
        return not self.is_dead() and pos in range(9) and self.__board[pos] != 'X'

    def evaluate_board(self):
        """ Get the evaluation of current board """
        if self.is_dead():
            return '1'

        for key in EVALUATE_BOARD_DICT:
            if self in EVALUATE_BOARD_DICT[key]:
                return key
        return '1'

    def get_valid_actions(self):
        """ Return the valid ceil that we can put chess on """
        if self.is_dead():
            return []

        action = self.__board[:]
        while 'X' in action:
            action.remove('X')

        return action

    def __rotate_board(self):
        """ In order to evaluate the board type, we need to get the reversed board type """
        board = self.__board
        board_180 = list(reversed(self.__board))
        board_90 = [board[6], board[3], board[0], board[7], board[4], board[1], board[8], board[5], board[2]]
        board_270 = list(reversed(board_90))
        for i in range(9):
            if board_90[i] != 'X':
                board_90[i] = str(i)
            if board_180[i] != 'X':
                board_180[i] = str(i)
            if board_270[i] != 'X':
                board_270[i] = str(i)

        # As symmetry board can also be regarded as same board
        def get_symmetry(temp):
            new_board = [temp[2], temp[1], temp[0], temp[5], temp[4], temp[3], temp[8], temp[7], temp[6]]
            for i in range(9):
                if new_board[i] != 'X':
                    new_board[i] = str(i)

            return new_board

        return (board_90, board_180, board_270, get_symmetry(board), get_symmetry(board_90), get_symmetry(board_180),
                get_symmetry(board_270))

    def try_action(self, pos):
        """
        Try to change pos to 'X' and return a new board
        :param pos: pos index, must be in [0, 8]
        :return: a new board with pos set to 'X'
        """
        if isinstance(pos, str):
            pos = int(pos)
        new_board = self.copy()
        new_board[pos] = 'X'
        return new_board


class TicTacToeGame(object):
    def __init__(self, board_num=3, game_state=None):
        """
        init game only support 3 boards currently
        """
        if game_state is None:
            self.board = []
            self.board_num = board_num
            for i in range(board_num):
                self.board.append(GameBoard())
            self.player_index = False
            self.player_name = None
        else:
            self.board = []
            self.board_num = game_state.board_num
            for board in game_state.board:
                self.board.append(board.copy())
            self.player_index = game_state.player_index
            self.player_name = game_state.player_name

    def __str__(self):
        """
        Use a string to represent current board
        :return: the board string
        """
        string_info = []
        for i in range(self.board_num):
            character = chr(ord('A') + i)
            string_info.append('{}:     '.format(character))
        string_info = ''.join(string_info)
        row1 = " ".join(self.board[0][:3])
        row2 = " ".join(self.board[0][3:6])
        row3 = " ".join(self.board[0][6:9])

        for i in range(1, self.board_num):
            row1 = "{}  {}".format(row1, " ".join(self.board[i][:3]))
            row2 = "{}  {}".format(row2, " ".join(self.board[i][3:6]))
            row3 = "{}  {}".format(row3, " ".join(self.board[i][6:9]))

        return "{}\n{}\n{}\n{}".format(string_info, row1, row2, row3)

    def is_valid_action(self, action_pos):
        """
        Check whether current move is valid move
        :param action_pos: the position that need to change to X
        :return: whether this action is valid or not
        """
        action_pos = action_pos.lower()
        if len(action_pos) != 2:
            return False
        board_index = ord(action_pos[0]) - ord('a')
        piece_index = action_pos[1]
        if board_index >= self.board_num or board_index < 0 or not piece_index.isdigit() or piece_index == '9':
            return False
        return self.board[board_index].is_valid_move(int(piece_index))

    def take_action(self, action):
        """
        Change board value based on the action input
        :param action: action pos
        :return: None
        """
        action = action.lower()
        if not self.is_valid_action(action):
            raise ValueError('Invalid action {}'.format(action))

        board_index = ord(action[0]) - ord('a')
        self.board[board_index][int(action[1])] = 'X'
        self.player_index = not self.player_index

    def is_finish(self):
        """ Check whether game is finished or not """
        for board in self.board:
            if not board.is_dead():
                return False
        return True

    def get_valid_actions(self):
        actions = []
        for i in range(self.board_num):
            board_index = chr(ord('a') + i)
            valid_actions = self.board[i].get_valid_actions()
            for j in valid_actions:
                actions.append("{}{}".format(board_index, j))

        return actions

    def play(self, player1_is_ai=True, player2_is_ai=False):
        """
        Play tic tac toe game
        :param player1_is_ai: Whether player1 is AI or not
        :param player2_is_ai: Whether player2 is AI or not
        """
        if player1_is_ai and player2_is_ai:
            players = [AIPlayer('AI1'), AIPlayer('AI2')]
        elif player2_is_ai:
            players = ['Your', AIPlayer()]
        elif player1_is_ai:
            players = [AIPlayer(), 'Your']
        else:
            players = ['Player1', 'Player2']

        # Main game code
        while not self.is_finish():
            player_index = int(self.player_index)
            player = players[player_index]
            print '{} move:'.format(player),

            # get player type
            if isinstance(player, AIPlayer):
                # action = player.get_next_action(self.board)
                action = player.get_action(self)
                print action.upper()
            else:
                action = raw_input()
                while not self.is_valid_action(action):
                    action = raw_input("Invalid action, please input again: ")
            self.take_action(action)
            print self

        player = players[int(self.player_index)]
        print "{} wins".format(player)


class AIPlayer(object):
    """
    AI Class, used to generate next action based on boards
    """

    def __init__(self, name='AI', depth=1):
        self.__name = name
        self.__depth = depth
        self.__ai_index = None

    def __str__(self):
        return self.__name

    def eval_action(self, game_state):
        """
        Eval current game board state
        :param game_state: current game state
        :return: the game score of current game board
        """
        if game_state.is_finish():
            if self.__ai_index == game_state.player_index:
                return int(self.__ai_index)
            else:
                return int(not self.__ai_index)

        valid_actions = game_state.get_valid_actions()
        total_value = 0
        max_value = int(not self.__ai_index)
        for action in valid_actions:
            new_game_state = TicTacToeGame(game_state=game_state)
            new_game_state.take_action(action)
            game_score = self.eval_action(new_game_state)
            if game_state.player_index == self.__ai_index:
                if isinstance(game_score, int) and bool(game_score) == self.__ai_index:
                    return int(game_score)
            total_value += game_score
            if abs(game_score - int(self.__ai_index)) < abs(max_value - int(self.__ai_index)):
                max_value = game_score

        if game_state.player_index == self.__ai_index:
            return max_value
        else:
            if total_value == 0 or total_value == len(valid_actions):
                return total_value / len(valid_actions)
            else:
                return float(total_value) / len(valid_actions)

    def get_action(self, game):
        """
        Except mac version of tictactoe game
        :param game: current game state, and TicTacToeGame class
        :return: valid actions
        """
        valid_actions = game.get_valid_actions()
        target = int(game.player_index)
        if self.__ai_index is None:
            self.__ai_index = game.player_index

        min_value = int(not self.__ai_index)
        opt_action = valid_actions[0]
        for action in valid_actions:
            new_game = TicTacToeGame(game_state=game)
            new_game.take_action(action)
            game_score = self.eval_action(new_game)
            if isinstance(game_score, int) and game_score == target:
                return action

            elif abs(game_score - target) < abs(min_value - target):
                min_value = game_score
                opt_action = action

        return opt_action

    def get_next_action(self, board, current_player=True, depth=0):
        """
        Use depth limit search to find the best action

        @:param board: current board state
        @:param current_player: whether AI is current player
        @:param depth: current searching depth, default is 0
        @:return: if AI is current player, return AI action else return the number of positive position that next
        player has
        """

        board_num = len(board)
        valid_action_list = [i.get_valid_actions() for i in board]
        state_list = [i.evaluate_board() for i in board]
        win_action = []
        min_win = None
        next_action = None

        # travel all possible actions to find the best option
        for i in range(board_num):
            board_index = chr(ord('a') + i)
            for action in valid_action_list[i]:
                new_board = board[i].try_action(action)
                new_state_list = state_list[:]
                new_state_list[i] = new_board.evaluate_board()
                current = merge_state(new_state_list)

                # if current action is in P_POSITION, which means current player must win
                if current in P_POSITION:
                    if current_player:
                        return '{}{}'.format(board_index, action)
                    else:
                        win_action.append('{}{}'.format(board_index, action))

                # else if find the action with the minimum actions number
                elif depth < self.__depth:
                    new_board_list = board[:]
                    new_state_list[i] = new_board
                    n_of_win_action = self.get_next_action(new_board_list, not current_player, depth + 1)
                    if min_win is None or n_of_win_action < min_win:
                        min_win = n_of_win_action
                        next_action = '{}{}'.format(board_index, action)

        return next_action if current_player else len(win_action)


def merge_state(state):
    """ Apply Q = < a, b, c, d | aa = 1, bbb = b, bbc = c, ccc = acc, bbd = d, cd = ad, dd = cc> to get current game
    state """
    if isinstance(state, str):
        pass
    elif isinstance(state, list):
        state = ''.join(state)
    else:
        raise ValueError("Invalid state: {}".format(state))

    # When state still has value and current state is not a goal state
    while len(state) != 0 and ''.join(state) not in Q:
        former_state = state

        # index 0 is count a, 1 is count b, 2 is count c, 3 is count d
        num_index = {'a': 0, 'b': 0, 'c': 0, 'd': 0, '1': 0}
        for i in state:
            num_index[i] += 1

        # Apply bbd = d, bbc = c, bbb = b
        while num_index['b'] > 1:
            if num_index['b'] > 2 or num_index['c'] > 0 or num_index['d'] > 0:
                num_index['b'] -= 2
            else:
                break

        # Apply dd = cc
        while num_index['d'] > 1:
            num_index['c'] += 2
            num_index['d'] -= 2

        # Apply ccc = acc
        while num_index['c'] > 2:
            num_index['c'] -= 1
            num_index['a'] += 1

        # Apply cd = ad
        while num_index['d'] > 0 and num_index['c'] > 0:
            num_index['c'] -= 1
            num_index['a'] += 1

        # Apply aa = 1
        while num_index['a'] > 1:
            num_index['a'] -= 2

        state = 'a' * num_index['a'] + 'b' * num_index['b'] + 'c' * num_index['c'] + 'd' * num_index['d']
        if former_state == state:
            break

    if len(state) == 0:
        return '1'
    else:
        return ''.join(state)


if __name__ == "__main__":
    test = TicTacToeGame(3)
    test.play(player1_is_ai=True, player2_is_ai=False)

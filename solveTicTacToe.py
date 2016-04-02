#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: COMP7404A2
# File name: solveTicTacToe
# Date: 1/4/2016


PLAYERS = [("Player1 move", "Player2 move"), ("AI", "Your move"), ("AI1", "AI2")]
P_POSITION = ['a', 'bb', 'bc', 'cc']
Q = [1, 'a', 'b', 'ab', 'bb', 'abb', 'c', 'ac', 'bc', 'abc', 'cc', 'acc', 'bcc', 'abcc', 'd', 'ad', 'bd', 'abd']
EVALUATE_BOARD_DICT = {'1': ['X12345678',
                             '0123X5678',
                             'XXX345678',
                             'X123X567X',
                             'X1234X6X8',
                             '0X23X56X8',
                             'XXXX45678',
                             'XXX3X5678',
                             'XXX345X78',
                             'XXX3456X8',
                             'XX23X56X8',
                             'XX23X567X',
                             'X1X3X5X78',
                             '0X2XXX678',
                             'XXXXX5678',
                             'XXXX4X678',
                             'XXXX45X78',
                             'XXXX456X8',
                             'XXXX4567X',
                             'XXX3X5X78',
                             'XXX3X56X8',
                             'XXX345XX8',
                             'XXX345X7X',
                             'XX2XXX678',
                             'XX2XX567X',
                             'XX23XX6X8',
                             'XX23XX67X',
                             'XX23X5XX8',
                             'XX23X5X7X',
                             'XX23X56XX',
                             'X1X3X5X7X',
                             '0X2XXX6X8',
                             'XXXXXX678',
                             'XXXXX5X78',
                             'XXXXX56X8',
                             'XXXXX567X',
                             'XXXX4XX78',
                             'XXXX4X6X8',
                             'XXXX45X7X',
                             'XXXX456XX',
                             'XXX3X5XX8',
                             'XXX3X5X7X',
                             'XXX345XXX',
                             'XX2XXX6X8',
                             'XX2XXX67X',
                             'XX23XXXX8',
                             'XX23XXX7X',
                             'XXXXXXX78',
                             'XXXXXX6X8',
                             'XXXXX5X7X',
                             'XXXXX56XX',
                             'XXXX4XXX8',
                             'XXXX4XX7X',
                             'XXX3X5XXX',
                             'XX2XXX6XX',
                             'XXXXXXXX8',
                             'XXXXXXX7X',
                             'XXXX4XXXX'],
                       'a': ['X1234567X',
                             '0X2X45678',
                             '0X23456X8',
                             'XX2345X78',
                             'X1X3X5678',
                             'X1X3456X8',
                             'X123XX678',
                             'XX2XX5678',
                             'XX2X4X678',
                             'XX2X4567X',
                             'XX23456XX',
                             'X1X345X7X',
                             '0X2X4X6X8',
                             'XX23XXX78',
                             'XX234XXX8',
                             'XX234XX7X',
                             'XX2X4X6XX'],
                       'ab': ['XX23X5678', 'X1X345X78', '0X2XX5678', 'XX234X6X8', 'XX234X67X'],
                       'ad': ['XX2345678'],
                       'b': ['X1X345678',
                             'X123X5678',
                             'X1234X678',
                             '0X23X5678',
                             'XX2X45678',
                             '0X2X4X678',
                             'XX23XX678',
                             'XX23X5X78',
                             'XX234XX78',
                             'XX2345XX8',
                             'XX2345X7X',
                             'X1X3X56X8',
                             'X123XX6X8',
                             'XX2X4X6X8',
                             'XX2X4X67X'],
                       'c': ['012345678'],
                       'cc': [],
                       'd': ['XX234X678', 'XX23456X8', 'XX234567X']}


class GameBoard(object):
    ''' Use to store the date of current game board '''

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
        str1 = {''.join(self)}
        if isinstance(other, str):
            str2 = other
        else:
            str2 = ''.join(other)
        str_list = self.rotate_board()
        for board in str_list:
            str1.add(''.join(board))
        return str2 in str1

    def __hash__(self):
        return tuple(self.__board).__hash__()

    def copy(self):
        new_board = self.__board[:]
        return GameBoard(new_board)

    def is_dead(self):
        ''' Check whether current board can be played any more '''
        possible_lines = ['012', '345', '678', '036', '147', '258', '048', '246']
        for i in possible_lines:
            for j in i:
                if j in self.__board:
                    break
            else:
                return True
        return False

    def is_valid_move(self, pos):
        ''' Check whether current position can be set to X '''
        return not self.is_dead() and pos in range(9) and self.__board[pos] != 'X'

    def evaluate_board(self):
        if self.is_dead():
            return 1

        new_board = self.__board[:]
        while 'X' in new_board:
            new_board.remove('X')

        number_sum = sum([int(i) for i in new_board])
        if len(new_board) == 9:
            return 'c'

        elif len(new_board) == 8:
            if '4' in new_board:
                return 1
            else:
                return 'cc'

        elif len(new_board) == 7:
            if '4' in new_board:
                pass
            else:
                return 'b'

    def rotate_board(self):
        ''' In order to evaluate the board type, we need to get the reversed board type '''
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

        def get_symmetry(temp):
            new_board = [temp[2], temp[1], temp[0], temp[5], temp[4], temp[3], temp[8], temp[7], temp[6]]
            for i in range(9):
                if new_board[i] != 'X':
                    new_board[i] = str(i)

            return new_board

        return (board_90, board_180, board_270, get_symmetry(board), get_symmetry(board_90), get_symmetry(board_180),
                get_symmetry(board_270))


class TicTacToeGame(object):
    def __init__(self, board_num=3):
        '''
        init game only support 3 boards currently
        '''
        self.board = []
        self.board_num = board_num
        for i in range(board_num):
            self.board.append(GameBoard())
        self.player_index = False
        self.player_name = None

    def __str__(self):
        '''
        Use a string to represent current board
        :return: the board string
        '''
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
        '''
        Check whether current move is valid move
        :param action_pos: the position that need to change to X
        :return: whether this action is valid or not
        '''
        action_pos = action_pos.lower()
        if len(action_pos) != 2:
            return False
        board_index = ord(action_pos[0]) - ord('a')
        piece_index = action_pos[1]
        if board_index >= self.board_num or board_index < 0 or not piece_index.isdigit() or piece_index == '9':
            return False
        return self.board[board_index].is_valid_move(int(piece_index))

    def take_action(self, position):
        position = position.lower()
        if not self.is_valid_action(position):
            raise ValueError('Invalid action {}'.format(position))

        board_index = ord(position[0]) - ord('a')
        self.board[board_index][int(position[1])] = 'X'

    def is_finish(self):
        ''' Check whether game is finished or not '''
        for board in self.board:
            if not board.is_dead():
                return False
        return True

    def play(self, ai_num=0):
        '''
        Play tic tac toe game
        :param ai_num: the number of AI players, if this number greater than 2, regard as 2
        '''
        if ai_num > 2:
            ai_num = 2

        self.player_name = PLAYERS[ai_num]
        while not self.is_finish():
            player_name = self.player_name[int(self.player_index)]
            print '{}:'.format(self.player_name[int(self.player_index)]),
            if 'AI' in player_name:
                pass
            else:
                action = raw_input()
                while not self.is_valid_action(action):
                    action = raw_input("Invalid action, please input again: ")
            self.take_action(action)
            print self

            self.player_index = not self.player_index

        player_name = self.player_name[int(self.player_index)]
        print "{} wins".format(player_name.split(' ')[0])


class AIPlayer(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    test = TicTacToeGame(1)
    test.play()
    # test_game_board()
    # get_all_board()

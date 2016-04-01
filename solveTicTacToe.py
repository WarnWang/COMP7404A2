#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: COMP7404A2
# File name: solveTicTacToe
# Date: 1/4/2016


PLAYERS = [("Player1 move", "Player2 move"), ("AI", "Your move"), ("AI1", "AI2")]


class ticTacToeGame(object):
    def __init__(self, board_num=3):
        '''
        init game only support 3 boards currently
        '''
        self.board = []
        self.board_num = board_num
        for i in range(board_num):
            self.board.append([str(i) for i in range(9)])
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
        if board_index > self.board_num or board_index < 0 or not piece_index.isdigit() or piece_index == '9':
            return False
        if self.__is_finish(self.board[board_index]) or self.board[board_index][int(piece_index)] == 'X':
            return False
        return True

    def take_action(self, position):
        position = position.lower()
        if not self.is_valid_action(position):
            raise ValueError('Invalid action {}'.format(position))

        board_index = ord(position[0]) - ord('a')
        self.board[board_index][int(position[1])] = 'X'

    def __is_finish(self, board=None):
        '''
        internal function, check whether current board can add more piece or not
        :param board: board index, possible values is 'a', 'b' or 'c'
        :return: boolean, true or false
        '''
        if board is None:
            return True
        if board[4] == 'X':
            pass
        possible_lines = ['012', '345', '678', '036', '147', '258', '048', '246']
        for i in possible_lines:
            for j in i:
                if j in board:
                    break
            else:
                return True
        return False

    def is_finish(self):
        ''' Check whether game is finished or not '''
        for board in self.board:
            if not self.__is_finish(board):
                return False
        return True

    def play(self, AI_num=0):
        '''
        Play tic tac toe game
        :param AI_num: the number of AI players, if this number greater than 2, regard as 2
        :return: None
        '''
        if AI_num > 2:
            AI_num = 2

        self.player_name = PLAYERS[AI_num]
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


if __name__ == "__main__":
    test = ticTacToeGame(2)
    test.play()

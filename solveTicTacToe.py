#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: COMP7404A2
# File name: solveTicTacToe
# Date: 1/4/2016


PLAYERS = ("AI", "Your move")


class ticTacToeGame(object):
    def __init__(self):
        self.board_a = [str(i) for i in range(9)]
        self.board_b = [str(i) for i in range(9)]
        self.board_c = [str(i) for i in range(9)]
        self.board = {
            'a': self.board_a,
            'b': self.board_b,
            'c': self.board_c
        }
        self.player_index = False

    def __str__(self):
        string_info = "A:     B:     C:"
        row1 = " ".join(self.board_a[:3])
        row2 = " ".join(self.board_a[3:6])
        row3 = " ".join(self.board_a[6:9])

        row1 = "{}  {}  {}".format(row1, " ".join(self.board_b[:3]), " ".join(self.board_c[:3]))
        row2 = "{}  {}  {}".format(row2, " ".join(self.board_b[3:6]), " ".join(self.board_c[3:6]))
        row3 = "{}  {}  {}".format(row3, " ".join(self.board_b[6:9]), " ".join(self.board_c[6:9]))

        return "{}\n{}\n{}\n{}".format(string_info, row1, row2, row3)

    def take_action(self, position):
        position = position.lower()
        if position[0] not in 'abc' or len(position) != 2 or not position[1].isdigit() or position[1] == '9':
            raise ValueError('Invalid action {}'.format(position))
        if self.board[position[0]][int(position[1])] != 'X':
            self.board[position[0]][int(position[1])] = 'X'

    def is_finish(self, board='a'):
        pass


if __name__ == "__main__":
    test = ticTacToeGame()
    test.take_action('B0')
    test.take_action('A1')
    print test

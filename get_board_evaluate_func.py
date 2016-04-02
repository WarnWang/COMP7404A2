#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: COMP7404A2
# File name: get_board_evaluate_func
# Author: Mark Wang
# Date: 2/4/2016

from solveTicTacToe import GameBoard


def get_all_board():
    board_dict = {'1': ['X12345678',
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
    board = GameBoard()
    for variable_num in range(6, 9):
        variable_list = generate_variable_list(variable_num)
        for change_variable in variable_list:
            temp = board.copy()
            for i in change_variable:
                temp[i] = 'X'
            for key in board_dict:
                if temp in board_dict[key]:
                    break
            else:
                print temp
                key = raw_input("Which dict should this board put: ")
                board_dict[key].append(temp.__repr__())

    import pprint
    pprint.pprint(board_dict, width=120)


def generate_variable_list(num, start_index=0):
    num_list = []
    if num == 1:
        for i in range(start_index, 9):
            num_list.append([i])
        return num_list

    for i in range(start_index, 10 - num):
        shorter_list = generate_variable_list(num - 1, i + 1)
        for j in shorter_list:
            temp = [i]
            temp.extend(j)
            num_list.append(temp)

    return num_list


def test_game_board():
    board = GameBoard()
    board[0] = 'X'
    board[1] = 'X'
    another_board = '01X34X678'
    print board
    print another_board
    print board == another_board
    b = [board]
    print another_board in b

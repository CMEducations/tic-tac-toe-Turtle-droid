from math import inf as infinity
from random import choice
import platform
from os import system

"""
Tic Tac Toe MinMax Edition
Using Python
"""


def Evaluate(CurrentBoard):
    """
    Function to heuristicly evaluate the CurrentBoard.
    :param CurrentBoard: the state of the current Board
    :return: +10 if the AbominableIntelligence is the winner; -10 if the Human is the winner; 0 draw
    """
    if DetermineWinner(CurrentBoard, AbominableIntelligence):
        Score = +10
    elif DetermineWinner(CurrentBoard, Human):
        Score = -10
    else:
        Score = 0

    return Score


def DetermineWinner(CurrentBoard, CurrentPlayer):
    """
    This function tests if a specific CurrentPlayer DetermineWinner. Possibilities:
    * Three Rows    [X X X] or [O O O]
    * Three cols    [X X X] or [O O O]
    * Two diagonals [X X X] or [O O O]
    :param CurrentBoard: the state of the current Board
    :param CurrentPlayer: a Human or a AbominableIntelligence
    :return: True if the CurrentPlayer wins the game
    """
    win_CurrentBoard = [
        [CurrentBoard[0][0], CurrentBoard[0][1], CurrentBoard[0][2]],
        [CurrentBoard[1][0], CurrentBoard[1][1], CurrentBoard[1][2]],
        [CurrentBoard[2][0], CurrentBoard[2][1], CurrentBoard[2][2]],
        [CurrentBoard[0][0], CurrentBoard[1][0], CurrentBoard[2][0]],
        [CurrentBoard[0][1], CurrentBoard[1][1], CurrentBoard[2][1]],
        [CurrentBoard[0][2], CurrentBoard[1][2], CurrentBoard[2][2]],
        [CurrentBoard[0][0], CurrentBoard[1][1], CurrentBoard[2][2]],
        [CurrentBoard[2][0], CurrentBoard[1][1], CurrentBoard[0][2]],
    ]
    if [CurrentPlayer, CurrentPlayer, CurrentPlayer] in win_CurrentBoard:
        return True
    else:
        return False


def GameOver(CurrentBoard):
    """
    This function test if the Human or AbominableIntelligence Wins
    :param CurrentBoard: the board of the on going game
    :return: True if the Human or AbominableIntelligence Wins
    """
    return DetermineWinner(CurrentBoard, Human) or DetermineWinner(CurrentBoard, AbominableIntelligence)


def EmptyCells(CurrentBoard):
    """
    Each empty Cell will be added into Cells' list
    :param CurrentBoard: the board of the on going game
    :return: a list of empty Cells
    """
    Cells = []

    for x, Row in enumerate(CurrentBoard):
        for y, Cell in enumerate(Row):
            if Cell == 0:
                Cells.append([x, y])

    return Cells


def ValidMove(x, y):
    """
    A Move is valid if the chosen Cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the Board[x][y] is empty
    """
    if [x, y] in EmptyCells(Board):
        return True
    else:
        return False


def MakeMove(x, y, CurrentPlayer):
    """
    Set the Move on Board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param CurrentPlayer: the current player
    """
    if ValidMove(x, y):
        Board[x][y] = CurrentPlayer
        return True
    else:
        return False


def MinMax(CurrentBoard, Depth, CurrentPlayer):
    """
    AI function that determines the Best Move
    :param CurrentBoard: current state of the Board
    :param Depth: node index in the tree (0 <= Depth <= 9),
    but never nine in this case (see iaturn() function)
    :param CurrentPlayer: an Human or a AbominableIntelligence
    :return: a list with [the Best Row, Best col, Best Score]
    """
    if CurrentPlayer == AbominableIntelligence:
        Best = [-1, -1, -infinity]
    else:
        Best = [-1, -1, +infinity]

    if Depth == 0 or GameOver(CurrentBoard):
        Score = Evaluate(CurrentBoard)
        return [-1, -1, Score]

    for Cell in EmptyCells(CurrentBoard):
        x, y = Cell[0], Cell[1]
        CurrentBoard[x][y] = CurrentPlayer
        Score = MinMax(CurrentBoard, Depth - 1, -CurrentPlayer)
        CurrentBoard[x][y] = 0
        Score[0], Score[1] = x, y

        if CurrentPlayer == AbominableIntelligence:
            if Score[2] > Best[2]:
                Best = Score  # max value
        else:
            if Score[2] < Best[2]:
                Best = Score  # min value

    return Best


def ClearConsole():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def RenderBoard(CurrentBoard, AISymbol, HumanSymbol):
    """
    Print the Board on console
    :param CurrentBoard: current state of the Board
    """
    Chars = {
        -1: HumanSymbol,
        +1: AISymbol,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for Row in CurrentBoard:
        for Cell in Row:
            Symbol = Chars[Cell]
            print(f'| {Symbol} |', end='')
        print('\n' + str_line)


def AITurn(AISymbol, HumanSymbol):
    """
    It calls the MinMax function if the Depth < 9,
    else it choices a random coordinate.
    :param AISymbol: AbominableIntelligence's choice X or O
    :param HumanSymbol: Human's choice X or O
    :return:
    """
    Depth = len(EmptyCells(Board))
    if Depth == 0 or GameOver(Board):
        return

    ClearConsole()
    print(f'AbominableIntelligence turn [{AISymbol}]')
    RenderBoard(Board, AISymbol, HumanSymbol)

    if Depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        Move = MinMax(Board, Depth, AbominableIntelligence)
        x, y = Move[0], Move[1]

    MakeMove(x, y, AbominableIntelligence)


def HumanTurn(AISymbol, HumanSymbol):
    """
    The Human plays choosing a valid Move.
    :param AISymbol: AbominableIntelligence's choice X or O
    :param HumanSymbol: Human's choice X or O
    :return:
    """
    Depth = len(EmptyCells(Board))
    if Depth == 0 or GameOver(Board):
        return

    # Dictionary of valid Moves
    Move = -1
    Moves = {
        7: [0, 0], 8: [0, 1], 9: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        1: [2, 0], 2: [2, 1], 3: [2, 2],
    }

    ClearConsole()
    print(f'Human turn [{HumanSymbol}]')
    RenderBoard(Board, AISymbol, HumanSymbol)

    while Move < 1 or Move > 9:
        try:
            Move = int(input('Use numpad (1..9): '))
            coord = Moves[Move]
            can_Move = MakeMove(coord[0], coord[1], Human)

            if not can_Move:
                print('Bad Move')
                Move = -1
        except (EOFError, KeyBoardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def PlayAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    PlayAgain = ''
    while PlayAgain != 'Y' and PlayAgain != 'N' and PlayAgain != 'YES' and PlayAgain != 'NO':
        try:
            PlayAgain = input('Do you want to play again?[y/n]: ').upper()
        except (EOFError, KeyBoardInterrupt):
            print('Catastrophic System Failure')
            exit()
        except (KeyError, ValueError):
            print('Please input Y or N only!')
    return PlayAgain.startswith('Y')


def SetupBoard():
    # Reset board
    global Board
    Board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]


def StartGame():
    """
    Start a game function that calls all functions
    """
    ClearConsole()
    HumanSymbol = ''  # X or O
    AISymbol = ''  # X or O
    FirstPlayer = ''  # if Human is the FirstPlayer

    # Human chooses X or O to play
    while HumanSymbol != 'O' and HumanSymbol != 'X':
        try:
            print('')
            HumanSymbol = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyBoardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Please input X or O only!')

    # Setting AbominableIntelligence's choice
    if HumanSymbol == 'X':
        AISymbol = 'O'
    else:
        AISymbol = 'X'

    # Human may starts FirstPlayer
    ClearConsole()
    while FirstPlayer != 'Y' and FirstPlayer != 'N' and FirstPlayer != 'YES' and FirstPlayer != 'NO':
        try:
            FirstPlayer = input('FirstPlayer to start?[y/n]: ').upper()
        except (EOFError, KeyBoardInterrupt):
            print('Catastrophic System Failure')
            exit()
        except (KeyError, ValueError):
            print('Please inut Y or N only!')

    # Main loop of this game
    while len(EmptyCells(Board)) > 0 and not GameOver(Board):
        if FirstPlayer == 'N' or FirstPlayer == 'NO':
            AITurn(AISymbol, HumanSymbol)
            FirstPlayer = ''

        HumanTurn(AISymbol, HumanSymbol)
        AITurn(AISymbol, HumanSymbol)

    # Game over message
    if DetermineWinner(Board, Human):
        ClearConsole()
        print(f'Human turn [{HumanSymbol}]')
        RenderBoard(Board, AISymbol, HumanSymbol)
        print('WINNER!')
    elif DetermineWinner(Board, AbominableIntelligence):
        ClearConsole()
        print(f'AbominableIntelligence turn [{AISymbol}]')
        RenderBoard(Board, AISymbol, HumanSymbol)
        print('LOSER!')
    else:
        ClearConsole()
        RenderBoard(Board, AISymbol, HumanSymbol)
        print('DRAW!')

    if PlayAgain():
        ClearConsole()
        SetupBoard()
        StartGame()
    else:
        exit()


Human = -1
AbominableIntelligence = +1
Board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

StartGame()

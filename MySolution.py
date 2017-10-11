def negamaxIDS(game, maxDepth):
    for depth in range(maxDepth):
        score, move = negamax(game, depth)
        if move != None:
            break

    if move is None:
        # if (move is None or abs(score) == abs(float("inf"))):
        return None, None
    else:
        return score, move


def negamaxIDSab(game, maxDepth):
    for depth in range(maxDepth):
        # score, move = negamaxAB(game, depth, float('inf'), -float('inf'))
        score, move = negamaxAB(game, depth, -float('inf'), float('inf'))
        if move != None:
            break

    if move is None:
        # if (move is None or abs(score) == abs(float("inf"))):
        return None, None
    else:
        return score, move

def negamax(game, depthLeft):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None  # call to negamax knows the move
    # Find best move and its value from current state
    bestValue, bestMove = None, None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        # Use depth-first search to find eventual utility value and back it up.
        #  Negate it because it will come back in context of next player
        value, _ = negamax(game, depthLeft - 1)
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if bestValue is None or value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue, bestMove = value, move
    return bestValue, bestMove

def negamaxAB(game, depthLeft, alpha, beta):
    # If at terminal state or depth limit, return utility value and move None
    if game.isOver() or depthLeft == 0:
        return game.getUtility(), None
    # Find best move and its value from current state
    bestValue = -float('inf')
    bestMove = None
    for move in game.getMoves():
        # Apply a move to current state
        game.makeMove(move)
        # Use depth-first search to find eventual utility value and back it up.
        #  Negate it because it will come back in context of next player
        value, _ = negamaxAB(game, depthLeft-1, -beta, -alpha)
        # Remove the move from current state, to prepare for trying a different move
        game.unmakeMove(move)
        if value is None:
            continue
        value = - value
        if value > bestValue:
            # Value for this move is better than moves tried so far from this state.
            bestValue = value
            bestMove = move
            if(bestValue >= beta):
                return bestValue, bestMove

        alpha = max(bestValue, alpha)
        if (alpha >= beta):
            return alpha, move

    return bestValue, bestMove


# def negamaxAB(game, depthLeft, alpha, beta):
#     # If at terminal state or depth limit, return utility value and move None
#     if game.isOver() or depthLeft == 0:
#         return game.getUtility(), None
#     # Find best move and its value from current state
#     bestValue = -float('infinity')
#     bestMove = None
#     for move in game.getMoves():
#         # Apply a move to current state
#         game.makeMove(move)
#         # Use depth-first search to find eventual utility value and back it up.
#         #  Negate it because it will come back in context of next player
#         value, _ = negamaxAB(game, depthLeft - 1, -beta, -alpha)
#         if value is None:
#             continue
#         value = - value
#         # Remove the move from current state, to prepare for trying a different move
#         game.unmakeMove(move)
#         if value > bestValue:
#             # Value for this move is better than moves tried so far from this state.
#             bestValue = value
#             bestMove = move
#         if value > alpha:
#             alpha = value
#         if (alpha >= beta):
#             return alpha, move
#     return bestValue, bestMove


class TTT(object):
    def __init__(self):
        self.board = [' '] * 9
        self.player = 'X'
        if False:
            self.board = ['X', 'X', ' ', 'X', 'O', 'O', ' ', ' ', ' ']
            self.player = 'O'
        self.playerLookAHead = self.player
        self.movesExplored = 0

    def locations(self, c):
        return [i for i, mark in enumerate(self.board) if mark == c]

    def getMoves(self):
        moves = self.locations(' ')
        return moves

    def getUtility(self):
        whereX = self.locations('X')
        whereO = self.locations('O')
        wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]]
        isXWon = any([all([wi in whereX for wi in w]) for w in wins])
        isOWon = any([all([wi in whereO for wi in w]) for w in wins])
        if isXWon:
            return 1 if self.playerLookAHead is 'X' else -1
        elif isOWon:
            return 1 if self.playerLookAHead is 'O' else -1
        elif ' ' not in self.board:
            return 0
        else:
            return None  ########################################################## CHANGED FROM -0.1

    def isOver(self):
        return self.getUtility() is not None

    def makeMove(self, move):
        self.board[move] = self.playerLookAHead
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'
        self.movesExplored += 1

    def changePlayer(self):
        self.player = 'X' if self.player == 'O' else 'O'
        self.playerLookAHead = self.player

    def unmakeMove(self, move):
        self.board[move] = ' '
        self.playerLookAHead = 'X' if self.playerLookAHead == 'O' else 'O'

    def getMovesExplored(self):
        return self.movesExplored

    def getXMovesMade(self):
        return self.board.count('X')

    def getMovesMade(self):
        return 9 - self.board.count(' ')

    def __str__(self):
        s = '{}|{}|{}\n-----\n{}|{}|{}\n-----\n{}|{}|{}'.format(*self.board)
        return s


def ebf(nNodes, depth, precision=0.01):
    if nNodes == 0:
        return 0

    def ebfRec(low, high):
        mid = (low + high) * 0.5
        if mid == 1:
            estimate = 1 + depth
        else:
            estimate = (1 - mid ** (depth + 1)) / (1 - mid)
        if abs(estimate - nNodes) < precision:
            return mid
        if estimate > nNodes:
            return ebfRec(low, mid)
        else:
            return ebfRec(mid, high)

    return ebfRec(1, nNodes)


def opponent(board):
    return board.index(' ')


def playGame(game, opponent, depthLimit, method):
    print(game)
    while not game.isOver():
        if method == "negamax":
            score, move = negamax(game, depthLimit)
        elif method == "negamaxIDS":
            score, move = negamaxIDS(game, depthLimit)
        elif method == "negamaxIDSab":
            score, move = negamaxIDSab(game, depthLimit)
        else:
            break

        if move == None:
            print('move is None. Stopping.')
            break
        game.makeMove(move)
        print('Player', game.player, 'to', move, 'for score', score)
        print(game)
        if not game.isOver():
            game.changePlayer()
            opponentMove = opponent(game.board)
            game.makeMove(opponentMove)
            print('Player', game.player, 'to', opponentMove)
            print(game)
            game.changePlayer()

def printResults(game, algorithm):
    ebfCalculated = "{0:.2f}".format(ebf(game.getMovesExplored(), game.getMovesMade()))
    line = "{} made {} moves. {} moves explored for ebf({}, {}) of {}".format(algorithm, game.getXMovesMade(), game.getMovesExplored(), game.getMovesExplored(), game.getMovesMade(),ebfCalculated)
    print(line)


def playGames(opponent, depthLimit):
    game = TTT()
    algorithm = "negamax"
    playGame(game, opponent, depthLimit, algorithm)
    printResults(game, algorithm)
    game = TTT()
    algorithm = "negamaxIDS"
    playGame(game, opponent, depthLimit, algorithm)
    printResults(game, algorithm)
    game = TTT()
    algorithm = "negamaxIDSab"
    playGame(game, opponent, depthLimit, algorithm)
    printResults(game, algorithm)



playGames(opponent, 20)

# game = TTT()
# playGame(game, opponent, 20, "negamax")
# print("Moves Explored: ", game.getMovesExplored())
# print("EBS: ", ebf(game.getMovesExplored(), game.getMovesMade()))
# game = TTT()
# playGame(game, opponent, 20, "negamaxIDS")
# print("Moves Explored: ", game.getMovesExplored())
# print("EBS: ", ebf(game.getMovesExplored(), game.getMovesMade()))
# game = TTT()
# playGame(game, opponent, 20, "negamaxIDSab")
# print("Moves Explored: ", game.getMovesExplored())
# print("EBS: ", ebf(game.getMovesExplored(), game.getMovesMade()))

import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board, symbol):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    print("*****inside minimax")
    def __init__(self, symbol, depth):
        super(MinimaxPlayer, self).__init__(symbol)
        self.d = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
#        print('***** minimax')
        #legalMoves = game_rules.getLegalMoves(board, self.symbol)
        #if len(legalMoves) > 0:
            #print('**check', legalMoves[0])
#        print('**original board: ', board)
#        print('**original symbol: ', self.symbol)

        def minimax_recur(depth, board, turn, currsymbol):
#            print('**minimax_recur board: ', board)
#            print('**current player: ', currsymbol)
            legalMoves = game_rules.getLegalMoves(board, currsymbol) #self.symbol)
#            print('**all legal moves: ', legalMoves)

            if len(legalMoves) == 0 or depth == 0:
#                print('**case1')
#                print('**heuristic: ', self.h1(board, currsymbol))
                return None, self.h1(board, currsymbol)
            
            val = (POS_INF, NEG_INF)[turn]
#            print('**val = ', val)
            move = None

            tmpmove = (None, None)

            for eachmove in legalMoves:
#                print('**now move: ', eachmove)

                if tmpmove[0] != None:
                    board = self.originalboard(board, tmpmove[0], tmpmove[1], currsymbol)

#                print('board: ', board)

                tmpmove = (eachmove[0], eachmove[len(eachmove) - 1]) #start -> end
#                print('**tmpmove: ', tmpmove)

                board = game_rules.makeMove(board, eachmove)
#                print('**nowboard: ', board)
                succmove, succval = minimax_recur(depth-1, board, not turn, self.changeturn(currsymbol))
#                print('*****now val:', succval)
               
#                print('current move: ', eachmove)
#                print('bestval: ', val)
#                print('bestmove: ', move)
                a, b = (((move, val), (eachmove, succval))[succval < val], ((move, val), (eachmove, succval))[succval > val])[turn]
                move = a
                val = b
#                print('**bestmove: ', move)
#                print('**bestval: ', val)

            board = self.originalboard(board, tmpmove[0], tmpmove[1], currsymbol)

#            print('then return bestmove: ', move)
#            print('then return bestval: ', val)
            return move, val

        return minimax_recur(self.d, board, True, self.symbol)[0]


    
    def originalboard(self, board, start, end, currsymbol):
        if start[0] == end[0]:
            dirct = (0, int((end[1] - start[1]) / abs(end[1] - start[1])))
            #print('dctn: ', dirct)
        else:
            dirct = (int((end[0] - start[0]) / abs(end[0] - start[0])), 0)
            #print('dctn: ', dirct)
        #print('check start: ', start)
        #print('check end: ', end)
        capture = (start[0] + dirct[0], start[1] + dirct[1])
        #print('check NEXT: ', NEXT)
        board[start[0]][start[1]] = currsymbol
        board[end[0]][end[1]] = ' '

        while (capture[0]-end[0])*dirct[0] < 0 or (capture[1]-end[1])*dirct[1] < 0:
            board[capture[0]][capture[1]] = self.changeturn(currsymbol)
            capture = (capture[0] + dirct[0]*2, capture[1] + dirct[1]*2)

        return board

    



        #return legalMoves[0]
    #else: return None

    def changeturn(self, s):
        if s == 'x':
            return 'o'
        else:
            return 'x'



# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth):
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.d = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
#        print('***** alphabeta')
        #legalMoves = game_rules.getLegalMoves(board, self.symbol)
        #if len(legalMoves) > 0: return legalMoves[0]
        #else: return None
#        print('original board: ', board)

        def alphabeta_recur(depth, board, turn, currsymbol, alpha, beta):
#            print('** now board: ', board)
#            print('** now player: ', currsymbol)
            legalMoves = game_rules.getLegalMoves(board, currsymbol)
#            print('all legal moves: ', legalMoves)

            if len(legalMoves) == 0 or depth == 0:
#                print('case1')
#                print('h1: ', self.h1(board, currsymbol))
                # only return heuristic
                # self.printCurrentInfo(depth, self.heuristic(board, self), None)
                return None, self.h1(board, currsymbol)

#            print('turn: ', turn)
            val = (POS_INF, NEG_INF)[turn]
#            print('val: ', val)
            
            move = None

            tmpmove = (None, None)

            # judge every nodes possible, select the biggest/smallest one
            for eachmove in legalMoves:
#                print('now eachmove: ', eachmove)

                if tmpmove[0] != None:
                    board = self.originalboard(board, tmpmove[0], tmpmove[1], currsymbol)

                tmpmove = (eachmove[0], eachmove[len(eachmove) - 1])
#                print('new move: ', tmpmove)

                board = game_rules.makeMove(board, eachmove)
#                print('board: ', board)
                
                succmove, succval = alphabeta_recur(depth - 1, board, not turn, self.changeturn(currsymbol), alpha, beta)
#                print('now succval: ', succval)

#                print('check a,b: ')
#                print('succval: ', succval)
#                print('val: ', val)
#                print('eachmove: ', eachmove)
#                print('move: ', move)
#                print('turn: ', turn)
                a, b = (((move, val), (eachmove, succval))[succval < val], ((move, val), (eachmove, succval))[succval > val])[turn]
                move = a
                val = b

#                print('move: ', move)
#                print('val: ', val)


                if turn:
                    alpha = (alpha, val)[alpha <= val]
#                    print('alpha: ', alpha)
                else:
                    beta = (beta, val)[beta >= val]
#                    print('beta: ', beta)
                if beta <= alpha:
#                    print('beta < alpha, break', beta, alpha)
                    break

            board = self.originalboard(board, tmpmove[0], tmpmove[1], currsymbol)

#            print('then return move: ', move)
#            print('then return bestval: ', val)
            return move, val

        return alphabeta_recur(self.d, board, True, self.symbol, NEG_INF, POS_INF)[0]



    def originalboard(self, board, start, end, currsymbol):
        if start[0] == end[0]:
            dirct = (0, int((end[1] - start[1]) / abs(end[1] - start[1])))
            #print('dctn: ', dirct)
        else:
            dirct = (int((end[0] - start[0]) / abs(end[0] - start[0])), 0)
            #print('dctn: ', dirct)
        #print('check start: ', start)
        #print('check end: ', end)
        capture = (start[0] + dirct[0], start[1] + dirct[1])
        #print('check NEXT: ', NEXT)
        board[start[0]][start[1]] = currsymbol
        board[end[0]][end[1]] = ' '

        while (capture[0]-end[0])*dirct[0] < 0 or (capture[1]-end[1])*dirct[1] < 0:
            board[capture[0]][capture[1]] = self.changeturn(currsymbol)
            capture = (capture[0] + dirct[0]*2, capture[1] + dirct[1]*2)

        return board
    
    def changeturn(self, s):
        if s == 'x':
            return 'o'
        else:
            return 'x'



class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)





import chess
import random as r

def make_a_good_move(board):
    '''
    makes a move that is suggested by minimax function
    :param board: current chess board cotaining pieces and legal moves
    '''
    if not board.is_checkmate() and not board.is_stalemate():

        m= minimax(board,True)


        board.push(m[1])

def minimax(board,abp):
    '''
    This is a simple wrapper of the minimax functions.
    this function exists because the minimax functions are recursive
    and therefore have multiple arguments which are the same for every initial call
    :param board: current chess board
    :param abp: Bool of whether to use alpha beta pruning
    :return: returns minimax call
    '''

    if abp:
        return minimax2(board, 4, -100000, 100000)
    else:
        return minimax_without_abp(board,3)

def minimax2(board, depth, alpha, beta):
    '''
    This is a more complex version of the minimax_without_abp function.
    this function does use alpha beta pruning to save computing power
    and be able to search more deeply into the moves tree
    :param board: current chess board
    :param depth: how much deeper the algorithm has to go into the moves tree
    :param alpha: best choice for maximizing player
    :param beta: best choice for minimizing player
    :return: returns evaluation together with best move if there have not yet been any recursive calls
    '''

    # handling end of tree (when depth is 0)
    if depth ==0:
        return evaluate(board),0
    # handling game endings
    elif board.is_checkmate():
        return depth +2 *evaluate(board),0
    elif board.outcome() != None:
        return 0,0

    #getting all legal moves for this branch
    legal = list(board.legal_moves)

    bestmove = legal[r.randint(0,len(legal)-1)]
    bestmove_for_black =legal[r.randint(0,len(legal)-1)]


    if board.turn == chess.WHITE:
        #max
        maxeval = -100000

        for move in legal:

            board.push(move)

            currenteval = minimax2(board, depth - 1, alpha, beta)[0]

            board.pop()

            if currenteval > maxeval:
                bestmove =move

            maxeval = max(currenteval,maxeval)

            #below the computer looks if the maximizing player has a new best move
            # to play at the current depth in the tree of moves
            alpha = max(currenteval,alpha)

            #right here the computer looks at whether the minimizing player had a better move earlier on
            # and prunes if this is the case
            if alpha >= beta:
                break

        return maxeval,bestmove

    else:
        #min
        mineval = 100000
        for move in legal:
            #code below goes through all moves in the moves tree
            board.push(move)
            currenteval = minimax2(board, depth - 1, alpha, beta)[0]
            board.pop()


            if currenteval < mineval:
                bestmove_for_black =move
            mineval = min(currenteval,mineval)

            #below the computer looks if the minimizing player has a new best move
            # to play at the current depth in the tree of moves
            beta = min(currenteval,beta)

            #right here the computer looks at whether the maximizing player had a better move earlier on
            # and prunes if this is the case
            if alpha >= beta:
                break

        return mineval,bestmove_for_black


def minimax_without_abp(board, depth):
    '''
    This is a plain recursive minimax algorithm
    :param board: current chess board
    :param depth: how much further the algorithm has to look into the moves tree
    :return: returns evaluation and best move or a recursive call
    '''
    # handling end of tree (when depth is 0)
    if depth ==0:
        return evaluate(board),0
    # handling game endings
    elif board.is_checkmate():
        depth +1 *evaluate(board),0
    elif board.outcome() != None:
        return 0,0

    bestmove =0
    bestmove_for_black =0

    #getting all legal moves for this branch
    legal = list(board.legal_moves)

    if board.turn == chess.WHITE:
        #max
        maxeval = -100000

        #code below goes through all moves in the moves tree
        for move in legal:
            if bestmove == 0:
                bestmove = move

            board.push(move)

            currenteval = minimax_without_abp(board, depth - 1)[0]
            maxeval = max(currenteval,maxeval)

            board.pop()


            if currenteval == maxeval:
                bestmove =move

        return maxeval,bestmove

    else:
        #min
        mineval = 100000

        #code below goes through all moves in the moves tree
        for move in legal:

            board.push(move)

            currenteval = minimax_without_abp(board, depth - 1)[0]
            mineval = min(currenteval,mineval)

            board.pop()

            if currenteval == mineval:
                bestmove_for_black =move

        return mineval,bestmove_for_black


def evaluate(board):
    start =0
    if not board.is_checkmate():
        for piece in board.board_fen():
            if piece not in "123456789/":
                #uppercase == white
                #lowercase == black
                if piece == "p":
                    start-=1
                elif piece == "P":
                    start+=1
                elif piece in "nb":
                    start-=3
                elif piece in "NB":
                    start+=3
                elif piece == "r":
                    start-=5
                elif piece == "R":
                    start+=5
                elif piece == "q":
                    start-=9
                elif piece == "Q":
                    start+=9
    else:
        if board.turn == chess.WHITE:
            return -1000
        else:
            return 1000

    return start

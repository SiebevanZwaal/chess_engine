import chess
import random as r

#engine
def make_a_good_move(board):
    '''
    makes a move that is suggested by minimax function
    :param board: current chess board cotaining pieces and legal moves
    '''
    if not board.is_checkmate() and not board.is_stalemate():
        print("checkmate",board.is_checkmate())
        m= minimax(board,True)
        print(m)

        board.push(m[1])

def minimax(board,abp):
    #wrapper of minimax
    if abp:
        return minimax2(board, 5, -100000, 100000)
    else:
        return minimax_without_abp(board,3)

def minimax2(board, depth, alpha, beta):
    '''minimax algorithm that cant deal with checkmate works sometimes because of the alpha beta pruning'''
    if depth ==0:
        return evaluate(board),0
    elif board.is_checkmate():
        return depth +2 *evaluate(board),0
    elif board.outcome() != None:
        return 0,0

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


            alpha = max(currenteval,alpha)


            if alpha >= beta:
                break


        return maxeval,bestmove

    else:
        #min
        mineval = 100000
        for move in legal:
            board.push(move)
            currenteval = minimax2(board, depth - 1, alpha, beta)[0]


            board.pop()


            if currenteval < mineval:
                bestmove_for_black =move
            mineval = min(currenteval,mineval)


            beta = min(currenteval,beta)
            if alpha >= beta:
                break
        return mineval,bestmove_for_black



def minimax_without_abp(board, depth):
    '''minimax algorithm that cant deal with checkmate but works'''
    if depth ==0:
        return evaluate(board),0
    elif board.is_checkmate():
        depth +1 *evaluate(board),0
    elif board.outcome() != None:
        return 0,0

    bestmove =0
    bestmove_for_black =0
    if board.turn == chess.WHITE:
        #max
        maxeval = -100000

        for move in board.legal_moves:
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
        for move in board.legal_moves:
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
                elif piece =="R":
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

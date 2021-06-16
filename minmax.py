import chess
import random as r
#engine
def make_a_good_move(board):
    print("making a good move from mm")

    board.push(minimax(board,False))



def minimax(board,abp):
    #wrapper of minimax
    if abp:
        return minimax2(board, 3, -100000, 100000)[1]
    else:
        return minimax_without_abp(board,3)[1]

def minimax2(board, depth, alpha, beta):
    '''minimax algorithm that cant deal with checkmate works sometimes because of the alpha beta pruning'''
    if board.is_checkmate() or depth ==0:
        return evaluate(board),0
    bestmove =0
    if board.turn == chess.WHITE:
        #max
        maxeval = -100000

        for move in board.legal_moves:
            if bestmove == 0:
                bestmove = move
            board.push(move)
            currenteval,badmove = minimax2(board, depth - 1, alpha, beta)
            maxeval = max(currenteval,maxeval)
            alpha = max(currenteval,alpha)

            board.pop()

            if alpha >= beta:
                break
            if currenteval == maxeval:
                bestmove =move

        return maxeval,bestmove

    else:
        #min
        mineval = 100000
        for move in board.legal_moves:
            board.push(move)
            currenteval,badmove = minimax2(board, depth - 1, alpha, beta)
            mineval = min(currenteval,mineval)
            beta = min(currenteval,beta)
            board.pop()
            if alpha >= beta:
                break
            if currenteval == mineval:
                bestmove =move

        return mineval,bestmove

def minimax_without_abp(board, depth):
    '''minimax algorithm that cant deal with checkmate but works'''
    if board.is_checkmate() or depth ==0:
        return evaluate(board),0
    bestmove =0
    if board.turn == chess.WHITE:
        #max
        maxeval = -100000

        for move in board.legal_moves:
            if bestmove == 0:
                bestmove = move
            board.push(move)
            currenteval,badmove = minimax_without_abp(board, depth - 1)
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
            currenteval,badmove = minimax_without_abp(board, depth - 1)
            mineval = min(currenteval,mineval)
            board.pop()

            if currenteval == mineval:
                bestmove =move

        return mineval,bestmove

def minimax4(board):
    #wrapper of minimax
    m = minimax3(board, 4,4,[])

    print("checkmatelist:",m[2])
    return m[1]


###
# I am currently working on the algoritm below and after it works i will try to implement abp
###


def minimax3(board, depth,ogdebth,nested_checkmate_list):
    '''minimax algoritm that does not really work without abp where i tried to save the moves that lead to checkmate
    debth : how many levels of branches the algorithm has left to go into moves tree
    ogdebth : how many levels of branches the plan was to evaluate at the call of the algorithm
    nested_checkmate_list : a list supposed to contain lists with moves that would lead to checkmate
    '''
    if depth ==0:
        e= evaluate(board)

        return e,0,nested_checkmate_list

    elif board.is_checkmate():
        e= evaluate(board)
        checkmate_list = []
        for i in range(-1,-1*(ogdebth-depth),-1):
            checkmate_list.append(board.move_stack[i])
        checkmate_list.append("checkmatelist with fen of :"+board.board_fen())
        nested_checkmate_list.append(checkmate_list)
        return e,0,nested_checkmate_list


    if depth ==3:
        amount_of_legal_moves=0
        legalmoveslist =[]
        for move in board.legal_moves:
            amount_of_legal_moves+=1
            legalmoveslist.append(move)
        bestmove =legalmoveslist[r.randint(0,amount_of_legal_moves-1)]
    else:
        bestmove =0


    if board.turn == chess.WHITE:
        #max
        maxeval = -100000
        for move in board.legal_moves:

            board.push(move)
            if board.is_checkmate():
                #moves toevoegen per list en dan kijken welke de snelste checkmate is
                checkmate_list = []
                for i in range(-1,-1*(ogdebth-depth)-2,-1):
                    checkmate_list.append(board.move_stack[i])
                checkmate_list.append("checkmatelist with fen of :"+board.board_fen())
                nested_checkmate_list.append(checkmate_list)
                #stops searching
                board.pop()
                return maxeval,bestmove,nested_checkmate_list

            currenteval,badmove,nested_checkmate_list = minimax3(board, depth - 1,ogdebth,nested_checkmate_list)#, alpha, beta)
            if currenteval == 1000:
                bestmove =move
            if currenteval > maxeval:
                maxeval = currenteval
                bestmove =move

            board.pop()




        return maxeval,bestmove,nested_checkmate_list

    else:
        #min
        mineval = 100000
        for move in board.legal_moves:
            board.push(move)
            currenteval,badmove,nested_checkmate_list = minimax3(board, depth - 1,ogdebth,nested_checkmate_list)
            if currenteval < mineval:
                mineval = currenteval

            board.pop()


        return mineval,0,nested_checkmate_list



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



#below is a simple test for minimax to see what they would do in a "checkmate in 2 scenario"




board = chess.Board("7k/8/1R6/R7/8/8/8/7K")
print(board.status())
print(board.board_fen())

print(board.turn == chess.BLACK)
m4 =minimax4(board)
print("minimax 4 suggested move ",m4)
print("minimax 2 suggested move ",minimax(board,True))
print("minimax without abp sugggested move",minimax(board,False))
board.push_uci("a5a7")
board.push_uci("h8g8")

m4 =minimax4(board)
print("minimax 4 suggested move ",m4)
print("minimax 2 suggested move ",minimax(board,True))
print("minimax without abp sugggested move",minimax(board,False))
# print(m in board.legal_moves)
print(board.legal_moves)


print(board.board_fen())




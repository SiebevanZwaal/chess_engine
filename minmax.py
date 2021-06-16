import chess
import random as r
#engine
def make_a_good_move(board):
    print("making a good move from mm")
    #print(board.board_fen())
    # l=[]
    # for move in board.legal_moves:
    #     l.append(move)
    #
    # r=random.randint(0,len(l)-1)
    # print("r",r)
    # print("len(l)",len(l))
    # board.push(minimax2(board,3)[1])
    board.push(minimax(board))
    # uci = "e2e4"
    #return "a7a5"


def minimax(board):
    #wrapper of minimax
    return minimax2(board, 3, -100000, 100000)[1]


def minimax2(board, depth, alpha, beta):
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

        return mineval,0

def minimax4(board):
    #wrapper of minimax
    m = minimax3(board, 4,4,[])
    #[[Move.from_uci('a5a8'), Move.from_uci('h8g8'), Move.from_uci('b6b7')], [Move.from_uci('b6b8'), Move.from_uci('h8g8'), Move.from_uci('a5a7')]]
    print("checkmatelist:",m[2])
    return m[1]

def minimax3(board, depth,ogdebth,nested_checkmate_list):
    if depth ==0:
        e= evaluate(board)

        return e,0,nested_checkmate_list

    elif board.is_checkmate():
        e= evaluate(board)
        checkmate_list = []
        for i in range(-1,-1*(ogdebth-depth),-1):
            # print("ogdebht",ogdebth)
            # print("debth",depth)
            # print("i",i)
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
        # print("max, aka white")
        # print(board.move_stack)
        # print(board.legal_moves)
        for move in board.legal_moves:

            board.push(move)
            if board.is_checkmate():
                #moves toevoegen per list en dan kijken welke de snelste checkmate is
                checkmate_list = []
                for i in range(-1,-1*(ogdebth-depth)-2,-1):
                    # print("ogdebht",ogdebth)
                    # print("debth",depth)
                    # print("i",i)
                    checkmate_list.append(board.move_stack[i])
                checkmate_list.append("checkmatelist with fen of :"+board.board_fen())
                nested_checkmate_list.append(checkmate_list)
                #stops searching
                board.pop()
                return maxeval,bestmove,nested_checkmate_list

            currenteval,badmove,nested_checkmate_list = minimax3(board, depth - 1,ogdebth,nested_checkmate_list)#, alpha, beta)
            if currenteval == 1000:
                #print("bestmove is mat")
                bestmove =move
            # if board.is_checkmate():
            #     print("checkmate",board.board_fen())
            #     currenteval = 1000
            if currenteval > maxeval:
                maxeval = currenteval
                #print("bestmove is niet mat")
                bestmove =move

            board.pop()




        return maxeval,bestmove,nested_checkmate_list

    else:
        #min
        mineval = 100000
        if board.is_check():
            print("min, aka black")
            print(board.move_stack)
            print(board.legal_moves)
        for move in board.legal_moves:
            board.push(move)
            currenteval,badmove,nested_checkmate_list = minimax3(board, depth - 1,ogdebth,nested_checkmate_list)#, alpha, beta)
            # if board.is_checkmate():
            #     print("checkmate",board.board_fen())
            #     currenteval = -1000
            if currenteval < mineval:
                mineval = currenteval
                #bestmove =move

            board.pop()


        return mineval,0,nested_checkmate_list

def minimaxscore(board, depth):#, alpha, beta):

    if board.is_checkmate() or depth ==0:
        e= evaluate(board)
        print(e)
        return e#evaluate(board)#,0
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
            # currenteval,badmove = minimax3(board, depth - 1)#, alpha, beta)
            currenteval = minimax3(board, depth - 1)#, alpha, beta)

            if currenteval > maxeval:
                maxeval = currenteval
                #bestmove =move
            #maxeval = max(currenteval,maxeval)
            # alpha = max(currenteval,alpha)
            # if currenteval == maxeval:
            #     bestmove =move
            board.pop()

            # if alpha >= beta:
            #     break


        return maxeval#,bestmove

    else:
        #min
        mineval = 100000
        for move in board.legal_moves:
            board.push(move)
            #currenteval,badmove = minimax3(board, depth - 1)#, alpha, beta)
            currenteval = minimax3(board, depth - 1)#, alpha, beta)

            if currenteval < mineval:
                mineval = currenteval


            # beta = min(currenteval,beta)
            board.pop()
            # if alpha >= beta:
            #     break

        return mineval#,0    #bestmove

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
            print("evalated mat black won")
            return -1000
        else:
            print("evalated mat white won")
            return 1000

    return start


board = chess.Board("7k/8/1R6/R7/8/8/8/7K")
print(board.status())
print(board.board_fen())
# board.push_uci("e4d5")
print(board.turn == chess.BLACK)
m =minimax4(board)
print("score = ",m)
# print(m in board.legal_moves)
print(board.legal_moves)
board.push_uci("a5a8")
print(board.legal_moves)

print(board.board_fen())
print(evaluate(board))
# board.push_uci("d6d8")

print(evaluate(board))

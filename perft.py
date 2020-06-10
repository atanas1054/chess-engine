import chess

board = chess.Board()


def Perft(depth):

   move_list = []

   nodes = 0
   for move in board.legal_moves:
       move_list.append(move)
   n_moves = len(move_list)

   for i in range(n_moves):
        if (depth == 1):
            nodes+=1
        else:
           board.push(move_list[i])
           nodes += Perft(depth - 1)
           board.pop()

   return nodes

#print(Perft(6))
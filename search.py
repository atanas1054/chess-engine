import chess
from evaluation import *

def MVV_LVA(board: chess.Board, m: chess.Move):

    moving_piece = board.piece_at(m.from_square)
    attacked_piece = board.piece_at(m.to_square)
    order = 0
    if attacked_piece:
        # P=1, N=2, B=3, R=4, Q=5, K=6,
        order = PIECE_VALUES[attacked_piece.piece_type] - moving_piece.piece_type
    return order


#negamax
def negamax(board, depth, ply=0, MAX_PLY = 128):
    """
    """
    if depth <= 0:
        # This is a leaf node. So use plain evaluation or quiescence search.
        return evaluate_board(board), []

    if ply >= MAX_PLY:
        # Hard stop on search depth.
        return evaluate_board(board), []

    if board.is_fivefold_repetition() or board.is_stalemate() or board.is_seventyfive_moves() or board.is_insufficient_material():
        return 0, []

    if board.is_checkmate():
        # Board is in checkmate, return a distance from mate score.
        return -100000 + ply, []

    best_value = -9999999
    pv = []
    for move in board.legal_moves:
        board.push(move)
        search_value, child_pv = search(board, depth - 1, ply + 1)
        search_value = -search_value
        board.pop()
        if search_value > best_value:
            best_value = search_value
            pv = [move] + child_pv

    return best_value, pv

#minimax
# def minimax(board, depth, maximizingPlayer):
#     if depth == 0 or game over in position
#         return static evaluation of position
#
#     if maximizingPlayer:
#         maxEval = -infinity
#         for each child of position
#             eval = minimax(child, depth - 1, false)
#             maxEval = max(maxEval, eval)
#         return maxEval
#
#     else:
#         minEval = +infinity
#         for each child of position
#             eval = minimax(child, depth - 1, true)
#             minEval = min(minEval, eval)
#         return minEval

#alpha-beta negamax

def search(board, alpha, beta, depth, ply=0):

    if depth <= 0:
        # This is a leaf node. So use plain evaluation or quiescence search.
        return evaluate_board(board), []


    if board.is_checkmate():
        # Board is in checkmate, return a distance from mate score.
        return -100000 + ply, []

    if board.is_fivefold_repetition() or board.is_stalemate() or board.is_seventyfive_moves() or board.is_insufficient_material():
        return 0, []

    # Sort moves according to a MMV-LVA
    legal_moves = sorted(board.legal_moves, reverse=True,
                         key=lambda m: MVV_LVA(board, m))

    best_score = -9999999
    pv = []
    for move in legal_moves:
        board.push(move)

        # The bounds are inverted and negated due to Negamax.
        score, child_pv = search(board, -beta, -alpha, depth - 1, ply + 1)
        # The return value is negated due to Negamax.
        score = -score
        board.pop()

        if score > best_score:
            # The best move till now, but PV is not updated since it
            # does not necessarily beat alpha.
            best_score = score

        if best_score > alpha:
            # The move beats (and therefore raises) alpha. PV
            # can be updated.
            alpha = best_score
            pv = [move] + child_pv

        if best_score >= beta:
            # Beta-cutoff. This was a CUT-node.
            #return beta, []
            break

    # If alpha was raised (and did not cause a beta-cutoff), then the node
    # is considered a PV-node. Otherwise it is an ALL-node.
    return best_score, pv
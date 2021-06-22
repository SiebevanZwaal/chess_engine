from unittest import TestCase
import chess
import minmax

class Test(TestCase):
    def test_make_a_good_move(self):
        board = chess.Board("7k/R7/1R6/8/8/8/8/7K")
        minmax.make_a_good_move(board)
        self.assertTrue(board.is_checkmate())
        board = chess.Board("7k/8/1R6/R7/8/8/8/7K")
        minmax.make_a_good_move(board)
        minmax.make_a_good_move(board)
        minmax.make_a_good_move(board)
        self.assertTrue(board.is_checkmate())

def test_evaluate(self):
        board = chess.Board()
        eval = minmax.evaluate(board)
        self.assertEqual(eval,0)
        board = chess.Board("qrbkp3/8/8/8/8/8/8/6K1")
        eval = minmax.evaluate(board)
        self.assertEqual(eval,-18)
        board = chess.Board("QRBKP3/8/8/8/8/8/8/6k1")
        eval = minmax.evaluate(board)
        self.assertEqual(eval,18)



import chess
import chess.svg
import numpy as np
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget


class MainWindow(QWidget):
    def __init__(self, bitboard):
        super().__init__()

        self.setGeometry(100, 100, 325, 325)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 300, 300)

        self.chessboardSvg = chess.svg.board(
            None, squares=chess.SquareSet(bitboard)).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)


def bitboard_to_svg(bitboard):
    app = QApplication([])
    window = MainWindow(bitboard)
    window.show()
    app.exec()


bitboard_to_svg(chess.BB_RANK_8)

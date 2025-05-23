import os
from PyQt6.QtCore import Qt, QPoint, QRectF
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPolygon, QPainterPath


class BoardImage(QLabel):
    def __init__(self, parent=None):
        super(BoardImage, self).__init__(parent)

        directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(directory, 'images', 'board.png')
        image = QPixmap(image_path)

        # Rounding corners
        image_rounded = QPixmap(image.size())
        image_rounded.fill(Qt.GlobalColor.transparent)
        painter = QPainter(image_rounded)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        clip_path = QPainterPath()
        rectangle = QRectF(image.rect())
        clip_path.addRoundedRect(rectangle, 15, 15)
        painter.setClipPath(clip_path)
        painter.drawPixmap(0, 0, image)
        painter.end()

        self.setPixmap(image_rounded)
        self.setFixedSize(image.size())

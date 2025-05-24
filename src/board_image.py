import os
import math
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

        self.arrow: list[QPoint] = []

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 255, 140)) # temporary blue, exact blue will be added later

        arrow = QPolygon([
            QPoint(399, 400),
            QPoint(398, 399),
            QPoint(397, 399),
            QPoint(396, 398),
            QPoint(395, 397),
            QPoint(395, 396),
            QPoint(394, 395),
            QPoint(394, 200),
            QPoint(394 - 21, 200),
            QPoint(400, 200 - 28),
            QPoint(401, 200 - 28),
            QPoint(407 + 21, 200),
            QPoint(407, 200),
            QPoint(407, 395),
            QPoint(406, 396),
            QPoint(406, 397),
            QPoint(405, 398),
            QPoint(404, 399),
            QPoint(403, 399),
            QPoint(402, 400),
        ])

        painter.drawPolygon(arrow)

        if self.arrow:
            painter.drawPolygon(self.arrow)
        
        painter.end()

    def draw_arrow(self, origin: QPoint, destination: QPoint):
        arrow_length = self.move_distance(origin, destination)

        arrow_tip_length = 28
        arrow_tip_added_width = 21
        arrow_bottom_length = 6
        arrow_body_length = arrow_length - arrow_tip_length - arrow_bottom_length + 1

        origin.setY(origin.y() + 1)

        self.arrow.clear()

        self.arrow.append(QPoint(origin.x() - 1, origin.y()))
        self.arrow.append(QPoint(self.arrow[-1].x() - 1, self.arrow[-1].y() - 1))
        self.arrow.append(QPoint(self.arrow[-1].x() - 1, self.arrow[-1].y()))
        self.arrow.append(QPoint(self.arrow[-1].x() - 1, self.arrow[-1].y() - 1))
        self.arrow.append(QPoint(self.arrow[-1].x() - 1, self.arrow[-1].y() - 1))
        self.arrow.append(QPoint(self.arrow[-1].x(), self.arrow[-1].y() - 1))
        self.arrow.append(QPoint(self.arrow[-1].x() - 1, self.arrow[-1].y() - 1))
        self.arrow.append(QPoint(self.arrow[-1].x(), self.arrow[-1].y() - arrow_body_length))
        self.arrow.append(QPoint(self.arrow[-1].x() - arrow_tip_added_width, self.arrow[-1].y()))
        self.arrow.append(QPoint(origin.x(), self.arrow[-1].y() - arrow_tip_length))
        self.arrow.append(QPoint(self.arrow[-1].x() + 1, self.arrow[-1].y()))
        self.arrow.append(QPoint(self.arrow[-1].x() + 6 + arrow_tip_added_width, self.arrow[-1].y() + arrow_tip_length))
        self.arrow.append(QPoint(self.arrow[-1].x() - arrow_tip_added_width, self.arrow[-1].y()))
        self.arrow.append(QPoint(self.arrow[-1].x(), self.arrow[-1].y() + arrow_body_length))
        self.arrow.append(QPoint(self.arrow[-1].x() - 1, self.arrow[-1].y() + 1))
        self.arrow.append(QPoint(self.arrow[-1].x(), self.arrow[-1].y() + 1))
        self.arrow.append(QPoint(self.arrow[-1].x() - 1, self.arrow[-1].y() + 1))
        self.arrow.append(QPoint(self.arrow[-1].x() - 1, self.arrow[-1].y() + 1))
        self.arrow.append(QPoint(self.arrow[-1].x() - 1, self.arrow[-1].y()))
        self.arrow.append(QPoint(self.arrow[-1].x() - 1, self.arrow[-1].y() + 1))

        self.update()

    def move_distance(self, origin: QPoint, destination: QPoint):
        return int(math.hypot(destination.x() - origin.x(), destination.y() - origin.y()))

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
        self.origin = QPoint()
        self.rotation = 0.0

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 255, 140)) # temporary blue, exact blue will be added later

        if self.arrow:
            painter.translate(self.origin)
            painter.rotate(self.rotation)
            painter.translate(- self.origin)

            painter.drawPolygon(self.arrow)
            
            painter.translate(self.origin)
            painter.rotate(- self.rotation)
            painter.translate(- self.origin)
        
        painter.end()

    def draw_arrow(self, origin: QPoint, destination: QPoint):
        arrow_length = self.calculate_move_distance(origin, destination)

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

        origin.setY(origin.y() - 1)
        self.origin = origin
        self.rotation = self.calculate_rotation(origin, destination)

        self.update()

    def calculate_move_distance(self, origin: QPoint, destination: QPoint):
        return int(math.hypot(destination.x() - origin.x(), destination.y() - origin.y()))

    def calculate_rotation(self, origin: QPoint, destination: QPoint):
        dx = destination.x() - origin.x()
        dy = destination.y() - origin.y()
        angle_to_destination = math.atan2(dy, dx)
        angle_up = -math.pi / 2
        return math.degrees(angle_to_destination - angle_up)

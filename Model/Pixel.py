from PyQt5.Qt import QColor,QImage

class Pixels():
    @staticmethod
    def pix(file_path):
        myPixmap = QImage(file_path)
        if myPixmap.byteCount() == 0:
            return [0, 0, 0]
        size_h = myPixmap.height()
        size_w = myPixmap.width()
        if (size_h or size_w)>250:
            size_h=250
            size_w=250
        rgb = [0, 0, 0]
        for x in range(size_h):
            for y in range(size_w):
                a = QColor(myPixmap.pixel(x, y))
                rgb[0] += a.red()
                rgb[1] += a.green()
                rgb[2] += a.blue()
        rgb[0] = int(rgb[0] / (size_h * size_w))
        rgb[1] = int(rgb[1] / (size_w * size_h))
        rgb[2] = int(rgb[2] / (size_h * size_w))
        return rgb

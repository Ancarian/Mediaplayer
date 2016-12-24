from PyQt5.Qt import QColor, QImage, QPixmap


class Pixels:
    @staticmethod
    def pix(file_path):
        my_pixmap = QImage(file_path)
        if my_pixmap.byteCount() == 0:
            return [0, 0, 0]
        size_h = my_pixmap.height()
        size_w = my_pixmap.width()

        rgb = [0, 0, 0]
        result_x, result_y = 0, 0
        for x in range(0, size_h, 3):
            for y in range(0, size_w, 3):
                a = QColor(my_pixmap.pixel(x, y))

                if (a.red()>30 and a.blue()>30 and a.green()>30) and (a.red()<225 and a.blue()<225 and a.green()<225):
                    rgb[0] += a.red()
                    rgb[1] += a.green()
                    rgb[2] += a.blue()
                    result_x+=1
                    result_y+=1

        for i in range(len(rgb)):
            rgb[i] = rgb[i] / (result_x)


        return rgb

    @staticmethod
    def resize(file_path, x):
        my_pixmap = QPixmap(file_path)
        h = my_pixmap.size().height()
        if h > x:
            ratio = h / x
        else:
            ratio = x / h
        my_pixmap.setDevicePixelRatio(ratio)
        return my_pixmap



from torch import nn
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
import os

_default_fill = "#000000"
# _default_fill = "#ffffff"
_shaps = ('chord', 'pieslice', 'ellipse', 'rectangle', 'polygon')  # 弦，椭圆，矩形，扇形区，多边形
MIN = 30


class Graph(nn.Module):
    # part * part 个 height * width 画布 ，每块用（x,y)表示
    def __init__(self, height=400, width=400, part=1, color=None):
        super().__init__()
        if color is None:
            # color = [255., 255., 255.]
            color = [0., 0., 0., 0.]

        self.back_height = height
        self.back_width = width
        background = np.ndarray((height * part, width * part, 4), np.uint8)
        background[:, :, 0] = color[0]
        background[:, :, 1] = color[1]
        background[:, :, 2] = color[2]
        background[:, :, 3] = color[3]
        self._background = background  # 背景画布
        self._part = part
        image = Image.fromarray(self._background)
        self._image = image  # 绘制对象
        drawer = ImageDraw.Draw(image)
        self._drawer = drawer  # 画笔
        self._area = []

    def draw(self, shapes, p):
        print('*****************************draw*****************************')
        step = 0
        # shap_with_info = []
        # pos = (0, 0, 0, 0)
        back_central = ((p[1] - 0.5) * self.back_width, (p[0] - 0.5) * self.back_height)
        # for part, shap in shapes:
        print(back_central)
        part = shapes[0]
        shap = shapes[1]
        print(part)
        print(shap)

        min = max(part / 2, MIN)

        if shap == _shaps[0]:  # chord
            # 生成随机参数
            radius = random.randrange(min // 2, part // 2)
            central = back_central
            start = random.randrange(0, 360 - MIN)
            end = random.randrange(start + MIN, 360 + 1)
            self.chord(central, radius, start, end)
            # shap_with_info.append((shap, (central, radius, start, end)))
            print(radius)
            print(central)
        elif shap == _shaps[1]:  # pieslice
            # 生成随机参数
            radius = random.randrange(min // 2, part // 2)
            central = back_central
            start = random.randrange(0, 360 - MIN)
            end = random.randrange(start + MIN, 360 + 1)
            self.pieslice(central, radius, start, end)
            # shap_with_info.append((shap, (central, radius, start, end)))
            print(radius)
            print(central)
        elif shap == _shaps[2]:  # ellipse
            width = random.randrange(MIN, part)
            height = random.randrange(MIN, part)
            pos = (back_central[0] - width // 2, back_central[1] - height // 2, back_central[0] + width // 2,
                   back_central[1] + height // 2)
            print(pos)
            self.ellipse(pos)
        elif shap == _shaps[3]:  # rectangle
            width = random.randrange(MIN, part)
            height = random.randrange(MIN, part)
            pos = (back_central[0] - width // 2, back_central[1] - height // 2, back_central[0] + width // 2,
                   back_central[1] + height // 2)
            self.rectangle(pos)
        elif shap == _shaps[4]:  # polygon
            print('*******polygon******')

            positon = []
            sides = random.randrange(3, 7)
            for step in range(sides):
                px = random.randrange(back_central[0] - self.back_width // 2, back_central[0] + self.back_width // 2)
                py = random.randrange(back_central[1] - self.back_height // 2, back_central[1] + self.back_height // 2)
                positon.append((px, py))
                # positon.append(py)
            print(sides)
            print(positon)
            self.polygon(positon)

        step += 1
        return self.area_compute(back_central)

    def area_compute(self, back_central):
        print('*****************************area_compute*****************************')
        pixel_count = 0
        for x in range(int(back_central[0] - self.back_width // 2), int(back_central[0] + self.back_width // 2)):
            for y in range(int(back_central[1] - self.back_height // 2), int(back_central[1] + self.back_height // 2)):
                if self._image.getpixel((x, y)) != (0, 0, 0, 0):
                    pixel_count += 1
        # print(pixel_count)
        self._area.append(pixel_count)
        return (pixel_count, self.back_width * self.back_height)

    # return shapes

    def line(self, pos=(0, 0, 10, 10), color=_default_fill, width=0):
        self._drawer.line((pos[0], pos[1], pos[2], pos[2]), color, width)

    #  画弦 start = 开始的角度
    # 含义：和方法arc()一样，但是使用直线连接起始点。
    # 变量options的outline给定弦轮廓的颜色。Fill给定弦内部的颜色。
    def chord(self, central, radius, start=0, end=180, color=_default_fill):
        self._drawer.chord((central[0] - radius, central[1] - radius, central[0] + radius, central[1] + radius), start,
                           end,
                           fill=color)

    # Pieslice
    # 定义：draw.pieslice(xy,start, end, options)
    # 含义：和方法arc()一样，但是在指定区域内结束点和中心点之间绘制直线。
    # 变量options的fill给定pieslice内部的颜色。
    def pieslice(self, central, radius, start=0, end=180, color=_default_fill):
        self._drawer.pieslice((central[0] - radius, central[1] - radius, central[0] + radius, central[1] + radius),
                              start,
                              end,
                              fill=color)

    def ellipse(self, pos=(0, 0, 0, 0), color=_default_fill):
        self._drawer.ellipse(pos, fill=color)

    # arc
    # 定义：draw.arc(xy, start, end, options)
    # 含义：在给定的区域内，在开始和结束角度之间绘制一条弧（圆的一部分）。
    # arc。
    def arc(self, central, radius, start=0, end=180, color=_default_fill):
        self._drawer.arc((central[0] - radius, central[1] - radius, central[0] + radius, central[1] + radius),
                         start,
                         end,
                         fill=color)

    # 绘制一个多边形。
    # 多边形轮廓由给定坐标之间的直线组成，在最后一个坐标和第一个坐标间增加了一条直线，形成多边形。
    # 坐标列表是包含2元组[(x,y),…]或者数字[x,y,…]的任何序列对象。它最少包括3个坐标值。
    # 变量options的fill给定多边形内部的颜色。
    def polygon(self, xy, color=_default_fill):
        self._drawer.polygon(xy, fill=color)

    # Re
    # ctangle
    # xy = [x0,y0,x1,y1]
    def rectangle(self, xy, color=_default_fill):
        self._drawer.rectangle(xy, fill=color)

    # Point
    # 定义：draw.point(xy,options)
    # 含义：在给定的坐标点上画一些点。
    # point。
    def point(self, points, color=_default_fill):
        self._drawer.point(points, fill=color)

    def show(self, title=None):
        self._image.show(title)

    def clear(self):
        image = Image.fromarray(self._background)
        self._image = image  # 绘制对象
        drawer = ImageDraw.Draw(image)
        self._drawer = drawer  # 画笔

    def save(self, name, quality=100):
        self._image.save(name, quality=quality)

    # def to_svg(self, name):
    #     os.system('python evaluate_gpu.py | tee -a %s' % result)

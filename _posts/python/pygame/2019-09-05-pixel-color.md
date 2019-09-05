---
layout: article
title: pixel and color
permalink: /_posts/python/pygame/2019-09-05-pixel-color 
tags: Pygame
aside:
  toc: true
sidebar:
  nav: Pygame
---

<!--more-->

## 像素

凑近显示器，你能看到图像是由一个一个点构成的，这些点就是像素。一个分辨率为 $1280 \times 1024$ 的显示器，有 $1280 \times 1024 = 1310720$ 个像素。一个 `RGB` 系统，每个像素可以显示 $256 \times 256 \times 256 = 16777216‬$ 种颜色。（推荐阅读博客：[一张白纸可以承载多少](https://eyehere.net/2011/how-many-image-in-one-paper/)）

如果将 $16777216‬$ 种颜色全部显示出来，可以使用一个分辨率为 $4096 \times 4096$ 的图像来实现。下面写一个小程序来实现这个功能：

```python
import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))

all_colors = pygame.Surface((4096, 4096), depth=24)

x = 0
y = -1


def get_pixel():
    global x, y
    if y >= 4096:
        x += 1
        y = 0
    else:
        y += 1
    pixel = (x, y)
    return pixel


for r in range(256):
    print(r + 1, "out of 256")
    for g in range(256):
        for b in range(256):
            all_colors.set_at(get_pixel(), (r, g, b))  # 设置像素的颜色

pygame.image.save(all_colors, "allcolors.bmp")

```

下图即为输出结果：

![image](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/python/pygame/assets/1.jpg)

## 颜色

我们大概都知道，将蓝色和黄色混合就成了绿色。事实上，我们可以使用**红黄蓝**（光学三原色）混合出所有的颜色。而电脑屏幕上的三原色是**红绿蓝**。我们可以写一个程序来展示使用不同程度的红绿蓝三原色混合之后颜色：

```python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit

# 窗口分辨率
SCREEN_WIDTH = 640  # 宽
SCREEN_HEIGHT = 480  # 高


def create_scales(height):
    red_scale_surface = pygame.surface.Surface((SCREEN_WIDTH, height))
    green_scale_surface = pygame.surface.Surface((SCREEN_WIDTH, height))
    blue_scale_surface = pygame.surface.Surface((SCREEN_WIDTH, height))

    for x in range(SCREEN_WIDTH):
        # x/(SCREEN_WIDTH-1) 的取值为 [0, 1]
        # color 的取值为 [0, 255]
        color = int((x/(SCREEN_WIDTH-1))*255)
        red = (color, 0, 0)
        green = (0, color, 0)
        blue = (0, 0, color)
        line_rect = (x, 0, 1, height)
        pygame.draw.rect(red_scale_surface, red, line_rect)
        pygame.draw.rect(green_scale_surface, green, line_rect)
        pygame.draw.rect(blue_scale_surface, blue, line_rect)
    return red_scale_surface, green_scale_surface, blue_scale_surface


def run():
    # 游戏初始化
    pygame.init()
	# 创建窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    red_scale, green_scale, blue_scale = create_scales(80)

    color = [127, 127, 127]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        screen.fill((0, 0, 0))

        screen.blit(red_scale, (0, 0))
        screen.blit(green_scale, (0, 80))
        screen.blit(blue_scale, (0, 160))

        # 获取鼠标的位置
        x, y = pygame.mouse.get_pos()

        # 如果按下鼠标左键，获取按下位置对应颜色
        if pygame.mouse.get_pressed()[0]:
            for item in range(3):
                if (y > item*80) and (y < (item + 1)*80):
                    color[item] = int((x/(SCREEN_WIDTH-1))*255)
            pygame.display.set_caption("PyGame Color Test - "+str(tuple(color)))

        # 更新圆的位置
        for item in range(3):
            pos = (int((color[item]/255)*(SCREEN_WIDTH-1)), item*80 + 40)
            pygame.draw.circle(screen, (255, 255, 255), pos, 20)

        pygame.draw.rect(screen, tuple(color), (0, 240, 640, 240))

        pygame.display.update()


if __name__ == '__main__':
    run()

```

运行结果为：

![image](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/python/pygame/assets/2.png)

在这个例子里，你可以用鼠标移动三个白点，代表了三原色的量，下面就是不同混合得到的结果，在标题上你可以看到 `RGB` 三个数值。

## 颜色的变亮和变暗

如果把颜色 `RGB` 的每一个数值乘以一个小于 $1$ 的非负数（注意：颜色的 `RGB` 值必须是一个整数，所以需要将结果取整），那么颜色就会变暗。

如果将颜色 `RGB` 的每一个数值乘以一个大于 $1$ 的数值，那么颜色就会变亮，不过要注意，`RGB` 的最大值是 $255$，所以超过 $255$ 的数值都要设置成 $255$。

## 颜色的混合

我们用一种叫做“**线性插值(linear interpolation)**”的方法来做这件事情。为了找到两种颜色的中间色，我们将这第二种颜色与第一种颜色的差乘以一个0~1之间的小数，然后再加上第一种颜色就行了。如果这个数为0，结果就完全是第一种颜色；是1，结果就只剩下第二种颜色；中间的小数则会皆有两者的特色。

```python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit


color1 = (221, 99, 20)
color2 = (96, 130, 51)
factor = 0


def blend_color(color1, color2, factor):
    (r1, g1, b1) = color1
    (r2, g2, b2) = color2
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return r, g, b


def main():
    global factor
    pygame.init()

    screen = pygame.display.set_mode((640, 480))

    pygame.draw.circle(screen, color1, (int(factor * 639.0), 120), 10)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        screen.fill((255, 255, 255))

        tri = [(0, 120), (639, 100), (639, 140)]
        pygame.draw.polygon(screen, color2, tri)

        x, y = pygame.mouse.get_pos()

        if pygame.mouse.get_pressed()[0]:
            factor = x / 639.0
            pygame.display.set_caption("Pygame Color Blend Test - %.3f" % factor)

        color = blend_color(color1, color2, factor)
        pygame.draw.circle(screen, color, (int(factor * 639.0), 120), 10)
        pygame.draw.rect(screen, color, (0, 240, 640, 240))

        pygame.display.update()


if __name__ == '__main__':
    main()
```

运行结果：

![image](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/python/pygame/assets/3.png)

在这里例子里，移动小球你能看到小球和下方的颜色在“橙色”和“绿色”之间渐变。
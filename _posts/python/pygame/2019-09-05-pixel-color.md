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

![image](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/python/pygame/assets/allcolors.jpg)

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

![image](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/python/pygame/assets/1567322970038.png)

在这个例子里，你可以用鼠标移动三个白点，代表了三原色的量，下面就是不同混合得到的结果，在标题上你可以看到 `RGB` 三个数值。


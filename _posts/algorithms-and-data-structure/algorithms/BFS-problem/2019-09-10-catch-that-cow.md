---
layout: article
title: catch that cow
permalink: /_posts/algorithms-and-data-structure/algorithms/BFS-problem/2019-09-10-catch-that-cow
tags: Algorithms
aside:
  toc: true
sidebar:
  nav: Algorithms
---

<!--more-->

### 问题描述

农夫知道一头牛的位置，想要抓住它。农夫和牛都位于数轴上，农夫起始位于点 $N(0 \le N \le 100000)$，牛位于点$K(0 \le K \le 100000)$。农夫有三种移动方式：

1. 从 $N$ 点移动到 $N-1$，花费一分钟。
2. 从 $N$ 点移动到 $N + 1$，花费一分钟。
3. 从 $N$ 点移动到 $2 * N$，花费一分钟。

假设牛没有意识到农夫的行动，站在原地不动。农夫最少需要花多少时间才能抓到牛？

### 输入

两个整数，$N$ 和 $K$。

### 输出

一个整数，农夫抓住牛所要花费的最少的时间。

### 样例输入

```python
5 17
```

### 样例输出

```python
4
```

### 问题分析

广度优先搜索（BFS, Breadth-First Search）是按照距离初始状态由远及近的顺序进行搜索的，因此经常用来求最短路径之类的问题。结合[博客](https://blog.csdn.net/qq_34690929/article/details/77461552#question)的图片来分析一下 `BFS` 算法。

![img](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/algorithms-and-data-structure/algorithms/BFS-problem/assets/20170821233341072.png)

在广度优先搜索中，需要使用到**队列**来按顺序将每层的节点进行处理。

初始位置 5 入队列。

取出队列首部位置 5 ，计算下一个位置，就是 4，6，10 三个位置，将其依次入队列。

取出队列首部位置 4，计算下一个状态，就是 3，5，8，但是由于初始位置就是 5，5 这个位置已经被处理过了，所以 5 这个位置不用再入队列，只将 3，8 位置入队列。

同理，不断循环操作队列，当找到目标节点，返回的层数就是最少的时间；如果队列为空时还找不到目标节点，则说明没办法到达目标节点。

### python 代码实现

```python
# -*- coding: utf-8 -*-
from queue import Queue

MAXN = int(1e5)  # 位置的最大值
open = Queue()  # 初始化一个队列
close = [False for _ in range(MAXN + 10)]  # 用来记录位置是否已经到达过，如果为True，则到达过，否则没有到达过。

start, end = map(int, input().strip().split())


class Step:
    def __init__(self, pos, step):
        self.pos = pos  # 记录当前位置
        self.step = step  # 记录到达当前位置所用的时间


def bfs():
    open.put(Step(start, 0))
    close[start] = True
    while not open.empty():
        cur = open.get()  # 取出队列首部元素，计算下一个位置
        if cur.pos == end:  # 找到目标位置
            print(cur.step)
            break
        else:
            if cur.pos - 1 > 0 and not close[cur.pos - 1]:
                open.put(Step(cur.pos - 1, cur.step + 1))
                close[cur.pos - 1] = True
            if cur.pos + 1 < MAXN and not close[cur.pos + 1]:
                open.put(Step(cur.pos + 1, cur.step + 1))
                close[cur.pos + 1] = True
            if cur.pos * 2 < MAXN and not close[cur.pos * 2]:
                open.put(Step(cur.pos * 2, cur.step + 1))
                close[cur.pos * 2] = True
    print('-1')


if __name__ == '__main__':
    bfs()

```


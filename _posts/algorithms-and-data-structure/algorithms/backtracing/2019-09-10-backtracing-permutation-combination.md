---
layout: article
title: backtracing implement permutation and combination
permalink: /_posts/algorithms-and-data-structure/algorithms/backtracing/2019-09-10-backtracing-permutation-combination
tags: Algorithms
aside:
  toc: true
sidebar:
  nav: Algorithms
---

<!--more-->

排列组合分为两大类：第一类，待处理的序列中任意两个元素都不相同；第二类，待处理的序列中存在相同元素。但是这两类问题，都可以使用**集合**来很好的解决。

## 全排列（Permutation）

```python
class Permutation:
    def __init__(self, sequence, num=None):
        """
        对序列 sequence 中的元素进行全排列
        :param sequence: list 一个待处理的序列
        :param num: 默认为None, 表示对序列中的所有元素进行全排列，如果用户给定了值，则表示从 sequence 挑选 num 个元素进行全排列
        """
        assert type(sequence) is list
        assert len(sequence) > 0
        self.__sequence = sequence
        self.__n = len(self.__sequence)
        if num is None:
            self.__m = self.__n
        else:
            assert type(num) is int
            assert num <= self.__n
            self.__m = num
        self.__vis = [False for _ in range(self.__n)]
        self.__record = []
        self.__total_case = 0  # 记录所有的案例数
        self.__result = set()  # 全排列的所有情况

        self.__dfs()

    def __dfs(self):
        if len(self.__record) == self.__m:
            self.__total_case += 1
            self.__result.add(str(self.__record))
            return
        else:
            for i in range(self.__n):  # 全排列是从头到尾遍历
                if not self.__vis[i]:
                    self.__vis[i] = True
                    self.__record.append(self.__sequence[i])
                    self.__dfs()
                    self.__record.pop()
                    self.__vis[i] = False

    @property
    def total_case(self):
        return self.__total_case

    @property
    def result(self):
        return self.__result
```



## 组合（Combination）

```python
class Combination:
    def __init__(self, sequence, num=None):
        """
        对序列 sequence 中的元素进行组合
        :param sequence: list 一个待处理的序列
        :param num: 默认为None, 表示对序列中的所有元素进行组合，如果用户给定了值，则表示从 sequence 挑选 num 个元素进行组合
        """
        assert type(sequence) is list
        assert len(sequence) > 0
        self.__sequence = sequence
        self.__n = len(self.__sequence)
        if num is None:
            self.__m = self.__n
        else:
            assert type(num) is int
            assert num <= self.__n
            self.__m = num
        self.__vis = [False for _ in range(self.__n)]
        self.__record = []
        self.__total_case = 0  # 记录所有的案例数
        self.__result = set()

        self.__dfs(0)

    def __dfs(self, num: int):
        if len(self.__record) == self.__m:
            self.__total_case += 1
            self.__result.add(str(self.__record))
            return
        else:
            for i in range(num, self.__n):  # 组合是从当前下标往后选择，
                if not self.__vis[i]:
                    self.__vis[i] = True
                    self.__record.append(self.__sequence[i])
                    self.__dfs(i + 1)
                    self.__record.pop()
                    self.__vis[i] = False

    @property
    def total_case(self):
        return self.__total_case

    @property
    def result(self):
        return self.__result
```


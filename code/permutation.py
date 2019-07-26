# -*- coding: utf-8 -*-

"""

"""


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
        self.__result = set()

        self.__dfs()

    def __dfs(self):
        if len(self.__record) == self.__m:
            self.__total_case += 1
            self.__result.add(str(self.__record))
            return
        else:
            for i in range(self.__n):
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


if __name__ == '__main__':
    per = Permutation([1, 2, 3], 3)
    print(per.total_case)
    print(per.result)

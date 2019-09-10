---
layout: article
title: set cover problem
permalink: /_posts/algorithms-and-data-structure/algorithms/greedy-problem/2019-09-10-set-cover-problem
tags: Algorithms
aside:
  toc: true
sidebar:
  nav: Algorithms
---

<!--more-->

## 概念

集合覆盖问题（`Set Cover Problem`）：给定一个集合 $U$ 有 $n$ 个元素，一个由集合 $U$ 的子集组成的集合 $S=\{S_1, S_2, \cdots, S_m\}$，其中每一个子集 $S_i$ 都有一个对应的成本（`Cost`） 。我们的目标是找到一个拥有最小成本的 $S$ 的子集能够覆盖所有的元素。

**示例**：

> 输入：
>
> $U=\{1,2,3,4,5\}$
> $S=\{S_1, S_2, S_3\}$
> $S_1=\{4,1,3\}$ ，$Cost(S_1)=5$
> $S_2=\{2,5\}$，$Cost(S_2)=10$
> $S_3=\{1,4,3,2\}$，$Cost(S_3)=3$
>
> 输出：
> 选择的集合为 $\{S_2, S_3\}$，其成本为 $13$。
>
> 集合 $S$ 的所有子集为 $\{S_1\}$，$\{S_2\}$，$\{S_3\}$，$\{S_1, S_2\}$，$\{S_1, S_3\}$，$\{S_2, S_3\}$，$\{S_1, S_2, S_3\}$ 和 $\varnothing$，总共有 $2^3=8$ 种情况。而其中能够覆盖集合 $U$ 中所有元素的集合只有 $\{S_1, S_2\}$，$\{S_2, S_3\}$ 和 $\{S_1, S_2, S_3\}$。成本最低的就是 $\{S_2, S_3\}$。

## 贪婪算法

贪婪算法（`Greedy algorithm`），或者叫暴力求解算法（`Brute-Force algorithm`）。

>1. Let $I$ represents set of elements included so far.  Initialize $I = \{\}$.
>
>2. while $I$ != $U$ do
>
>   - Find the set $S_i$ in $\{S_1, S_2, \dots, S_m\}$ whose cost effectiveness is smallest, i.e., the ratio of cost $Cost(S_i)$ and number of newly added elements is minimum. 
>     Basically we pick the set for which following value is minimum: 
>
>   $$
>   \frac{Cost(Si)}{|Si - I|} \tag{1}
>   $$
>
>   - Add elements of above picked $S_i$ to $I$, i.e.,  $I = I \bigcup S_i$.

让我们通过详细地描述解上述示例的过程来理解贪婪算法：

>First iteration:
>$I=\{\}$
>The cost of $S_1$: $\frac{Cost(S_1)}{|S_1-I|}=\frac{5}{3}$
>The cost of $S_2$: $\frac{Cost(S_2)}{|S_2-I|}=\frac{10}{2}$
>The cost of $S_3$: $\frac{Cost(S_3)}{|S_3-I|}=\frac{3}{4}$
>Since $S_3$ has minimum value, the elements of $S_3$ is added to $I$, $I$ becomes $\{1,4,3,2\}$.
>
>Second iteration:
>$I=\{1,4,3,2\}$
>The cost of $S_1$: $\frac{Cost(S_1)}{|S_1-I|}=\frac{5}{0}$
>The cost of $S_2$: $\frac{Cost(S_2)}{|S_2-I|}=\frac{10}{1}$
>Since $S_2$ has minimum value, the elements of $S_2$ is added to $I$, $I$ becomes $\{1,4,3,2,5\}$.


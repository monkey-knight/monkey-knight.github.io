---
layout: article
title: P、NP、NP-Complete and NP-Hard
permalink: /_posts/algorithms-and-data-structure/algorithms/2019-09-10-P-NP-NP-hard-NP-complete
tags: Algorithms
aside:
  toc: true
sidebar:
  nav: Algorithms
---

<!--more-->

## 多项式时间复杂度

> 概念1：解决问题需要的时间与问题的规模之间关系是多项式关系。

多项式关系形如 $O(n^k)$，其中 $k$ 为常数，$n$ 是问题的规模。例如，$O(nlog(n))$，$O(n^3)$ 都是多项式时间复杂度。而 $O(n^{log(n)})$，$O(2^n)$ 是指数时间复杂度。$O(n!)$ 是阶乘时间复杂度。

## `P` 问题

`P` 问题，即多项式问题（`Polynomial Problem`）。

> 概念 2：在多项式时间内可解的问题为多项式问题。

例如，时间复杂度为 $O(nlog(n))$ 的快速排序和堆排序，$O(n^2)$ 的冒泡排序和直接选择排序算法都是P问题。

## NP 问题

`NP` 问题，即非确定性多项式问题（`Non-deterministic Polynomial Problem`）

> 概念 3：只能通过验证给定的猜测是否正确来求解的问题为非确定性多项式问题。

**非确定性**指的是问题只能通过验证猜测来求解，而不能够直接求解；**多项式**指的是验证猜测可在多项式时间内完成。

例如，`Hamilton` 回路是 `NP` 问题，因为验证一条路是否恰好经过了每一个顶点可在多项式时间内完成，但是找出一个 `Hamilton` 回路却要穷举所有可能性，不能直接求解。

## NP-Complete 问题

### 归约

为了说明 `NP-Complete` 问题，我们先引入一个概念：归约（`Reducibility`）。

> 概念 4：如果能找到一个变化法则，对任意一个程序 `A` 的输入，都能按这个法则变换成程序 `B` 的输入，使两程序的输出相同，那么我们说，问题 `A` 可归约为问题 `B`，即可以用问题 `B` 的解法解决问题 `A`，或者说，问题 `A` 可以“变成”问题 `B`。

 例如，一元一次方程可以归约为一元二次方程。

### NP-Complete 问题

`NP-Complete` 问题，即非确定性多项式完全问题（`Non-deterministic Polynomial Complete Problem`）。`NP-Complete` 问题是指满足一下两个条件的问题：

- 它是一个 `NP` 问题。
- 所有的 `NP` 问题都可以归约到它。

## NP-Hard 问题

`NP-Hard` 问题，即非确定性多项式难问题（`Non-deterministic Polynomial Hard Problem` ）。它满足 `NP-Complete` 问题的第二条，但不一定满足第一条。
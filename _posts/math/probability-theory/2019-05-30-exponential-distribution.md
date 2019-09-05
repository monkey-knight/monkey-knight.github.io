---
layout: article
title: exponential distribution
permalink: /_posts/math/probability-theory/2019-05-30-exponential-distribution
tags: ProbabilityTheory
aside:
  toc: true
sidebar:
  nav: ProbabilityTheory
---

<!--more-->


原文地址：<https://blog.csdn.net/ccnt_2012/article/details/89875865>



## 馒头卖出之间的时间间隔

在阅读本文之前，需要仔细阅读理解[泊松分布](2019-05-28-poisson-distribution.md)。

基于在[泊松分布](2019-05-28-poisson-distribution.md)中的场景，现在考虑另外一个问题，馒头卖出之间的时间间隔如图：

![image](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/math/probability-theory/assets/12.png)

从图中我们可以看出时间间隔也是随机变量（也就是图中的 $T1、T2、T3、T4 \dots$），不过相对于馒头个数而言，时间间隔时连续的随机变量。如果知道这个时间间隔，老板也好调整自己的服务员人数（时间间隔短，那么需要的服务人员就多，反之需要的就少），优化成本结构。那时间间隔服从什么分布？

假如某一天没有卖出馒头，比如说周三吧，这意味着，周二最后卖出的馒头，和周四最早卖出的馒头中间至少间隔了一天：

![image](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/math/probability-theory/assets/13.png)

当然也可能运气不好，周二也没有卖出馒头。那么卖出两个馒头的时间间隔就隔了两天，但无论如何时间间隔都是大于一天的：

![image](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/math/probability-theory/assets/14.png)

而某一天没有卖出馒头的概率可以由泊松分布得出：

$$
P(x=0)=\frac{\lambda^0}{0!}e^{-\lambda}=e^{-\lambda}
$$

根据上面的分析，卖出两个馒头之间的时间间隔要大于一天，那么必然要包含没有卖出馒头的这天，所以两者的概率是相等的。如果假设随机变量 $Y$ 为卖出两个馒头之间的时间间隔。那么就有：

$$
P(Y>1)=P(X=0)=e^{-\lambda}
$$



## 泊松过程

之前讲的泊松分布只告诉了我们每天买出的馒头数。稍微扩展之后得到新的函数，即泊松过程：

$$
P(X=k,t)=\frac{(\lambda t)^k}{k!}e^{-\lambda t}
$$

通过泊松过程就可以知道不同时间段内卖出的馒头数的分布（$t=1$ 时是泊松分布）：

![image](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/math/probability-theory/assets/1559184118882.png)




## 指数分布

两次卖出馒头之间的时间间隔大于 $t$ 的概率，根据之前的分析，等价于 $t$ 时间段内没有卖出一个馒头的概率，而后者的概率可以由泊松过程给出。所以有：

$$
P(Y>t)=P(X=0,t)=\frac{(\lambda t)^0}{0!}e^{-\lambda t}=e^{-\lambda t}, t \ge 0
$$

进而有：

$$
P(Y \le t)=1-P(Y > t)=1-e^{-\lambda t}
$$

这其实已经得到了 $Y$ 的累积分布函数了：

$$
F(y)=P(Y \le t)=\left\{\begin{matrix}
1-e^{-\lambda t}, & t \ge 0\\ 
0 & t \lt 0
\end{matrix}\right.
$$

对其求导就能得到概率密度函数：

$$
p(y)=\left\{\begin{matrix}
\lambda e^{-\lambda t}, & t \ge 0\\ 
0 & t \lt 0
\end{matrix}\right.
$$

这就是卖出馒头的时间间隔 $Y$ 的概率密度函数，也称为指数分布。


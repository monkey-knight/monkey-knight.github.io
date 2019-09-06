---
layout: article
title: Minimizing probing cost and achieving identifiability in probe-based network link monitoring
permalink: /_posts/computer-network/network-diagnosis/2019-09-05-minimizing-probing-cost-and-achieving-identifiability-in-probe-based-network-link-monitoring
tags: NetworkDiagnosis
aside:
  toc: true
sidebar:
  nav: NetworkDiagnosis
---

<!--more-->

## 介绍

**motivation of network monitoring and performance inference**：

随着网络的不断发展，监控网络的性能和鲁棒性变得越来越重要。服务提供商需要追踪网络以确保其服务水平，此外，对网络性能非常敏感的应用程序（如，`VoIP`，`IPTV`，在线交易）也需要知道网络的状态（如，`loss rate`，`jitter`, `link delay`）。这些需求也就推动了网络监控和网络性能推断的研究。

**advantages of tomography-based end-to-end probe**：

- 与基于简单网络管理协议（`Simple Network Management Protocol, SNMP`）的投票不同，端到端探测不需要在路由器上运行代理。
- 直接测量非协作管理域的网络链路的性能是很难实现的，但是端到端测量却很擅长。

- 与 `ping` 和 `traceroute` 等基于应答的探测相比，端到端探测使用正常的数据包，因此不存在被中间路由器忽略或被防火墙阻塞的问题。

**selection of probing path**：

选择探测路径是基于探测的网络链路监控的主要问题。通常，我们需要考虑两个重要的点：`minimizing probing cost` 和 `achieving identifiability`。

`probing cost` 主要定义为探测路径的数量。它也可以是用于探测的端系统的数量。

一条探测路径可能包含多条链路，探测得到整条路径的性能，却不能够推断出其中链路的性能。为了能够唯一的推断出一条链路的性能，需要多个探测一起协作。

**classification of network links**：

网络链路可以分为两类。如果通过一组探测能够唯一地推断出一条链路的性能，那么此链路就是 `identifiable`，否则此链路就是 `unidentifiable`。如果探测路径选择的不好，可能本为可识别的链路最终都不能够唯一的推断其性能。

## 准备工作

### System Model and Problem Description

将网络建模成一个连通的无向图 $G(V, E)$，其中 $V$ 表示节点（`routers`）集合，$E=\{e_i|1 \le i \le m\}$ 表示边（路由间的通信链路）集合。

在网络中，有 $n$ 个探测路径 $P=\{p_i|1 \le i \le n\}$，它们是用来监控 $m_t$ 个目标链路 $E_t \in E$。为了简单，目标链路被标记为 $e_1, \dots, e_{m_t}$。

> 定义1. 给定一个网络 $G$ ，一个探测路径集合 $P$ ，和一个目标链路集合 $E_t$，目标就是从集合 $P$ 中选择最少量的探测路径，使得所有的可识别的目标链路能够被唯一确定，所有不可识别的目标链路能够被覆盖。

### Linear System Model

对于满足加性度量的链路性能，探测路径和链路的关系可以自然的建模成一个线性系统 $LS=\{ls_i | 1 \le i \le n\}$，其中 $ls_i$ 是第 $i$ 个线性方程如公式（1）。$a_{ij}$ 是一个二进制变量，如果探测路径 $p_i$ 覆盖了链路 $e_j$，那么其值就为 $1$；否则其值为 $0$。变量 $x_j$ 和 $b_i$ 分别表示链路 $e_j$ 和 探测路径$p_i$ 的性能。因此，公式（1）意味着 $p_i$ 的性能是所有在 $p_i$ 上的链路的性能的总和。
$$
\sum_{j=0}^{m}a_{ij}x_j=b_i
$$

这个线性方程组可以被改写成矩阵的形式，如公式（2）。变量 $\textbf{x}$ 是一个向量 $[x_1, x_2, \dots, x_m]^T$。变量 $\textbf{b}$ 是一个向量 $[b_1, b_2, \dots, b_n] ^T$。矩阵 $\textbf{A}$ 叫做依赖矩阵。 
$$
\textbf{A} \textbf{x}=\textbf{b}
$$
![image](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/computer-network/network-diagnosis/assets/1.png)

<center>fig.1, a simple of network</center>
上图中的网络有六个探测路径和五条链路。因此，线性方程组有六个等式和五个变量 $x_1, x_2, \dots, x_5$ 如 fig.2。

<img src="https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/computer-network/network-diagnosis/assets//2.png" alt="image" style="zoom:60%;" />

<center>fig.2, 线性方程组</center>
<img src="https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/computer-network/network-diagnosis/assets//3.png" alt="image" style="zoom:60%;" />

<center>fig.3, 依赖矩阵</center>

## Path Selection Algorithm

### Overview

算法的基本思想是





# <center>CLINK: The Boolean Solution to the Congested IP Link Location Problem: Theory and Practice</center>

**摘要**——像 network tomography 和 traffic matrix estimation 中的其他问题一样， 通过 end-to-end 测量定位拥塞链路需要解一个方程组，这个方程组将测量结果与一个表示链路的状态变量关联起来。在大多数的网络中，这个方程组不具备唯一解。为了解决这个问题，现在的方法都是采用一个不现实的假设：所有链路的先验拥塞概率相同。我们发现这个假设其实不需要，因为**这些概率能够通过利用布尔代数性质的一小组测量而唯一识别**。然后，我们可以将这些学到的概率作为先验，从而在任何时候都能够快速的找到拥塞的链路。与现有算法相比，这个算法准确度提高了一个数量级。我们通过在 Planetlab 网络中的仿真和实际实现来验证我们的结果。



## Introduction



## Related Work

根据 end-to-end 测量从而推断网络内部链路特性的方法叫做 network tomography。它需要解一个方程组，这个方程组通过线性代数或者布尔代数将 end-to-end 测量同链路特性联系起来（inversion problem）。大多数的 end-to-end tomography 方法分为两类：（1）在多播环境中，需要**探测包之间的强时间相关性**来解决线性代数的 inversion problem。（[The use of end-to-end multicast measurements for characterizing internal netowrk behavior]()、[Internet tomography]()、[Network tomography on general topologies]()）（2）使用**网络中拥塞链路的分布**来解决布尔代数的 inversion problem。（[Server-based inference of internet performance]()、[SCFS: Network tomography of binary netowrk performance characteristics]()、[Practical passive lossy network inference]()）

第一类中的方法 [The use of end-to-end multicast measurements for characterizing internal netowrk behavior]()、[Network tomography on general topologies]() 使用多播探测包来推断网络链路的 loss rate。因为多播在网络中没有广泛应用，[Internet tomography]() 使用单播包簇来模拟这个方法。这些方法准确率低而且需要大量的开发和管理费用。此外，这些方法对于实时应用来计算链路 loss rate 的代价昂贵。

第二类中的方法仅仅使用不相关的 end-to-end 测量来识别拥塞链路。这些方法通过找到能够解释测量结果的最小的一组链路来实现这个目的。它们有两个假设：

- 所有的链路拥有相同的先验拥塞概率。使用 $p_0$ 表示。
- $p_0$ 很小：在 [Server-based inference of internet performance]()、[SCFS: Network tomography of binary netowrk performance characteristics]() 中 $p_0$ 小于 $0.2$。

<font color='red'>第一个假设在真实的网络中是不现实的</font>。网络是异构的环境，链路拥有不同的拥塞概率。例如：backbone links 的拥塞概率要比 access links 的拥塞概率小。这样假设可能导致不准确的诊断。[SCFS: Network tomography of binary netowrk performance characteristics]() 一文中，当 $p_0$ 很大的时候，其 detection rate（拥塞链路被正确检测的百分比）只有 $30\%$。



## The Network and Performance Model



## VI. Using the Prior to Identify Congested Links

#### A. Problem Definition

先验概率提供了有用的网络信息，可以被用到很多应用中。其中一个应用就是结合先验概率和最新的测量来定位拥塞链路（而不简单是链路的拥塞概率）。

首先详细描述 CLINK（Congested Link Identification）问题。对于 CLINK 问题给出如下信息：

- 路由矩阵 $D$；
- 一个测量结果（messured snapshot）$\overrightarrow{y} = [y_1 \, y_2  \dots \, y_{n_p}]^T$  
- 先验链路状态概率 $\overrightarrow{p}$

然后我就需要求解公式 $y_i = \bigvee_{k=1}^{n_c}x_kD_{ik}$ 来得到 $\overrightarrow{x} = [x_1 \, x_2 \dots x_{n_c}]$ 。由于此公式有多个解，所以我们需要找到最可能的解。换句话说，我们希望找到一个向量 $\overrightarrow{x}$ （当 $x_k = 1$ 时要确实是拥塞的）来最大化如下条件概率：

$$
\underset{x}{argmax}\, \mathbb{p}_{\overrightarrow{p}}\{X = \overrightarrow{x} \,|\, Y = \overrightarrow{y}\}
$$

上述公式的解是所有拥塞链路集合最大后验（Maximum A-Posteriori, MAP）估计。

根据贝叶斯公式法则：

$$
\mathbb{p}_{\overrightarrow{p}}\{X = \overrightarrow{x} \,|\, Y = \overrightarrow{y}\} = \frac{\mathbb{p}_{\overrightarrow{p}}\{Y = \overrightarrow{y}\ \,|\, X = \overrightarrow{x}\} \, \mathbb{p}_{\overrightarrow{p}} \{X = \overrightarrow{x}\}}{\mathbb{p}_{\overrightarrow{p}} \{Y = \overrightarrow{y}\}}
$$

而且 $\mathbb{p}_{\overrightarrow{p}} \{Y = \overrightarrow{y}\}$ 只依赖与网络的状况和我们的测量结果，所以我们的最终目标可以等价于：

$$
\underset{x}{argmax} \, \mathbb{p}_{\overrightarrow{p}}\{Y = \overrightarrow{y}\ \,|\, X = \overrightarrow{x}\} \, \mathbb{p}_{\overrightarrow{p}} \{X = \overrightarrow{x}\}
$$
因为链路状态 $X_k$ 是独立随机变量，所以：
$$
\mathbb{p}_{\overrightarrow{p}} \{X = \overrightarrow{x}\} = \prod_{k=1}^{n_c} p_k^{x_k} (1-p_k)^{(1-x_k)}
$$
对于任意一条路径 $P_i$ ，给定 $X = \overrightarrow{x}$ ，要使 $Y_i = 0$ 当且仅当所有的 $x_k = 0, \, 0 \le k \le n_c $ ，即 $D_{ik}x_k = 0$ 或者 $(1 - D_{ik})^{x_k} = 1$。所以，条件概率
$$
\mathbb{p}_{\overrightarrow{p}}\{Y_i = 0\ \,|\, X = \overrightarrow{x}\} = \prod_{k=1}^{n_c}(1-D_{ik})^{x_k}
$$
和
$$
\mathbb{p}_{\overrightarrow{p}}\{Y_i = 1\ \,|\, X = \overrightarrow{x}\} = 1- \mathbb{p}_{\overrightarrow{p}}\{Y_i = 0\ \,|\, X = \overrightarrow{x}\}
$$
不是 $0$ 就是 $1$ 。

我们定义 $P_G$ 表示不拥塞路径的集合，$P_C$ 表示拥塞路劲的集合。所以，我们得到：
$$
\mathbb{p}_{\overrightarrow{p}}\{Y = \overrightarrow{y}\ \,|\, X = \overrightarrow{x}\} = \prod_{P_i \in P_G}\mathbb{p}_{\overrightarrow{p}}\{Y_i = 0\ \,|\, X = \overrightarrow{x}\} \prod_{P_i \in P_C}\mathbb{p}_{\overrightarrow{p}}\{Y_i = 1 \,|\, X = \overrightarrow{x}\}
$$

我们会发现这个概率的结果也是非 $0$ 即 $1$。

最终，由于公式 $\underset{x}{argmax} \, \mathbb{p}_{\overrightarrow{p}}\{Y = \overrightarrow{y}\ \,|\, X = \overrightarrow{x}\} \, \mathbb{p}_{\overrightarrow{p}} \{X = \overrightarrow{x}\}$ 的参数不为 $0$，所以此公式的解必须满足如下两个条件：（1）对于任意拥塞路劲，至少包含一条拥塞链路。（2）对于不拥塞路劲，其所有链路都不拥塞。

根据这个观测，我们就能够显著的简化 CLINK 问题。将路由矩阵 $D$ 去掉行（这些行表示不拥塞的路劲）和列（这些列表示链路属于一个不拥塞的路劲）得到一个新的路由矩阵 $R$。这样 $R$ 的每一行都表示一个拥塞路劲，每一列表示一条链路属于至少一条拥塞路劲。我们用 $\varepsilon_R $ 表示 $R$ 所有列代表的链路的集合。所以 $R$ 的维度就是 $P_C \times \varepsilon_R $。所以 CLINK 问题就变成了找到一个链路的集合 $L \in \varepsilon_R$，使得这个集合能够解释所有路劲的拥塞。所以：

$$
\underset{L \in \varepsilon_R}{argmax} P_{\overrightarrow{p}}(L) = \underset{L \in \varepsilon_R}{argmax} \prod_{k=1}^{|\varepsilon_R|}p_k^{x_k}(1-p_k)^{(1-x_k)}
$$
去掉上述公式中不依赖与 $L$ 的项，我们能够得到：
$$
\begin{align*}
\underset{L \in \varepsilon_R}{argmax} P_{\overrightarrow{p}}(L) &= \underset{L \in \varepsilon_R}{argmax} \sum_{k=1}^{|\varepsilon_R|}x_klog\frac{p_k}{1-p_k} \\ 
 &= \underset{L \in \varepsilon_R}{argmin} \sum_{k=1}^{|\varepsilon_R|}x_klog\frac{1- p_k}{p_k}
\end{align*}
$$


#### B. The Inference Algorithms

上述的优化问题其实就是带权重的集合覆盖问题（The Weighted Set Cover Problem, WSCP），是一个众所周知的 NP-Complete 问题。有大量的优化算法来解决带权重的集合覆盖问题，典型的是基于树搜索过程。这些算法中的大多数需要大量的计算时间。所以我们选择了一种能够产生高质量解的有效的启发式算法。我们定义链路 $e_k$ 的域为 $Domain(e_k), e_k \in \varepsilon_C$ ，表示所有包含此链路的路劲的集合。该算法使用贪婪的启发式方法，通过一系列步骤构造可行的解集，每一步都是选择一个链路，来最小化公式 $log((1-p_k) / p_k) / |Domain(e_k)|$。 
# <center>几种重要的分布</center>



## 0-1 分布

**0-1 分布**，又叫做 **$1$ 重伯努利（Bernoulli）试验**。记为 $X \sim B(1, p)$

一个事件 $A$ 要么发生，要么不发生，不存在其他情况。$A$ 发生的概率为 $p$，则不发生的概率就为 $1-p$。
$$
\begin{bmatrix}
X & 1 & 0\\ 
P_x & p & 1-p
\end{bmatrix}
$$


#### 0-1 分布数学期望

$$
\begin{align*}
E(X) &= 1 \times p + 0 \times (1-p) \\ 
 &= p
\end{align*}
$$

#### 0-1 分布方差

$$
\begin{align*}
D(X) &= E(X^2) - (E(X))^2\\ 
 &= 1^2 \times p + 0^2 \times (1-p)^2 - p^2 \\
 &= p(1-p)
\end{align*}
$$



## 二项分布

**二项分布**，又叫做 **$n$ 重伯努利（Bernoulli）试验**。记为 $X \sim B(n, p)$

- 每次试验只有两个结果，事件要么发生，要么不发生。
- 每次试验事件发生的概率为 $p$，事件不发生的概率 $1-p$。
- 每次试验相互独立。

$$
P(X=k)=C_n^kp^k(1-p)^{n-k}, (k=0,1,\dots,n)
$$



#### 二项分布数学期望

#### 二项分布方差

#### Probability Mass Function

![1558752047279](assets/1558752047279.png)

#### Cumulative Distribution Function

![1558754798671](assets/1558754798671.png)

## 几何分布

$$
P(X=k)=p(1-p)^{k-1}
$$





## 超几何分布

## 泊松分布

泊松分布（Poisson Distribution），记为 $X \sim P(\lambda)$。

如果还不了解泊松分布，强烈建议阅读文章：[泊松分布](./poisson_distribution.md)。

泊松分布的表达式：

$$
P(X=k)=\frac{\lambda^k}{k!}e^{-\lambda}, (k=1,2, \dots)
$$

#### Probability Mass Function

![1559048079277](assets/1559048079277.png)

#### Cumulative Distribution Function

![1559048537576](assets/1559048537576.png)

## 均匀分布

## 指数分布





## 正太分布





## Beta 分布

如果不了解 Beta 分布，强烈建立阅读文章：[Beta 分布](./beta_distribution.md)

Beta 分布的概率密度函数：
$$
f(x;\alpha, \beta) = \frac{1}{B(\alpha, \beta)}x^{a-1}(1-x)^{\beta-1}
$$


# `simpy` 基础

此文档描述了 `simpy` 的一些基本概念：它如何工作？processes、events 和 environment 分别是什么？我们能用它们作什么？

## `simpy` 如何工作？

如果你仔细分析 `simpy`，它其实就是一个异步事件的调度器（asynchronous event dispatcher）。你生成一些 events ，然后按照给定的仿真时间来调度它们。events 按照优先级，仿真时间和上升的事件 id进行排序。一个事件也有回调列表，当这个事件被事件循环触发和处理时，这些回调就会被执行。事件可能也有返回值。

这其中涉及的组件是你编写的环境、事件和处理函数。

处理函数实现你的仿真模型，也就是，它们定义了你的仿真的行为。他们是产生 `event` 实例的 `python` 生成器函数。

`environment` 将这些事件存储在事件列表中而且追踪当前的仿真时间。

当一个处理函数产生一个事件，`simpy` 会将此进程加入到事件的回调中而且将其挂起直到这个事件被触发和处理。

下面的一个非常简单的例子解释了所有的这些：

```python
>>> import simpy
>>>
>>> def example(env):
...     event = simpy.events.Timeout(env, delay=1, value=42)
...     value = yield event
...     print('now=%d, value=%d' % (env.now, value))
>>>
>>> env = simpy.Environment()
>>> example_gen = example(env)
>>> p = simpy.events.Process(env, example_gen)
>>>
>>> env.run()
now=1, value=42
```

上面的 `example()` 处理函数首先创建了一个 `Timeout` 事件。将 `environment` 、`delay`  和 `value` 传递给事件。这个 `Timeout` 事件就会将自己安排在 `now + delay`（这也就是为什么需要 `environment`）； 其他的事件类型经常将它们自己安排在当前仿真时间。

处理函数然后产生这个事件并且挂起。当 `simpy` 进程处理这个 `Timeout` 事件时，它就会被恢复。处理函数也接收事件的值（42）——可是，这个是可选项，如果你对这个值不感兴趣或者事件本身就没有值，`yield event` 也是没有问题的。

最后，处理函数打印出当前的仿真时间（仿真时间可以通过 `environment` 的 `now` 属性获得）和 `Timeout` 事件的值。

如果定义了所有需要的处理函数，在你的仿真环境中你可以实例化所有对象。在大多数情况下，你首先都会创建一个 `Environment` 的实例，因为在创建其它任何的一切事物时都需要将其进行传递。

开始一个处理函数包含两件事：

1. 你必须调用处理函数来创建一个生成器对象。（但是这并不会执行这个函数的任何代码，至于为什么，你可以学习 `python` 的关键字 `yield`）。
2. 然后创建一个 `Process` 实例而且将 `Environment` 和 生成器对象传递给它。这将安排一个初始化事件在当前仿真时间，这是处理函数开始执行的时间。这个进程实例也是一个事件，它会在处理函数返回时被触发。[guide to events](https://simpy.readthedocs.io/en/latest/topical_guides/events.html) 解释了为什么这个很方便。

最后，你就可以开始 `simpy` 的事件循环了。默认情况下，只要事件队列中有事件，事件循环都会执行，但是你也可以通过提供一个 `util` 参数（见 [simulation control](https://simpy.readthedocs.io/en/latest/topical_guides/environments.html#simulation-control)）

上面代码的精简版：

```python
>>> import simpy
>>>
>>> def example(env):
...     value = yield env.timeout(1, value=42)
...     print('now=%d, value=%d' % (env.now, value))
>>>
>>> env = simpy.Environment()
>>> p = env.process(example(env))
>>> env.run()
now=1, value=42
```


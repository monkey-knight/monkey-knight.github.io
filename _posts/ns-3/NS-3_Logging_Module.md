# NS-3 Logging Module

### Logging Overview

如果想要将模型的数据导出——使用“**Tracing**”。

如果想要获取调试信息，警告，错误信息或者想要在任何时候都能够很容易的获得一个快速的信息——使用“**Logging**”。

日志消息被分成了七个等级，按照升序排序为：

- LOG_ERROR——错误信息
- LOG_WARN——警告信息
- LOG_DEBUG——调试信息
- LOG_INFO——通知消息
- LOG_FUNCTION——函数调用的消息（两个相关的宏：NS_LOG_FUNCTION 用于成员函数；NS_LOG_FUNCTION_NOARGS 用于静态函数）
- LOG_LOGIC——函数的内部的逻辑流消息（相关的宏：NS_LOG_LOGIC）
- LOG_ALL——上述所有的消息

还提供了一个始终显示的无条件日志宏，不管日志级别或组件选择如何。

- NS_LOG_UNCOND



### Enabling Logging

在脚本中实现日志打印可以使用

```c++
LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO);
```

也可以通过 NS_LOG 环境变量来修改日志打印的等级

```shell
export 'NS_LOG=UdpEchoClientApplication=level_all'
```

注意：上述`UdpEchoClientApplication`并不是类名而是日志组件名。

在有些情况下，可能不能够确定是那个方法生成了日志消息，可以通过想`NS_LOG`环境变量添加`prefix_func`等级来解决这个问题。如：

```shell
export 'NS_LOG=UdpEchoClientApplication=level_all|prefix_func'
```

有时候能够观看到日志生成模拟器时间也是相当有用的，可以通过向`NS_LOG`环境变量添加`prefix_time`来实现，如：

```shell
export 'NS_LOG=UdpEchoClientApplication=level_all|prefix_func|prefix_time'
```

也可以通过一个简单的方式开启所有的日志组件。如：

```shell
export 'NS_LOG=*=level_all|prefix_func|prefix_time'
```

### Adding Logging to your Code

在脚本中定义一个日志组件的方式如下：

```c++
NS_LOG_COMPONENT_DEFINE("FirstSriptExample");
```

在脚本中通过宏来添加日志信息，如：

```c++
NS_LOG_INFO("Logging Message");
```

通过上一节我们就已经知道如何打印出这条日志信息，操作如下：

```shell
export 'NS_LOG=FirstScriptExample=info'
```


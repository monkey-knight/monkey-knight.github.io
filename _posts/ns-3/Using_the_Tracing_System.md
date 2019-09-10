# Using the Tracing System

模拟的目标就是能够产生输出用于之后的研究，NS-3的`Tracing`系统就是实现此功能的主要机制。

### ASCII Tracing

如果想要脚本能够输出`ASCII Tracing`输出，需要在脚本的`Simulator::run()`方法之前添加如下几行代码：

```c++
AsciiTraceHelper ascii;
pointToPoint.EnableAsciiAll(ascii.CreateFileStream("myfirst.tr"));
```

`pointToPoint.EnableAsciiAii()`方法希望告诉`helper`对启用所有的`point-to-point`设备的`ascii`追踪；并且希望`trace sinks`以`ascii`的格式写出包移动的信息。

在以`ascii`格式输出的文件中，每一行都对应一个追踪事件。每一行都由一个单个字符开始，这些字符的含义如下：

- +：发生在设备队列上的入队列操作
- -：发生在设备队列上的出队列操作
- d：表示一个包被丢弃，典型的原因是由于队列已满
- r：表示一个包被网络设备接受

### PCAP Tracing

NS-3也能够创建一种`.pcap`格式的追踪文件。`.pcap`就是一种抓包格式，最出名的能够读取和展示这种包格式的程序就是`Wireshark`。

开启`pcap`追踪的代码只有一行：

```c++
pointToPoint.EnablePcapAll("myfirst");
```

在这里传入了一个`myfirst`字符串，但是这个字符串并不是一个完整的文件名，而只是一个前缀，完整的文件名还会加上节点编号和设备编号，然后以`.pcap`结尾。

生产文件之后，我们现在就可以通过`tcpdump`来读取这些`pcap`格式的文件了。


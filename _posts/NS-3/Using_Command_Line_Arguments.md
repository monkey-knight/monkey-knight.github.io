# Using Command Line Arguments

### Overriding Default Attributes

另一种不用编辑和构建就可以更改NS-3脚本行为的方法是通过命令行参数。我们提供了一种机制来解析命令行参数，并根据这些参数自动设置局部和全局变量。

命令行的简单使用方法如下：

```c++
int main(int argc, char *argv[]){
    CommandLine cmd;
    cmd.Parse(argc,argv);
}
```

上面的两行代码非常有用，它能够开启 ns-3 全局变量和属性系统的大门。

首先我们可以从命令行的 help 来开启命令行使用之旅。使用示例如下：

```shell
./waf --run "scratch/myfirst --PrintHelp"
```

上面的命令的输出结果如下：

```shell
CommandLine:HandleArgument(): Handle arg name=PrintHelp value=
--PrintHelp: Print this help message. 
--PrintGroups: Print the list of groups. 
--PrintTypeIds: Print all TypeIds.
--PrintGroup=[group]: Print all TypeIds of group. 
--PrintAttributes=[typeid]: Print all attributes of typeid.
--PrintGlobals: Print the list of globals.
```

我们仔细来研究一下`--PrintAttributes`，它会根据`typeid`来打印相关的所有的属性。但是我们需要提供`typeid`，其实`typeid`和类名是一一对应的。示例如下：

```shell
./waf --run "scratch/myfirst --PrintAttributes=ns3::PointToPointNetDevice"
```

还可以通过命令行的方式来修改类的变量，实现如下：

```shell
./waf --run "scratch/myfirst --ns3::PointToPointNetDevice::DataRate=5Mbps"
```

如果你选择`--PrintGroups`参数，你能够看到所有注册的`typeid`组的列表，组名与源目录中的模块名对齐（尽管以大写字母开头）。但是打印出所有的信息的话就太大了，所以我们可以`--PrintGroup`输出某一个组的信息，打印出该组的`typeid`列表。

### Hooking Your Own Values

我们可以通过`CommandLine`的`AddValue()`方法来添加自己的`hook`，例如：

```c++
int main(int argc, char* argv[]){
    uint32_t nPackets = 1;
    
	CommandLine cmd;
    cmd.AddValue("nPackets", "Number of packets to echo", nPackets); 
    cmd.Parse (argc, argv);
}
```

然后我们就能够通过`--PringHelp`来打印出我们自己添加的`hook`。
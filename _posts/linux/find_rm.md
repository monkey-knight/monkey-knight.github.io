# find 命令与 rm 结合批量删除文件

`find` 命令的具体细节请看[链接]()。

例如，如果我需要删除目录 `/test/` 下有`b2b_*.tr` 性质的文件可以使用如下命令来实现：

```shell
find /test/ -name　"b2b_*.tr" | xargs rm
```

或者

```shell
rm `find /test/ -name　"b2b_*.tr"`
```

但是强烈推荐使用第一种用法，因为`xargs`可以解决多参数问题。




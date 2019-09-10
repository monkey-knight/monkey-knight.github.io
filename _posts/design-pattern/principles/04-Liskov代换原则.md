# <center>$Liskov$ 代换原则</center>

$Liskov$ 代换原则(Liskov Substitution Principle LSP)表示，任何基类可以出现的地方，子类一定可以出现。<font color=red>$Liskov$ 代换原则是对**开放封闭原则**的补充。实现**开放封闭原则**的关键步骤就是抽象化。而基类与子类的继承关系就是抽象化的具体实现，所以里氏代换原则是对实现抽象化的具体步骤的规范。</font>

简单的理解为一个软件实体如果使用的是一个父类，那么一定适用于其子类，而且它察觉不出父类对象和子类对象的区别。也就是说，软件里面，把父类都替换成它的子类，程序的行为没有变化。但是反过来的代换却不成立。

## 举例说明

首先创建一个 `Person` 类

```java
public class Person {
    public void display() {
        System.out.println("this is person");
    }
}
```

再创建一个 `Man` 类，继承这个 `Person` 类

```java
public class Man extends Person {

    public void display() {
        System.out.println("this is man");
    }
    
}
```

运行程序

```java
public class Test {
    public static void main(String[] args) {
        Person person = new Person();//new 一个Person实例
        display(person);
        
        Person man = new Man();//new 一个Man实例
        display(man);
    }
    
    public static void display(Person person) {
        person.display();
    }
}
```

运行结果

```java
this is person
this is man
```

运行没有影响，符合**一个软件实体如果使用的是一个父类的话，那么一定适用于其子类，而且它察觉不出父类和子类对象的区别**这句概念，这也就是 `java` 中的**多态**。


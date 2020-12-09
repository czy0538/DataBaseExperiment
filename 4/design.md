<img src="https://cdn.jsdelivr.net/gh/czy0538/photoBed/20201208201955.png" alt="界面设计" style="zoom:75%;" />



## 基本操作逻辑：

- 上方区域负责输入，选择框后在其后部加入相应数据并进行相应的查询


## 基本程序逻辑

- InputMessage：处理用户输入，为一个list，每个lineEdit对应一个

- isSelected:bool list,判断是否选中

- OutputMessage：存储需要显示的信息

  功能选择和表选择共同组合，封装成函数，使用其值的组合使用switch进行调用相关的函数

## 类

- 界面类
- 数据库类：封装各种对于查询的处理
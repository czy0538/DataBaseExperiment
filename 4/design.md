<img src="https://cdn.jsdelivr.net/gh/czy0538/photoBed/20201208201955.png" alt="界面设计" style="zoom:75%;" />



## 基本操作逻辑：

- 上方区域负责输入，选择框后在其后部加入相应数据并进行相应的查询


## 变量

- lineEditMessage：处理用户输入，为一个list，每个lineEdit对应一个

- isSelected:bool：list,判断是否选中，序号如lineEditMessage对应

  对应关系如图：

  <img src="https://cdn.jsdelivr.net/gh/czy0538/photoBed/20201213152754.png" alt="image-20201213152753956" style="zoom:50%;" />

- OutputMessage：存储需要显示的信息

- display_item：string：为select子句的内容

- condition_item：string，为where子句内容

- table_item：为from子句内容,现阶段把所有的表都选出来

- table_selected：bool list，0为S,1为SC，2为C，选中为True，否则False

  功能选择和表选择共同组合，封装成函数，使用其值的组合使用switch进行调用相关的函数

## 类

- 界面类
- 数据库类：封装各种对于查询的处理

## 查询

查询功能较为完善，支持基本查询，不支持分组查询等

## 删除

仅支持单表删除
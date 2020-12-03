create view V_NUM_AVG
as
select sdept,COUNT(sname) '系学生数',AVG(convert(int ,sage)) '平均年龄'
from S
group by sdept
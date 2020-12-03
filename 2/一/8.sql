select cno,AVG(grade) avg_grade
from SC
where sclass=1 and cno=3
group by cno
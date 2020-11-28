select s.sname,s.ssex,sc.grade
from s,sc
where sc.cno=1 and s.sno=sc.sno and s.sclass=sc.sclass
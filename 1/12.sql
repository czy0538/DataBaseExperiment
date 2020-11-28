select s.sclass,s.sno,s.sname,c.cname,grade
from s,c,sc
where sc.cno=1 and sc.sno=s.sno and sc.sclass =s.sclass and c.cno=1
order by grade desc;
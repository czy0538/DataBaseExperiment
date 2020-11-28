select s.sclass,s.sno,sname,ssex,sage,sdept,sc.cno,grade
from s ,sc,c
where s.sclass=2 and s.sclass=sc.sclass and s.sno = sc.sno and c.cno=sc.cno and c.cpno=1
select s.sclass,s.sno,sname,ssex,sage,sdept,c.cno,cname,cpno,ccredit,grade
from S,SC,C
where s.sno=sc.sno and s.sclass=sc.sclass and sc.cno=c.cno;
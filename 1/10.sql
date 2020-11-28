select s.sclass,s.sno,sname,ssex,sage,sdept,grade
from s 
left outer join sc
ON s.sno=sc.sno and s.sno=sc.sno and s.sclass=sc.sclass 
left join c
ON sc.cno=c.cno
where s.sclass=2 and s.ssex='Ů';
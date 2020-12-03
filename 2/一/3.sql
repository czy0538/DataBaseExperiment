select s.sclass,s.sno,sname,ssex,sdept,cno,grade
from s,sc scx
where s.sclass=1 and  scx.sclass=1 and scx.sno=s.sno
	  and scx.sno in (select scy.sno
				  from sc scy
				  where scy.sno=scx.sno and scy.sclass=scx.sclass
				  group by scy.sno
				  having AVG(scy.grade)>=85
				  );
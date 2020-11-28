select s.sclass,s.sno,sname
from s,sc
where s.sclass=sc.sclass 
	and s.sno=sc.sno 
	and sc.cno=2
	and grade>=all(select grade from SC where cno=2);

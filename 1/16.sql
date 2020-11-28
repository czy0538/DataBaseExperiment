select sclass,sno
from sc
where grade>(select min(grade)
			  from sc
			  where cno=2)
	  and cno=2;

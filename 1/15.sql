select sclass,sno
from sc
where grade<=all(select grade
				 from sc
				 where cno=2 and sclass=1
				 )
	  and  cno=2 
	  and  sclass=1
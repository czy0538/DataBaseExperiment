select s.sclass,s.sno,s.sname,c.cname,grade
from s,sc scx,c
where 3=(select count(*)
		from  sc scy
		where scy.sno=scx.sno
		and scy.sclass=scx.sclass)
	 and s.sno=scx.sno
	 and s.sclass =scx.sclass
	 and c.cno=scx.cno;
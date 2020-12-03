create view S_C_GRADE
as
select s.sno,s.sclass,s.sname,cname,grade
from (S left join SC on s.sno=sc.sno and s.sclass=sc.sclass)left join C on SC.cno=C.cno;
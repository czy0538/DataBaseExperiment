select sname,grade
from SC,S
where SC.sclass =S.sclass and SC.sno=S.sno and cno=2
order by grade desc
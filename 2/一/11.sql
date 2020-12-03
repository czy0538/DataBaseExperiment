update S
set sage=sage+1
where sname in(select sname
			from SC,s
			where SC.sclass=S.sclass and SC.sno=s.sno and SC.cno=1)
			and ssex='ÄÐ';
select *
from S;
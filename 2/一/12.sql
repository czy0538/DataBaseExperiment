create table AVG_GRADE
	(sno nchar(10),
	 sclass nchar(10),
	 avg_grade int,
	 primary key (sno,sclass));

insert 
into AVG_GRADE
select sno,sclass,AVG(grade)
from SC
group by sno,sclass


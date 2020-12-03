select s.sclass,S.sno,sum(ccredit) 'ังทึ'
from (s left join sc on S.sclass=SC.sclass and S.sno=SC.sno)
	left join C on SC.cno=C.cno
group by s.sclass,s.sno;
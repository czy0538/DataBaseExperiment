create view	V_IS_Score
as 
select SC.sno,SC.sclass
from SC,S
where S.sdept='IS' and SC.cno=1 and grade>90 and SC.sclass=S.sclass and SC.sno=S.sno
create view V_NUM_AVG
as
select sdept,COUNT(sname) 'ϵѧ����',AVG(convert(int ,sage)) 'ƽ������'
from S
group by sdept
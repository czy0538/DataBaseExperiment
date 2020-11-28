select distinct cno, count(*) 'number'
from sc
group by cno;
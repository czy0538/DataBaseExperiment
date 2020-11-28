select distinct sclass,sno
from sc scx
where not exists(select *
				 from sc scy
				 where scy.sno=1 and scy.sclass=2
				       and not exists(select*
									  from sc scz
									  where scz.sno=scx.sno
										    and scz.cno=scy.cno))
	  and (sno!=1 or sclass !=2);

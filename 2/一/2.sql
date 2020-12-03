select sclass,sno
from sc scx
where cno=1 and not exists 
				(select *
				from sc scy
				where scx.sno=scy.sno
					and scx.sclass=scy.sclass
					and cno=2);

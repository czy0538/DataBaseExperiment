select distinct scx.sclass,scx.sno
from s scx
where not exists(select *
			from SC scy
			where scy.cno=1 and exists(
			select *
			from SC scz
			where scz.sno=scx.sno and scz.sclass=scx.sclass
			and scy.sno=scz.sno and scy.sclass=scz.sclass));

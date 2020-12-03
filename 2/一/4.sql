select distinct s.sclass,s.sno,s.sname
from sc scx,s
where not exists
		(select*
		from SC scy
		where scy.sno=2 and scy.sclass=1
		and not exists(select *
						from SC scz
						where scz.sno=scx.sno
						and scz.sclass=scx.sclass
						and scz.cno=scy.cno))
		and scx.sclass=S.sclass
		and scx.sno=S.sno
		and not (scx.sclass=1 and scx.sno=2);
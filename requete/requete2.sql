
select * from pathologie
where id_pathologie in (select id_pathologie from pathologie_specialite group by id_pathologie having count(*)=1)
create or replace function restore_owner_relations() 
returns trigger as $$ 
begin 
    if old.is_deleted = TRUE
    and new.is_deleted = FALSE 
    then
        update owner_to_character
        set is_deleted = FALSE
        where owner_id = new.id;
    end if;
return new;
end;
$$ language plpgsql;
create trigger trigger_restore_user
after
update of is_deleted
on 
    owner 
    for each row 
    execute function restore_owner_relations();
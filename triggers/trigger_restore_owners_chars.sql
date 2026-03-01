create or replace function restore_owner_relations() 
returns trigger as $$ 
begin 
    if OLD.is_deleted = TRUE
    and NEW.is_deleted = FALSE 
    then
        update owner_to_character
        set is_deleted = FALSE
        where owner_id = NEW.id;
    end if;
return NEW;
end;
$$ language plpgsql;
create trigger trigger_restore_user
after
update of is_deleted
on 
    owner 
    for each row 
    execute function restore_owner_relations();
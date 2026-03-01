create or replace function delete_owner_relations() 
returns trigger as $$ 
begin
    if NEW.is_deleted = TRUE
    and (
        OLD.is_deleted = FALSE
        or OLD.is_deleted is null
    ) then
        update owner_to_character
        set is_deleted = TRUE
        where owner_id = NEW.id;
    end if;
return NEW;
end;
$$ LANGUAGE plpgsql;
create trigger trigger_delete_user
after
    update of is_deleted on owner
    for each row 
    execute function delete_owner_relations();
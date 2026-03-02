create or replace function delete_owner_relations() 
returns trigger as $$ 
begin
    if new.is_deleted is
    and (
        old.is_deleted is false
        or old.is_deleted is null
    ) then
        update owner_to_character
        set is_deleted = TRUE
        where owner_id = new.id;
    end if;
return new;
end;
$$ LANGUAGE plpgsql;
create trigger trigger_delete_user
after
    update of is_deleted on owner
    for each row 
    execute function delete_owner_relations();
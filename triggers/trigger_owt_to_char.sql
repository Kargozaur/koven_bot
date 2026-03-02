create or replace function sync_owt_to_ch()
returns trigger as $$
begin
	if (new.is_deleted is true and old.is_deleted is false) then
		update characters
			set is_deleted = true
		where id = new.character_id;
	elseif (new.is_deleted is false and old.is_deleted is true) then
		update characters
			set is_deleted = false
		where id= new.character_id;
	end if;
	return new;
end;
$$ language plpgsql;

create trigger trigger_sync_chars_soft_delete
after update
	of 
		is_deleted on owner_to_character
	for each row
	execute function sync_owt_to_ch();
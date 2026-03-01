create or replace function update_updated_at_column()
returns trigger as $$
begin
	new.updated_at = now();
	return new;
end;
$$ language plpgsql;

create trigger update_character_updated_at
before
update on 
    characters
    for each row
    execute procedure update_updated_at_column();
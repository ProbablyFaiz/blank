#!/usr/bin/env fish

argparse 's/skip-create' -- $argv
or exit 1

if test (count $argv) -ne 2
    echo "Usage: create_api_db_user.fish [--skip-create] <username> <database>"
    exit 1
end

set username $argv[1]
set database $argv[2]

if not set -q _flag_skip_create
    set password (openssl rand -base64 32)
    psql postgres -c "CREATE USER $username WITH PASSWORD '$password';"
end

psql $database -c "GRANT CONNECT ON DATABASE $database to $username;

GRANT USAGE on SCHEMA public to $username;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public to $username;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public to $username;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO $username;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO $username;"

if not set -q _flag_skip_create
    echo "Created user '$username' with password: $password"
else
    echo "Assigned all privileges to user '$username'"
end

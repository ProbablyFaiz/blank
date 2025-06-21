#!/usr/bin/env fish

argparse 's/skip-create' -- $argv
or exit 1

if test (count $argv) -ne 2
    echo "Usage: create_admin_db_user.fish [--skip-create] <username> <database>"
    exit 1
end

set username $argv[1]
set database $argv[2]

if not set -q _flag_skip_create
    set password (openssl rand -base64 32)
    psql postgres -c "CREATE USER $username WITH PASSWORD '$password';"
end

psql $database -c "GRANT CONNECT ON DATABASE $database to $username;

GRANT ALL PRIVILEGES ON SCHEMA public TO $username;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $username;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $username;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO $username;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO $username;

ALTER USER $username BYPASSRLS;"

if not set -q _flag_skip_create
    echo "Created user '$username' with password: $password"
else
    echo "Assigned all privileges to user '$username'"
end

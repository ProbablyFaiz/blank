#!/usr/bin/env python3

import argparse
import subprocess
import sys
import base64
import os


def run_psql(database, command, host=None, port=None, user=None, capture_output=False):
    """Run a psql command."""
    cmd = ["psql", database, "-t", "-c", command]
    if host:
        cmd.extend(["-h", host])
    if port:
        cmd.extend(["-p", str(port)])
    if user:
        cmd.extend(["-U", user])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def user_exists(username, host=None, port=None, pg_user=None):
    """Check if a PostgreSQL user exists."""
    result = run_psql(
        "postgres",
        f"SELECT 1 FROM pg_user WHERE usename = '{username}';",
        host=host,
        port=port,
        user=pg_user,
        capture_output=True,
    )
    return result.returncode == 0 and result.stdout.strip().startswith("1")


def database_exists(database, host=None, port=None, pg_user=None):
    """Check if a PostgreSQL database exists."""
    result = run_psql(
        "postgres",
        f"SELECT 1 FROM pg_database WHERE datname = '{database}';",
        host=host,
        port=port,
        user=pg_user,
        capture_output=True,
    )
    return result.returncode == 0 and result.stdout.strip().startswith("1")


def main():
    parser = argparse.ArgumentParser(description="Create PostgreSQL API user")
    parser.add_argument("username", help="Username to create")
    parser.add_argument("database", help="Database to grant privileges on")
    parser.add_argument(
        "--skip-create",
        "-s",
        action="store_true",
        help="Skip user creation and just assign privileges",
    )
    parser.add_argument(
        "--host",
        "-H",
        help="Database host (default: use psql defaults)",
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        help="Database port (default: use psql defaults)",
    )
    parser.add_argument(
        "--postgres-user",
        "-U",
        help="PostgreSQL user to connect as (default: current system user)",
    )

    args = parser.parse_args()

    # Check if database exists
    if not database_exists(
        args.database, host=args.host, port=args.port, pg_user=args.postgres_user
    ):
        print(f"Error: Database '{args.database}' does not exist")
        sys.exit(1)

    password = None

    # Handle user creation or validation
    if not args.skip_create:
        # Check if user already exists
        if user_exists(
            args.username, host=args.host, port=args.port, pg_user=args.postgres_user
        ):
            print(
                f"Error: User '{args.username}' already exists. Use --skip-create to just assign privileges."
            )
            sys.exit(1)

        # Create user
        print(f"Creating user '{args.username}'...")
        # Generate password with guaranteed complexity (lowercase, uppercase, number, special char)
        password = base64.b64encode(os.urandom(24)).decode("utf-8") + "!1Aa"
        result = run_psql(
            "postgres",
            f"CREATE USER {args.username} WITH PASSWORD '{password}';",
            host=args.host,
            port=args.port,
            user=args.postgres_user,
        )
        if result.returncode != 0:
            print(f"Error creating user '{args.username}'")
            if result.stderr:
                print(f"PostgreSQL error: {result.stderr}")
            sys.exit(1)
        print(f"User '{args.username}' created successfully")
    else:
        # Verify user exists when skipping creation
        if not user_exists(
            args.username, host=args.host, port=args.port, pg_user=args.postgres_user
        ):
            print(
                f"Error: User '{args.username}' does not exist. Remove --skip-create to create the user."
            )
            sys.exit(1)
        print(f"User '{args.username}' exists, assigning privileges...")

    # Grant privileges
    print(
        f"Granting API privileges to user '{args.username}' on database '{args.database}'..."
    )

    privilege_commands = f"""
GRANT CONNECT ON DATABASE "{args.database}" to {args.username};

GRANT USAGE on SCHEMA public to {args.username};
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public to {args.username};
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public to {args.username};

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {args.username};
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO {args.username};
"""

    result = run_psql(
        args.database,
        privilege_commands,
        host=args.host,
        port=args.port,
        user=args.postgres_user,
    )
    if result.returncode != 0:
        print(f"Error granting privileges to user '{args.username}'")
        if result.stderr:
            print(f"PostgreSQL error: {result.stderr}")
        sys.exit(1)

    if password:
        print(f"✓ Created API user '{args.username}' with password: {password}")
    else:
        print(f"✓ Assigned API privileges to user '{args.username}'")


if __name__ == "__main__":
    main()

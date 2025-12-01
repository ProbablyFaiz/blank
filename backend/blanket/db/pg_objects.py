"""In this file, we'll define Postgres functions, policies, and triggers we want Alembic
to track via alembic-utils. See https://olirice.github.io/alembic_utils/quickstart/
for more information."""

from alembic_utils.pg_extension import PGExtension
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_policy import PGPolicy

set_current_user_function = PGFunction(
    schema="public",
    signature="set_current_user(user_id integer)",
    definition="""
    RETURNS VOID AS $$
    BEGIN
        PERFORM set_config('app.current_user_id', user_id::text, false);
    END;
    $$ LANGUAGE plpgsql;
    """,
)

get_current_user_function = PGFunction(
    schema="public",
    signature="get_current_user()",
    definition="""
    RETURNS integer AS $$
    DECLARE
        user_id_text text;
    BEGIN
        user_id_text := current_setting('app.current_user_id', true);

        -- Return NULL if not set or empty string
        IF user_id_text IS NULL OR user_id_text = '' THEN
            RETURN NULL;
        END IF;

        -- Try to convert to integer, return NULL if invalid
        BEGIN
            RETURN user_id_text::integer;
        EXCEPTION WHEN invalid_text_representation THEN
            RETURN NULL;
        END;
    END;
    $$ LANGUAGE plpgsql;
    """,
)

postgis_extension = PGExtension(schema="public", signature="postgis")


tasks_user_policy = PGPolicy(
    schema="public",
    signature="tasks_user_policy",
    on_entity="public.tasks",
    definition="""
    AS PERMISSIVE
    USING (EXISTS (
        SELECT 1
        FROM app_users ua
        WHERE ua.id = get_current_user() AND ua.id = tasks.creator_id
    ))
    """,
)


PG_OBJECTS = [
    set_current_user_function,
    get_current_user_function,
    postgis_extension,
    tasks_user_policy,
]

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run all tests: `cd backend && pytest`
- Run frontend typechecking: `just typecheck`
- Run pytest tests: `just pytest`
- Run single test: `cd backend && uv run pytest test/path/to/test_file.py::TestClass::test_function -v`
- Format code: `just lint`
  - Often helpful to run this after making large code changes.
- Generate OpenAPI client: `just openapi` (regenerates frontend/src/client from running API)
- Generate (but do not run) DB migrations based on changes to backend/blank/db/models.py: `just migrate "message"` (auto-generate)
    - Please use `just migrate` and then modify the alembic migration as necessary, do not try to create one from scratch manually.
    - Remember when creating migrations for non-nullable columns that if they are for an existing table, you will probably need to
    modify the migration to first create the column as nullable, initialize the column's values appropriately, and then set it to
    non-nullable.

Note that, as shown, to run code in the backend Python environment, one must run `uv run <your python command>`
inside the `backend/` directory. The `just` shortcuts handle this for you when they are available.

YOU ARE ABSOLUTELY PROHIBITED FROM EXECUTING THE MIGRATION YOU HAVE GENERATED YOURSELF. DO NOT RUN `just migrate-up` OR
`alembic upgrade ...` or `alembic downgrade ...` UNDER ANY CIRCUMSTANCES. IF RUNNING A MIGRATION IS NECESSARY FOR THE
CONTINUATION OF WORK, ASK THE USER TO PERFORM IT.

## Pull Requests

When writing PR descriptions, be concise! It is unnecessary to bullet list every change in detail;
give the core changes. Most importantly, a PR should prominently highlight things which are important
for other developers to know: for instance, database migrations should be highlighted, any new environment
variables that they may want or need to set, etc. Remember: be concise, the purpose of these PRs is to
be communicative and not just a list of changes.

## Codebase Architecture
- **Package Management**: Backend uses `uv` (must prefix Python commands with `uv run` in backend dir)
- **API Client**: Uses Hey API (@hey-api/openapi-ts) with Axios client, not standard fetch
- **Database**: PostgreSQL with SQLAlchemy ORM, Alembic migrations, supports advanced features like RLS
- **Auth**: Auth0 integration with fastapi-auth0, supports organization-based multi-tenancy
- **Frontend**: React with TypeScript, feature-based organization in src/features/
- **State Management**: React Query for server state, React Context for auth/global state
- **Pre-commit Hooks**: Enforces ruff (Python), biome (TypeScript), and other quality checks

## Testing & Quality
- **Backend Tests**: Use pytest with VCR for HTTP mocking, complex auth mocking can be challenging
- **Frontend Type Checking**: Always run `pnpm typecheck` before commits
- **Code Quality**: Pre-commit hooks catch most issues, but manual review still needed
- **Generated Code**: API client files have linting issues that should be ignored (many @typescript-eslint/no-explicit-any)

## Development Notes
- **Auth Integration**: Complex dependency tree requiring careful mocking in tests
- **Database Relationships**: Watch for SQLAlchemy relationship overlap warnings in models
- **API Generation**: Client regeneration can introduce linting issues in generated files
- **Migration Best Practice**: Always use `just migrate "message"` to auto-generate migrations from model changes, then manually add any complex logic (like RLS policies). This ensures future devs get proper alembic detection and makes migrations more maintainable.
- **Pre-commit Best Practice**: If you run pre-commit run --all-files before committing, you can avoid having to double commit once the issues are fixed.
- **RLS Policies**: Define PGPolicy objects in models.py and register them in env.py for auto-generation. Syntax: signature is just policy name, on_entity is fully qualified table name (e.g., "public.table_name").

## Code Style
- Python: Use Ruff formatting (88 char line length), type annotations, snake_case functions/variables
- TypeScript: Biome formatting (2-space indent), functional React components, feature-based organization
- Imports: Group by standard library, third-party, local (alphabetically within groups)
- Error handling: Explicit error raising with descriptive messages and proper HTTP status codes
- Tests: Use pytest fixtures, VCR for HTTP mocking (`VCR_RECORD_MODE=once`)
- Typing: Full type annotations throughout, Pydantic models for API validation

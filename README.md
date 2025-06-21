# Blank Template

A full-stack template with a React frontend and FastAPI backend.

## Tech Stack

**Frontend:**
- [React 19](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/) + [Vite](https://vite.dev/)
- [TanStack Router](https://tanstack.com/router/latest/docs/framework/react/overview) for routing
- [shadcn/ui](https://ui.shadcn.com/) + [Tailwind CSS](https://tailwindcss.com/) for styling
- [TanStack Query](https://tanstack.com/query/latest/docs/framework/react/overview) for API state management

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) with async/await support
- [SQLAlchemy](https://www.sqlalchemy.org/) 2.x ORM + [Alembic](https://alembic.sqlalchemy.org/en/latest/) migrations
- [PostgreSQL](https://www.postgresql.org/) database
- [Pydantic](https://docs.pydantic.dev/) 2.x for data validation

**Tools:**
- [just](https://github.com/casey/just) for task automation
- [pnpm](https://pnpm.io/) for frontend package management
- [uv](https://docs.astral.sh/uv/) for Python dependency management
- **Code Quality**: Pre-commit hooks with [Ruff](https://github.com/astral-sh/ruff) (Python) and [Biome](https://biomejs.dev/) (TypeScript/JavaScript)

## Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **uv** (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **pnpm** (`npm install -g pnpm`)
- **just** task runner (`uv tool install rust-just`)
- **PostgreSQL**

For deployment:
- **Docker**/**Docker Compose**

## Quick Start

### 1. Clone and Customize

```bash
git clone https://github.com/ProbablyFaiz/blank.git <your-project-name>
cd <your-project-name>
```

**Customize the project name:**
- Recommended: Use VSCode's find/replace (Ctrl+Shift+H) with "Preserve Case" enabled
- Replace all instances of `blank` with your project name
- Update `backend/pyproject.toml` project name and description
- Update `frontend/package.json` name field

### 2. Install Dependencies

```bash
just install
```

This installs:
- Python dependencies in a virtual environment via `uv`
- Frontend dependencies via `pnpm`

### 3. Configure Environment

```bash
cp template.env .env
mkdir data
```

Edit `.env` and fill in the variables:
- Set `DATA_ROOT` to the absolute path of your `data` directory
- Configure PostgreSQL connection details
- For database credentials, use the helper scripts in `infra/` to create users:
  ```bash
  ./infra/create_admin_db_user.fish <your_admin_user> <your_database>
  ./infra/create_api_db_user.fish <your_api_user> <your_database>
  ```

### 4. Start Development

**Terminal 1 - Backend:**
```bash
just api
```

**Terminal 2 - Frontend:**
```bash
just frontend
```

Your app will be available at:
- Frontend: http://localhost:5185
- Backend API: http://localhost:8101
- API Docs: http://localhost:8101/docs

## Available Commands

### Development
- `just api` - Start FastAPI backend server
- `just frontend` - Start React development server
- `just routes` - Regenerate TanStack Router routes
- `just openapi` - Regenerate API client from backend OpenAPI spec
- `just shadcn-add <component>` - Add a shadcn/ui component; equivalent to `pnpm dlx shadcn@latest add <component>`

### Building & Quality
- `just build` - Build frontend for production
- `just lint` - Run pre-commit hooks (formatting, linting)
- `just typecheck` - Run TypeScript type checking

### Database
- `just migrate "description"` - Generate new Alembic migration
- `just migrate-up` - Apply pending migrations
- `just migrate-down` - Rollback last migration

### Shortcuts
- `just` - Show all available commands
- `just install` - Install all dependencies (frontend + backend)

## Project Structure

```
├── backend/           # FastAPI backend
│   ├── blank/         # Main package (rename this!)
│   │   ├── api/       # API routes
│   │   └── db/        # Database models & session
│   ├── alembic/       # Database migrations
│   └── pyproject.toml # Python dependencies
├── frontend/          # React frontend
│   ├── src/
│   │   ├── routes/    # TanStack Router routes
│   │   ├── features/  # Feature-based components
│   │   └── components/ui/ # shadcn/ui components
│   └── package.json   # Frontend dependencies
└── Justfile          # Task automation
```

**Note on Authentication:** This template doesn't include authentication by default. For production apps, we recommend Auth0 with `fastapi-auth0` (backend) and `@auth0/auth0-react` (frontend).

## Development Tips

- **Database changes**: Always create migrations with `just migrate "description"`
- **Code quality**: Run `just lint` before committing

Happy coding! 🚀

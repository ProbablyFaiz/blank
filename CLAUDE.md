# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Run all tests: `cd backend && pytest`
- Run frontend typechecking: `just typecheck`
- Run backend (Python) tests: `just test-backend`
    - Run single test file: `just test-backend <path to test file relative to backend/>` e.g., `just test-backend test/api/test_tasks_api.py`
- Run frontend (TS) tests: `just test-frontend`
    - Run single test file: `just test-frontend <path to test file relative to frontend/>` e.g., `just test-frontend src/features/home/HomePage.test.tsx`

- Format code: `just lint`
  - Often helpful to run this after making large code changes.
- Generate OpenAPI client: `just openapi` (regenerates frontend/src/client from running API)
- Generate (but do not run) DB migrations based on changes to backend/start/db/models.py: `just migrate "message"` (auto-generate)
    - Please use `just migrate` and then modify the alembic migration as necessary, do not try to create one from scratch manually.
    - Remember when creating migrations for non-nullable columns that if they are for an existing table, you will probably need to
    modify the migration to first create the column as nullable, initialize the column's values appropriately, and then set it to
    non-nullable.
- You should not, unless instructed, run the API or frontend dev servers; the developer is almost certainly already running them, and you doing so will just be harmful.

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

## FastAPI API Conventions
- All endpoints should be decorated with the response_model and an operation ID (in camel case, e.g. `listEvalIssues`). GET endpoints which return lists/paginated lists should be named as list{plural object in camel case}, for single objects, `read{singular object in camel case}`, e.g. `readEvalIssue`.
- When declaring endpoint dependencies, use the Annotated syntax, e.g., `db: Annotated[Session, Depends(get_db)]`, NOT the `= Depends(get_db)` default argument syntax.
- Words in urls should be separated by underscores, not dashes. E.g. `issue_histories` not `issue-histories`.
- By convention, list endpoints should return a paginated object using the PaginatedBase generic in backend/blank/api/interfaces.py. Here is an example:

```python
@router.get(
    "/tasks", response_model=PaginatedBase[TaskListItem], operation_id="listTasks"
)
def list_tasks(
    db: Annotated[Session, Depends(get_db)],
    project_id: int | None = None,
    search: Annotated[str, Query()] | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
):
    query = (
        # omitted
    )

    if project_id is not None:
        ...  # omitted

    if search is not None:
        ...  # omitted

    query = (
       ...  # omitted
    )
    tasks = db.execute(query).scalars().all()

    return PaginatedBase(
        items=tasks,
        total=total,
        page=page,
        size=limit,
    )
```

## Backend Development
- Typing is very important, so be sure to type any function arguments/outputs.
  - In Python, the lowercase types (e.g. 'list', 'dict') should be used where available instead of importing from the typing package. Note that lowercase types do not need to be imported.
  - Use `SomeType | None` instead of `Optional[SomeType]`.
- Pathlib Paths should be used over the equivalent os functions.
- Use SQLAlchemy 2.x ORM syntax, not 1.x.
  - Some helpful context: my projects are typically structured such that models are in <project_name>.db.models, and you can create a session with `from <project_name>.db.session import get_session` (e.g. `from cdle.db.session`) and then `session = get_session()`.
- Use Pydantic 2.x syntax, not 1.x.
- Prefer Pydantic models over dataclasses when applicable.
- Prefer full imports for lowercase (non-class, usually) symbols, e.g. `import tenacity ... @tenacity.retry` or `import tqdm ... tqdm.tqdm()`, and `from` imports for uppercase constants and classes, e.g., `from blank.db.models import Chunk, CHUNK_SEPARATOR`.

### Writing Standalone Scripts
- We like progress bars! *Long-running, important* loops should use a tqdm progress bar with appropriate concise desc parameter set. When postfixes are necessary (e.g. if tracking the number of records skipped in some loop operation), define a `pbar` variable separately, and then update it and set the postfix within the loop manually.
- To avoid confusion, always do "import tqdm" and then "tqdm.tqdm" for the progress bar instead of "from tqdm import tqdm". Repeat, use `import tqdm` and `tqdm.tqdm(...)` in code, NEVER `from tqdm import tqdm` and `tqdm(...)`.

### Using the `rl` Utility Library
When writing Python scripts, we have a utility library called `rl`. Some notes on `rl` and the way we use it:
- We have an enhanced version of click, the Python CLI library. The only difference in usage from the regular click is one does `import rl.utils.click as click` instead of `import click`.
- When using logging in a program, use `rl`'s preconfigured logger: `from rl.utils import LOGGER`.
- `rl` has (among others) the following IO functions, usable within `import rl.utils.io` (do not `from import`, use the absolute import):
    - `def get_data_path(*args) -> Path` — Generally, whenever a CLI script deals with input and output files/dirs, the default paths (which should typically be configurable via CLI options) are set on some subpath of the data path. E.g. `_DEFAULT_OUTPUT_DIR = rl.utils.io.get_data_path("raw_codes", "sf")`.
    - `def read_jsonl(filename: str | Path) -> Iterable[Any]` — yield an iterable of JSON-parsed items from a JSONL file, used as `for record in rl.utils.io.read_jsonl(...):` etc. If loading JSONL records into Pydantic models, you can also do `rl.utils.io.read_jsonl_into_pydantic(..., pydantic_cls=<pydantic_model>)` to iterate the records into a Pydantic model instances.
    - `def download(url: str, dest: str | Path) -> None` — Downloads a given url to a file with a progress bar, so when doing pure downloads this is preferable.

### Creating Click CLIs
When creating click CLIs, obey the following conventions:
- Unless otherwise instructed, prefer options, not arguments. Provide concise and descriptive help text for each option. Provide both a long (--foo) and short (-f) for all options unless doing so would lead to a conflict.
- Default values for options should be stored as private global constants (`_ALL_CAPS`) at the top of the file and then referenced (`default=_DEFAULT_INPUT_PATH`) in the option decorator.
- When declaring options that refer to file paths or directories, file paths should be suffixed with '_path', while directory paths should be suffixed with '_dir'. Path options should always be declared with `type=click.Path([any applicable exists/okay options], path_type=Path)` and the resulting function argument should therefore be typed as a pathlib `Path`.

## Frontend Development
- When using React, we use Typescript and typically build most UI elements with Tailwind/shadcn
    - Please use shadcn components where available or installable. When asked to use icons, use Lucide icons.
- When designing UI, you should build components that are aesthetically pleasing, modern in design, and consistent with the app's existing conventions.
- Generally speaking, import project files relative to the src directory using the `@/` alias, e.g. `@/features/home/CTA.tsx`

### API Client Usage (React Query)
Our API client is auto-generated and provides TanStack Query (React Query) integration:
- Import types from `@/client` (e.g., `import { TaskListItem } from "@/client"`)
- Import services like `DefaultService` from `@/client`
- Import query options from `@/client/@tanstack/react-query.gen`

API endpoint naming convention follows these patterns:
- GET endpoints for single items generate `readXOptions` functions (e.g., `readTaskOptions`)
- GET endpoints for paginated lists generate `listXOptions` functions (e.g., `listTaskRunPredictionsOptions`)
- Query keys are available as `readXQueryKey` and `listXQueryKey` functions with the same arguments as the `readXOptions` functions.

When using the client with React Query:
- For read operations, spread the options from the generated functions:
  ```typescript
  const { data } = useQuery({
    ...readTaskOptions({ path: { task_id: taskId } }),
  });
  ```
  - Note that useQuery does not have `onSuccess` or `onError` callbacks. To take actions on success and failure, you must use `useEffect` as is typical in React.
- For mutations, use the service directly:
  ```typescript
  const mutation = useMutation({
    mutationFn: (taskId: number) =>
      DefaultService.archiveTask({ path: { task_id: taskId } }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: getTasksQueryKey() });
    },
  });
  ```

### Implementing Pagination
- Use the `PaginationControl` component from `@/components` (`import PaginationControl from "@/components/PaginationControl"`):
  ```typescript
  interface PaginationControlProps {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
    onPageHover?: (page: number) => void;
  }
  ```
- Implement prefetching on hover for pagination items using `onPageHover`
- Use `keepPreviousData` option with paginated queries for smoother transitions:
  ```typescript
  const { data } = useQuery({
    ...listSomethingOptions({ query: { page: currentPage, limit: pageSize } }),
    placeholderData: keepPreviousData,
  });
  ```

### Performance Best Practices
- Implement prefetching when hovering over list items
- Always invalidate related queries after mutations that affect the data
- For heavily nested components, consider using QueryClient directly for prefetching

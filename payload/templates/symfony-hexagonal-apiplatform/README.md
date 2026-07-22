# __PROJECT_NAME__

__PROJECT_DESCRIPTION__

## Development

```bash
composer install            # install dependencies
symfony server:start        # run the app (or: php -S localhost:8000 -t public)

composer test               # run the tests (PHPUnit)
composer stan               # static analysis (PHPStan, level max)
composer cs                 # fix code style (PHP-CS-Fixer)
composer check              # cs check + stan + tests (CI gate)
```

The REST API is served by **API Platform** under `/api` (interactive docs at `/api`).

## Layout (hexagonal — ports & adapters, with API Platform)

Dependencies point inward: `Infrastructure → Application → Domain`. The domain
knows nothing about Symfony, Doctrine or API Platform.

- `src/Domain/` — pure PHP: `Model/` (aggregates), `ValueObject/`, `Repository/`
  (port interfaces), `Exception/`. No framework imports.
- `src/Application/` — use cases: `Command/`, `Query/`, `Handler/` (Messenger),
  `Port/` (outbound ports like `Clock`).
- `src/Infrastructure/` — adapters. `ApiPlatform/Resource/` — API DTOs decorated
  with `#[ApiResource]` (the domain model is never decorated); `ApiPlatform/State/`
  — the **Processor** (write) and **Provider** (read) that bridge API Platform to
  the Application/Domain via the command bus and repository ports.
  `Doctrine/` (`Mapping/` XML, `Repository/`, `Type/`) — persistence.
  `Symfony/Kernel.php` — the framework bootstrap (glue, so it lives here).
  Ports are bound to adapters in `config/services.yaml`.
- `tests/` — `Application/` unit tests (no kernel), `Infrastructure/` functional
  tests (`WebTestCase`), `Double/` test fakes.

The included `Task` slice is a worked example: `POST /api/tasks` → `TaskResource` →
`CreateTaskProcessor` → `CreateTask` command → handler → domain model → Doctrine
adapter; `GET /api/tasks/{id}` → `TaskProvider` → repository port → resource.

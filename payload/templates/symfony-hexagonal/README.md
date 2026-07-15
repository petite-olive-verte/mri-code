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

## Layout (hexagonal — ports & adapters)

Dependencies point inward: `Infrastructure → Application → Domain`. The domain
knows nothing about Symfony or Doctrine.

- `src/Domain/` — pure PHP: `Model/` (aggregates), `ValueObject/`, `Repository/`
  (port interfaces), `Exception/`. No framework imports.
- `src/Application/` — use cases: `Command/`, `Query/`, `Handler/` (Messenger),
  `Port/` (outbound ports like `Clock`).
- `src/Infrastructure/` — adapters: `Doctrine/` (`Mapping/` XML, `Repository/`,
  `Type/`), `Controller/` (thin HTTP). Ports are bound to adapters in
  `config/services.yaml`.
- `tests/` — `Application/` unit tests (no kernel), `Infrastructure/` functional
  tests (`WebTestCase`), `Double/` test fakes.

The included `Task` slice is a worked example of the flow: HTTP request DTO →
command → handler → domain model → Doctrine adapter.

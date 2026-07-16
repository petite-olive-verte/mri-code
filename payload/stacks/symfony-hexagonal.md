- **PHP ≥ 8.3** (the floor the template's language features require) with `declare(strict_types=1)` in every file.
- **Composer** for dependencies (single source of truth: `composer.json`).
- **Latest stable Symfony** (currently the 7.4 series); framework code at the edges, not in the business logic.
- **PHPStan** at **level max** (+ strict-rules, symfony & doctrine extensions) — zero errors (`composer stan`).
- **PHP-CS-Fixer** (`@Symfony` + `@PSR12` + strict) for style — `composer cs:check`.
- **PHPUnit** for tests (`composer test`); add zenstruck/foundry when you need object factories/fixtures.
- **Doctrine ORM** for persistence, mapped by **XML** under `src/Infrastructure/Doctrine/Mapping/` so
  the domain model carries no ORM attributes; migrations via doctrine-migrations.
- Native **enums** for closed sets of states; **readonly** value objects; constructor injection only.
- **Layout**: hexagonal (ports & adapters) — `src/Domain/` (pure PHP, zero framework),
  `src/Application/` (use cases), `src/Infrastructure/` (adapters). Ports are bound to adapters in
  `config/services.yaml`. Dependencies point inward, never outward.
- **Naming**: PSR-4/PSR-12 — `PascalCase` classes and filenames, `camelCase` methods; one class
  `src/<Layer>/Foo.php` ↔ one test `tests/<Layer>/FooTest.php`. The domain and use cases are
  unit-tested without booting the kernel; adapters via `KernelTestCase`/`WebTestCase`.

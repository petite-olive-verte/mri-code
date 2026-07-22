- **PHP ≥ 8.3** (the floor the template's language features require) with `declare(strict_types=1)` in every file.
- **Composer** for dependencies (single source of truth: `composer.json`).
- **Latest stable Symfony** (currently the 7.4 series); framework code at the edges, not in the business logic.
- **PHPStan** at **level max** (+ strict-rules, symfony & doctrine extensions) — zero errors (`composer stan`).
- **PHP-CS-Fixer** (`@Symfony` + `@PSR12` + strict) for style — `composer cs:check`.
- **PHPUnit** for tests (`composer test`); add zenstruck/foundry when you need object factories/fixtures.
- **Doctrine ORM** for persistence; migrations via doctrine-migrations.
- **Dev infra = Docker, Flex-managed.** Symfony Flex owns `compose.yaml`/`compose.override.yaml`
  through `###> pkg ###` blocks (`database` from doctrine, a mail catcher from `symfony/mailer`).
  **Extend** those blocks — pin versions via the env vars they expose (`POSTGRES_VERSION`, …) and
  hand-author only services with **no** recipe (e.g. MinIO). Never replace or duplicate a
  Flex-managed service, or `composer require` will keep re-injecting it and collide.
- Native **enums** for closed sets of states; **readonly** value objects; constructor injection only.
- **Layout**: PSR-4 — code in `src/`, tests in `tests/` mirroring the namespace tree.
- **Naming**: PSR-4/PSR-12 — `PascalCase` classes and filenames, `camelCase` methods; one class
  `src/Foo/Bar.php` ↔ one test `tests/Foo/BarTest.php`.

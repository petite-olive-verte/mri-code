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

## Layout

- `src/` — application code (`App\` namespace, PSR-4).
- `config/` — Symfony configuration and service wiring.
- `tests/` — PHPUnit tests, mirroring `src/`.
- `public/index.php` — HTTP entry point.

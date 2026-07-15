# PHP + Symfony (latest stable) — best practices (enforced conventions)

> The rules the implementation must follow on a Symfony project. Most are **enforced** by
> PHPStan (level max) and PHP-CS-Fixer; the rest are review criteria. Keep the business logic
> free of the framework — the constitution's "dependencies point inward" applies here.

## PHP language

- **`declare(strict_types=1)`** at the top of every file (enforced by PHP-CS-Fixer).
- **Native enums** for any closed set of states — never string/int constants:
  - *backed* enums (`enum X: string`) when the value is persisted / serialized;
  - *pure* enums for in-memory domain states. Enums may carry behaviour (`match`-based methods).
- **`readonly`** properties/classes for immutable **Value Objects**; construct valid or throw.
- **Constructor property promotion**; typed everything (params, returns, properties). Use `never`/`void`.
- Prefer **`match`** over `switch`; use **named arguments** for clarity on many-arg calls.
- **`final` by default** (composition over inheritance); `#[\Override]` when overriding.
- **`symfony/uid`** (ULID/UUID) for identifiers rather than DB auto-increment — keeps the domain
  independent of the persistence layer and lets you assign ids before flush.
- No bare `catch (\Throwable)`; catch specific exceptions. No hardcoded secrets.

```php
enum OrderStatus: string
{
    case Pending = 'pending';
    case Paid = 'paid';
    case Cancelled = 'cancelled';

    public function isTerminal(): bool
    {
        return match ($this) {
            self::Cancelled, self::Paid => true,
            self::Pending => false,
        };
    }
}

final readonly class Money
{
    public function __construct(public int $amountInCents, public string $currency)
    {
        if ($amountInCents < 0) {
            throw new \InvalidArgumentException('Amount must be positive.');
        }
    }
}
```

## Symfony

- **Constructor injection only** — never fetch from the container (`$this->get(...)`) or use it as a
  service locator. Rely on autowiring/autoconfiguration.
- **Thin, invokable controllers** (`__invoke`), `#[Route]` attributes. A controller maps HTTP ⇆ a
  command/query and serializes the result — no business rules.
- **Typed request payloads**: bind + validate DTOs with `#[MapRequestPayload]` / `#[MapQueryString]`
  instead of reading `$request` by hand.
- **Validation** via the Validator (constraints as attributes on DTOs). **Serialization** via the Serializer.
- **CQRS-lite with Messenger**: commands (writes) on `command.bus`, queries (reads) on `query.bus`;
  handlers are `#[AsMessageHandler]`, autoconfigured. The `validation` middleware is already wired.
- **Authorization** via Voters (`#[IsGranted]`), never inline role checks scattered in controllers.
- **Domain events** via the EventDispatcher; heavy work goes async through a Messenger transport.
- **Errors** → typed domain exceptions mapped to HTTP as **RFC 7807 Problem Details** in one listener,
  not `try/catch` in every controller.
- **Config**: env vars typed and injected with `#[Autowire]`; real secrets in `.env.local` or the
  **Symfony secrets vault**, never committed. Monolog with channels.

```php
#[AsController]
final class PlaceOrderController
{
    public function __construct(private readonly MessageBusInterface $commandBus) {}

    #[Route('/orders', methods: ['POST'])]
    public function __invoke(#[MapRequestPayload] PlaceOrderRequest $request): JsonResponse
    {
        $this->commandBus->dispatch(new PlaceOrder($request->sku, $request->quantity));

        return new JsonResponse(status: Response::HTTP_ACCEPTED);
    }
}
```

## Doctrine

- Repositories **return domain objects**, expose intention-revealing methods (`ofId`, `save`), not a
  generic query builder to callers.
- Map enums with **`#[ORM\Column(enumType: OrderStatus::class)]`**; use ULID/UUID id types from `symfony/uid`.
- Keep **no business logic** in entities beyond invariants; no service calls from entities.
- Schema changes go through **doctrine-migrations** (`make:migration` → review → `migrations:migrate`),
  never `schema:update` in a real environment.
- In a **hexagonal** layout, map with **XML in `Infrastructure/`** so `Domain/` entities stay attribute-free
  (see mri-code-scaffold-symfony-hexagonal).

## Tests & tooling

- **TDD** red-green-refactor (constitution). Unit-test the pure logic without booting the kernel;
  use **`KernelTestCase`** for integration and **`WebTestCase`** for HTTP.
- PHPUnit (latest stable) with `#[Test]` / `#[DataProvider]` attributes. **zenstruck/foundry** for test object factories.
- The spec's **acceptance criteria become tests**; target coverage ≥ 80%; at least one functional test
  per public entry point (HTTP route / CLI command).
- Gate every task on green: `composer check` (= `cs:check` + `stan` + `test`) before it's "done".
- **PHPStan level max** + `phpstan-strict-rules` + `phpstan-symfony` + `phpstan-doctrine`. Fix issues,
  don't baseline them away without a note.
- Small, atomic commits; never commit `vendor/`, `.env.local`, or secrets.

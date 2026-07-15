# Hexagonal architecture (ports & adapters) — the rules

> The rulebook the `symfony-hexagonal` template assumes. Read it before implementing, and keep new
> code on the right side of the boundary. This extends the general
> `php-symfony-best-practices.md` (enums, DTO mapping, Messenger, Doctrine) — everything there
> still applies.

## The one rule

**Dependencies point inward: `Infrastructure → Application → Domain`.** The domain never imports
the outer layers; the framework lives only at the edges. If a domain class needs something from
the outside (persistence, time, mail…), it declares a **port** (interface) and an **adapter** in
Infrastructure implements it.

## The three layers

### Domain — pure PHP, no framework
- `Model/` — aggregates/entities. **No ORM attributes**, no Doctrine, no Symfony imports. State
  changes go through intention-revealing methods, never public setters. Construct valid or throw.
- `ValueObject/` — immutable `readonly` types (ids, quantities, statuses). Enums for closed sets.
- `Repository/` — **port interfaces**, expressed in domain terms (`save(Task)`, `ofId(TaskId)`),
  never leaking a QueryBuilder or the EntityManager.
- `Exception/` — domain exceptions. They do not know about HTTP.
- Allowed dependency: value-type libraries like `symfony/uid` (a value object, not the framework).

### Application — use cases, orchestration
- `Command/` + `Query/` — immutable DTOs describing intent. **No validation attributes** here
  (validation is an edge concern; keep these pure).
- `Handler/` — one use case per handler (`#[AsMessageHandler(bus: 'command.bus')]` /
  `'query.bus'`). Depends **only on domain ports**, never on Doctrine or HTTP. Fully unit-testable.
- `Port/` — outbound ports the use cases need beyond persistence (e.g. `Clock`, `Notifier`).

### Infrastructure — adapters, the only place the framework appears
- `Controller/` — thin driving adapters. Bind + validate an **HTTP request DTO** with
  `#[MapRequestPayload]`, translate it into an Application command/query, dispatch it, serialize the
  result. No business logic.
- `Doctrine/Mapping/` — **XML** mapping for the domain model (this is what keeps `Domain/Model/`
  attribute-free). `Doctrine/Repository/` — port implementations. `Doctrine/Type/` — custom types
  translating value objects to/from columns.
- Other driven adapters (mail, clock, HTTP clients) live here too.

## Wiring — the three Symfony gotchas

1. **Keep the domain pure** → map entities with XML under `Infrastructure/Doctrine/Mapping/`
   (`SimplifiedXmlDriver`: with prefix `App\Domain\Model`, entity `App\Domain\Model\Task` maps from
   `Task.orm.xml`). Persist value objects via **custom Doctrine types**; persist enums via
   `enum-type`.
2. **Bind ports to adapters** in `config/services.yaml`:
   `App\Domain\Repository\TaskRepository: '@App\Infrastructure\Doctrine\Repository\DoctrineTaskRepository'`.
3. **Autowiring boundary** → in `services.yaml`, **exclude** `Domain/Model`, `Domain/ValueObject`,
   `Domain/Exception`, `Application/Command`, `Application/Query` from service registration: they are
   *data*, constructed by handlers or Doctrine, never injected. Handlers, controllers and adapters
   *are* services.

## Testing the layers
- **Domain + Application** → plain `PHPUnit\Framework\TestCase`, no kernel. Use fakes for the ports
  (see `tests/Double/InMemoryTaskRepository`, `FixedClock`). Fast and deterministic.
- **Infrastructure** → `KernelTestCase` (Doctrine adapters, against a test DB) and `WebTestCase`
  (controllers). The spec's acceptance criteria become tests, TDD red-green-refactor.

## Where does new code go? (quick test)
- Is it a business rule / invariant? → **Domain**.
- Does it orchestrate a scenario across the domain? → **Application** (a handler).
- Does it talk to the framework, the DB, the network, the clock, or HTTP? → **Infrastructure**
  (an adapter behind a port).

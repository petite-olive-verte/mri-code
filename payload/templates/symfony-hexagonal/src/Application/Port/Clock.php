<?php

declare(strict_types=1);

namespace App\Application\Port;

/**
 * Outbound port for the current time. Injecting the clock instead of calling
 * `new \DateTimeImmutable()` keeps use cases deterministic and unit-testable
 * (see tests: FixedClock). Bound to SystemClock in config/services.yaml.
 */
interface Clock
{
    public function now(): \DateTimeImmutable;
}

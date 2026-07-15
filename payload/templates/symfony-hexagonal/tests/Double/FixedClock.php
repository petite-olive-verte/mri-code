<?php

declare(strict_types=1);

namespace App\Tests\Double;

use App\Application\Port\Clock;

/**
 * Deterministic clock for tests — freezes time so use cases are reproducible.
 *
 * @internal test double
 */
final readonly class FixedClock implements Clock
{
    public function __construct(private \DateTimeImmutable $now)
    {
    }

    public function now(): \DateTimeImmutable
    {
        return $this->now;
    }
}

<?php

declare(strict_types=1);

namespace App\Infrastructure\Clock;

use App\Application\Port\Clock;

/**
 * Driven adapter: the real clock. Bound to the Clock port in services.yaml.
 */
final class SystemClock implements Clock
{
    public function now(): \DateTimeImmutable
    {
        return new \DateTimeImmutable();
    }
}

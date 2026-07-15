<?php

declare(strict_types=1);

namespace App\Enum;

/**
 * Backed enum — the canonical way to model a closed set of states in modern PHP.
 *
 * Backed enums (here `string`) serialize cleanly to JSON, to the database
 * (Doctrine `enumType:`), and to HTTP payloads, while pure enums (no backing
 * value) suit in-memory domain states. Prefer enums over class constants.
 */
enum HealthStatus: string
{
    case Ok = 'ok';
    case Degraded = 'degraded';

    /** Human-readable label — enums can carry behaviour, not just values. */
    public function label(): string
    {
        return match ($this) {
            self::Ok => 'All systems operational',
            self::Degraded => 'Running with degraded performance',
        };
    }
}

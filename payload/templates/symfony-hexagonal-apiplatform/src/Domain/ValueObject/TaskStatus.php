<?php

declare(strict_types=1);

namespace App\Domain\ValueObject;

/**
 * Backed enum modelling the task lifecycle. Lives in the domain and is
 * persisted as a string via Doctrine's `enum-type` mapping (no framework
 * dependency leaks in here).
 */
enum TaskStatus: string
{
    case Todo = 'todo';
    case Done = 'done';

    public function isFinished(): bool
    {
        return self::Done === $this;
    }
}

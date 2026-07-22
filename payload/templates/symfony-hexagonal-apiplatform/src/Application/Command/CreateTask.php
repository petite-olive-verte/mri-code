<?php

declare(strict_types=1);

namespace App\Application\Command;

/**
 * Command — a pure, immutable intent to change state. It carries no framework
 * concerns (no validation attributes): the HTTP request DTO at the edge is
 * validated and then translated into this command.
 */
final readonly class CreateTask
{
    public function __construct(public string $title)
    {
    }
}

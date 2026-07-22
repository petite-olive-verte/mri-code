<?php

declare(strict_types=1);

namespace App\Domain\Exception;

use App\Domain\ValueObject\TaskId;

/**
 * Domain exception. Infrastructure maps it to an HTTP 404 (RFC 7807) in a
 * single exception listener, so use cases never speak HTTP.
 */
final class TaskNotFound extends \RuntimeException
{
    public static function withId(TaskId $id): self
    {
        return new self(\sprintf('Task "%s" was not found.', $id->value));
    }
}

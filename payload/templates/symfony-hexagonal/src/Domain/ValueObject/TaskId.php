<?php

declare(strict_types=1);

namespace App\Domain\ValueObject;

use Symfony\Component\Uid\Ulid;

/**
 * Identity value object. Immutable and self-validating. The domain owns the
 * concept of identity; the persistence layer (Doctrine) only knows how to
 * store its string form — see Infrastructure\Doctrine\Type\TaskIdType.
 */
final readonly class TaskId
{
    public function __construct(public string $value)
    {
        if (!Ulid::isValid($value)) {
            throw new \InvalidArgumentException(\sprintf('Invalid TaskId "%s".', $value));
        }
    }

    public static function generate(): self
    {
        return new self((new Ulid())->toBase32());
    }

    public function equals(self $other): bool
    {
        return $this->value === $other->value;
    }

    public function __toString(): string
    {
        return $this->value;
    }
}

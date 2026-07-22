<?php

declare(strict_types=1);

namespace App\Infrastructure\Doctrine\Type;

use App\Domain\ValueObject\TaskId;
use Doctrine\DBAL\Platforms\AbstractPlatform;
use Doctrine\DBAL\Types\Type;

/**
 * Custom Doctrine type: translates the domain's TaskId value object to/from a
 * plain string column. This is the seam that lets the domain model stay pure
 * while persistence deals in scalars. Registered as `task_id` in doctrine.yaml.
 */
final class TaskIdType extends Type
{
    public const string NAME = 'task_id';

    public function getSQLDeclaration(array $column, AbstractPlatform $platform): string
    {
        return $platform->getStringTypeDeclarationSQL(['length' => 26, 'fixed' => true]);
    }

    public function convertToPHPValue(mixed $value, AbstractPlatform $platform): ?TaskId
    {
        if (null === $value || $value instanceof TaskId) {
            return $value;
        }

        if (!\is_string($value)) {
            throw new \InvalidArgumentException('Expected a string TaskId column value.');
        }

        return new TaskId($value);
    }

    public function convertToDatabaseValue(mixed $value, AbstractPlatform $platform): ?string
    {
        if (null === $value) {
            return null;
        }

        if ($value instanceof TaskId) {
            return $value->value;
        }

        if (!\is_string($value)) {
            throw new \InvalidArgumentException('Expected a TaskId or string.');
        }

        return $value;
    }
}

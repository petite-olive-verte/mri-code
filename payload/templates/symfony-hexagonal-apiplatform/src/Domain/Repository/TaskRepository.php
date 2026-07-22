<?php

declare(strict_types=1);

namespace App\Domain\Repository;

use App\Domain\Model\Task;
use App\Domain\ValueObject\TaskId;

/**
 * Outbound port. The domain declares what it needs from persistence in its own
 * terms; the adapter (Infrastructure\Doctrine\Repository\DoctrineTaskRepository)
 * provides the implementation, wired in config/services.yaml.
 */
interface TaskRepository
{
    public function save(Task $task): void;

    public function ofId(TaskId $id): ?Task;
}

<?php

declare(strict_types=1);

namespace App\Tests\Double;

use App\Domain\Model\Task;
use App\Domain\Repository\TaskRepository;
use App\Domain\ValueObject\TaskId;

/**
 * In-memory adapter for the TaskRepository port. Because the port is defined in
 * the domain, the use cases can be unit-tested with this fake — no database,
 * no kernel — which is the whole point of ports and adapters.
 *
 * @internal test double
 */
final class InMemoryTaskRepository implements TaskRepository
{
    /** @var array<string, Task> */
    private array $tasks = [];

    public function save(Task $task): void
    {
        $this->tasks[$task->id()->value] = $task;
    }

    public function ofId(TaskId $id): ?Task
    {
        return $this->tasks[$id->value] ?? null;
    }
}

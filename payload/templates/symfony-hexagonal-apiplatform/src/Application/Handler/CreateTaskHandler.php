<?php

declare(strict_types=1);

namespace App\Application\Handler;

use App\Application\Command\CreateTask;
use App\Application\Port\Clock;
use App\Domain\Model\Task;
use App\Domain\Repository\TaskRepository;
use App\Domain\ValueObject\TaskId;
use Symfony\Component\Messenger\Attribute\AsMessageHandler;

/**
 * Use case. Depends only on domain ports (TaskRepository, Clock) — never on
 * Doctrine or the HTTP layer — so it is fully unit-testable without a kernel.
 * Registered on the command bus; returns the new id for the caller.
 */
#[AsMessageHandler(bus: 'command.bus')]
final readonly class CreateTaskHandler
{
    public function __construct(
        private TaskRepository $tasks,
        private Clock $clock,
    ) {
    }

    public function __invoke(CreateTask $command): TaskId
    {
        $task = Task::create(TaskId::generate(), $command->title, $this->clock->now());
        $this->tasks->save($task);

        return $task->id();
    }
}

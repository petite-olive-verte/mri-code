<?php

declare(strict_types=1);

namespace App\Infrastructure\ApiPlatform\State;

use ApiPlatform\Metadata\Operation;
use ApiPlatform\State\ProcessorInterface;
use App\Application\Command\CreateTask;
use App\Domain\Repository\TaskRepository;
use App\Domain\ValueObject\TaskId;
use App\Infrastructure\ApiPlatform\Resource\TaskResource;
use Symfony\Component\Messenger\HandleTrait;
use Symfony\Component\Messenger\MessageBusInterface;

/**
 * Write adapter (POST): translates the validated TaskResource into the
 * CreateTask command, dispatches it on the command bus, then re-reads the
 * created task through the domain repository and returns it as a resource.
 *
 * @implements ProcessorInterface<TaskResource, TaskResource>
 */
final class CreateTaskProcessor implements ProcessorInterface
{
    use HandleTrait;

    public function __construct(
        MessageBusInterface $commandBus,
        private readonly TaskRepository $tasks,
    ) {
        $this->messageBus = $commandBus;
    }

    public function process(mixed $data, Operation $operation, array $uriVariables = [], array $context = []): TaskResource
    {
        \assert($data instanceof TaskResource);

        /** @var TaskId $id */
        $id = $this->handle(new CreateTask($data->title));

        $task = $this->tasks->ofId($id)
            ?? throw new \RuntimeException('Task not found right after creation.');

        return TaskResource::fromDomain($task);
    }
}

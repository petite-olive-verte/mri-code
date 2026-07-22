<?php

declare(strict_types=1);

namespace App\Infrastructure\ApiPlatform\State;

use ApiPlatform\Metadata\Operation;
use ApiPlatform\State\ProviderInterface;
use App\Domain\Repository\TaskRepository;
use App\Domain\ValueObject\TaskId;
use App\Infrastructure\ApiPlatform\Resource\TaskResource;

/**
 * Read adapter (GET item): loads a Task through the domain repository port and
 * maps it to the API resource. A missing or malformed id yields null, which
 * API Platform renders as 404.
 *
 * @implements ProviderInterface<TaskResource>
 */
final class TaskProvider implements ProviderInterface
{
    public function __construct(private readonly TaskRepository $tasks)
    {
    }

    public function provide(Operation $operation, array $uriVariables = [], array $context = []): ?TaskResource
    {
        $id = $uriVariables['id'] ?? null;
        if (!\is_string($id)) {
            return null;
        }

        try {
            $task = $this->tasks->ofId(new TaskId($id));
        } catch (\InvalidArgumentException) {
            return null; // malformed id → 404
        }

        return null === $task ? null : TaskResource::fromDomain($task);
    }
}

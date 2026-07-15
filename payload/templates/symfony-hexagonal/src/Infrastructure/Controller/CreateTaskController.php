<?php

declare(strict_types=1);

namespace App\Infrastructure\Controller;

use App\Application\Command\CreateTask;
use App\Domain\ValueObject\TaskId;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Attribute\MapRequestPayload;
use Symfony\Component\Messenger\HandleTrait;
use Symfony\Component\Messenger\MessageBusInterface;
use Symfony\Component\Routing\Attribute\Route;

/**
 * Driving adapter (inbound). Thin: it validates the payload (via the DTO),
 * dispatches a command onto the command bus, and serializes the result. No
 * business rule lives here.
 */
final class CreateTaskController
{
    use HandleTrait;

    public function __construct(MessageBusInterface $commandBus)
    {
        $this->messageBus = $commandBus;
    }

    #[Route('/tasks', name: 'task_create', methods: ['POST'])]
    public function __invoke(#[MapRequestPayload] CreateTaskRequest $request): JsonResponse
    {
        /** @var TaskId $id */
        $id = $this->handle(new CreateTask($request->title));

        return new JsonResponse(['id' => $id->value], Response::HTTP_CREATED);
    }
}

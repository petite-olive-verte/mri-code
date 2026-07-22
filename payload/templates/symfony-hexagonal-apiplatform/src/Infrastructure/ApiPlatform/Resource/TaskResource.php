<?php

declare(strict_types=1);

namespace App\Infrastructure\ApiPlatform\Resource;

use ApiPlatform\Metadata\ApiProperty;
use ApiPlatform\Metadata\ApiResource;
use ApiPlatform\Metadata\Get;
use ApiPlatform\Metadata\Post;
use App\Domain\Model\Task;
use App\Infrastructure\ApiPlatform\State\CreateTaskProcessor;
use App\Infrastructure\ApiPlatform\State\TaskProvider;
use Symfony\Component\Validator\Constraints as Assert;

/**
 * API-facing DTO for a Task — an Infrastructure adapter. The domain model
 * (App\Domain\Model\Task) carries NO API Platform attribute; the HTTP shape
 * lives here and is bridged to the domain by the state Provider (read) and
 * Processor (write). Keeps the hexagon pure while exposing a REST API.
 */
#[ApiResource(
    shortName: 'Task',
    operations: [
        new Get(provider: TaskProvider::class),
        new Post(processor: CreateTaskProcessor::class),
    ],
)]
final class TaskResource
{
    public function __construct(
        #[ApiProperty(identifier: true, writable: false)]
        public ?string $id = null,
        #[Assert\NotBlank]
        #[Assert\Length(max: 255)]
        public string $title = '',
        #[ApiProperty(writable: false)]
        public ?string $status = null,
        #[ApiProperty(writable: false)]
        public ?\DateTimeImmutable $createdAt = null,
    ) {
    }

    public static function fromDomain(Task $task): self
    {
        return new self(
            $task->id()->value,
            $task->title(),
            $task->status()->value,
            $task->createdAt(),
        );
    }
}

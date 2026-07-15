<?php

declare(strict_types=1);

namespace App\Domain\Model;

use App\Domain\ValueObject\TaskId;
use App\Domain\ValueObject\TaskStatus;

/**
 * Task aggregate — pure domain model. No Doctrine attributes, no framework
 * imports: it is mapped from the outside via XML in Infrastructure. State
 * transitions go through intention-revealing methods, never public setters.
 */
final class Task
{
    private TaskStatus $status;

    private function __construct(
        private readonly TaskId $id,
        private readonly string $title,
        private readonly \DateTimeImmutable $createdAt,
    ) {
        $this->status = TaskStatus::Todo;
    }

    public static function create(TaskId $id, string $title, \DateTimeImmutable $now): self
    {
        $title = trim($title);
        if ('' === $title) {
            throw new \InvalidArgumentException('A task title cannot be empty.');
        }

        return new self($id, $title, $now);
    }

    public function markDone(): void
    {
        $this->status = TaskStatus::Done;
    }

    public function id(): TaskId
    {
        return $this->id;
    }

    public function title(): string
    {
        return $this->title;
    }

    public function status(): TaskStatus
    {
        return $this->status;
    }

    public function createdAt(): \DateTimeImmutable
    {
        return $this->createdAt;
    }
}

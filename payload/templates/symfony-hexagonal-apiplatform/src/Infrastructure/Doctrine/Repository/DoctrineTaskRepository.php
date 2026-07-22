<?php

declare(strict_types=1);

namespace App\Infrastructure\Doctrine\Repository;

use App\Domain\Model\Task;
use App\Domain\Repository\TaskRepository;
use App\Domain\ValueObject\TaskId;
use Doctrine\ORM\EntityManagerInterface;

/**
 * Driven adapter implementing the TaskRepository port with Doctrine ORM.
 * It returns domain objects and exposes only intention-revealing methods —
 * callers never see the EntityManager or a QueryBuilder.
 */
final readonly class DoctrineTaskRepository implements TaskRepository
{
    public function __construct(private EntityManagerInterface $em)
    {
    }

    public function save(Task $task): void
    {
        $this->em->persist($task);
        $this->em->flush();
    }

    public function ofId(TaskId $id): ?Task
    {
        return $this->em->find(Task::class, $id);
    }
}

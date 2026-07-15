<?php

declare(strict_types=1);

namespace App\Tests\Application;

use App\Application\Command\CreateTask;
use App\Application\Handler\CreateTaskHandler;
use App\Domain\ValueObject\TaskStatus;
use App\Tests\Double\FixedClock;
use App\Tests\Double\InMemoryTaskRepository;
use PHPUnit\Framework\Attributes\Test;
use PHPUnit\Framework\TestCase;

/**
 * Pure unit test of the use case: no kernel, no database, no HTTP. This is what
 * the hexagonal layout buys — fast, isolated tests of the business logic.
 */
final class CreateTaskHandlerTest extends TestCase
{
    #[Test]
    public function it_creates_and_stores_a_todo_task(): void
    {
        $tasks = new InMemoryTaskRepository();
        $handler = new CreateTaskHandler($tasks, new FixedClock(new \DateTimeImmutable('2026-01-01 00:00:00')));

        $id = $handler(new CreateTask('Write the spec'));

        $stored = $tasks->ofId($id);
        self::assertNotNull($stored);
        self::assertSame('Write the spec', $stored->title());
        self::assertSame(TaskStatus::Todo, $stored->status());
    }
}

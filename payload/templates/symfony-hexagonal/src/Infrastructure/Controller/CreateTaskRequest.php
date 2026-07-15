<?php

declare(strict_types=1);

namespace App\Infrastructure\Controller;

use Symfony\Component\Validator\Constraints as Assert;

/**
 * HTTP request DTO — lives at the edge and carries the validation constraints,
 * so the framework validates the payload before any use case runs. It is then
 * translated into the pure Application\Command\CreateTask command.
 */
final readonly class CreateTaskRequest
{
    public function __construct(
        #[Assert\NotBlank]
        #[Assert\Length(max: 255)]
        public string $title = '',
    ) {
    }
}

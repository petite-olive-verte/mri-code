<?php

declare(strict_types=1);

namespace App\Tests\Infrastructure;

use PHPUnit\Framework\Attributes\Test;
use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

/**
 * Functional smoke test of the driving adapter. It boots the kernel (which
 * validates the container and Doctrine mapping) and checks the validation
 * boundary — a blank title is rejected before any use case or DB access, so
 * this test stays green without a provisioned database.
 */
final class CreateTaskControllerTest extends WebTestCase
{
    #[Test]
    public function it_rejects_a_blank_title(): void
    {
        $client = self::createClient();
        $client->request(
            'POST',
            '/tasks',
            server: ['CONTENT_TYPE' => 'application/json'],
            content: (string) json_encode(['title' => '']),
        );

        self::assertResponseStatusCodeSame(422);
    }
}

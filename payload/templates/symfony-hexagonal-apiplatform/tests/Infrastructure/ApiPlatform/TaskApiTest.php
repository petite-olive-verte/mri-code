<?php

declare(strict_types=1);

namespace App\Tests\Infrastructure\ApiPlatform;

use PHPUnit\Framework\Attributes\Test;
use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

/**
 * Functional smoke test of the Task API resource. It hits the validation
 * boundary — a blank title is rejected before the state processor and any DB
 * access — so it stays green without a provisioned database. Full create/read
 * flow tests need a migrated test DB.
 */
final class TaskApiTest extends WebTestCase
{
    #[Test]
    public function it_rejects_a_blank_title(): void
    {
        $client = self::createClient();
        $client->request(
            'POST',
            '/api/tasks',
            server: ['CONTENT_TYPE' => 'application/ld+json', 'HTTP_ACCEPT' => 'application/ld+json'],
            content: (string) json_encode(['title' => '']),
        );

        self::assertResponseStatusCodeSame(422);
    }
}

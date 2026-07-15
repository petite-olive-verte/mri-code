<?php

declare(strict_types=1);

namespace App\Tests\Controller;

use App\Enum\HealthStatus;
use PHPUnit\Framework\Attributes\Test;
use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

/**
 * Smoke test: the kernel boots and the health endpoint answers. It also
 * demonstrates the functional-test style (WebTestCase) that infrastructure
 * adapters — controllers, CLI commands — should be covered with.
 */
final class HealthControllerTest extends WebTestCase
{
    #[Test]
    public function health_endpoint_reports_ok(): void
    {
        $client = self::createClient();
        $client->request('GET', '/health');

        self::assertResponseIsSuccessful();
        self::assertJson((string) $client->getResponse()->getContent());

        /** @var array{status: string, label: string} $payload */
        $payload = json_decode((string) $client->getResponse()->getContent(), true, 512, \JSON_THROW_ON_ERROR);

        self::assertSame(HealthStatus::Ok->value, $payload['status']);
    }
}

<?php

declare(strict_types=1);

namespace App\Controller;

use App\Enum\HealthStatus;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\Routing\Attribute\Route;

/**
 * Thin, invokable controller: it is an adapter at the edge of the app.
 * It does no business logic — it maps an HTTP call to a response. As the app
 * grows, controllers dispatch a command/query onto the Messenger bus and
 * serialize the result, keeping the domain free of the framework.
 */
final class HealthController
{
    #[Route('/health', name: 'health', methods: ['GET'])]
    public function __invoke(): JsonResponse
    {
        $status = HealthStatus::Ok;

        return new JsonResponse([
            'status' => $status->value,
            'label' => $status->label(),
        ]);
    }
}

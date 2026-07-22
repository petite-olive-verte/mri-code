<?php

declare(strict_types=1);

namespace App\Infrastructure\Symfony;

use Symfony\Bundle\FrameworkBundle\Kernel\MicroKernelTrait;
use Symfony\Component\HttpKernel\Kernel as BaseKernel;

/**
 * The Symfony application kernel — framework glue, so it lives in Infrastructure
 * (Domain and Application never reference it). `getProjectDir()` still resolves
 * the repo root by walking up to composer.json, so config/ paths are unaffected.
 */
final class Kernel extends BaseKernel
{
    use MicroKernelTrait;
}

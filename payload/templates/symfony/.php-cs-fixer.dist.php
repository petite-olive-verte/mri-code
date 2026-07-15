<?php

declare(strict_types=1);

$finder = PhpCsFixer\Finder::create()
    ->in(__DIR__.'/src')
    ->in(__DIR__.'/tests')
    ->exclude('.mri_code');

return (new PhpCsFixer\Config())
    ->setRiskyAllowed(true)
    ->setRules([
        '@Symfony' => true,
        '@Symfony:risky' => true,
        '@PSR12' => true,
        'declare_strict_types' => true,
        'native_function_invocation' => ['include' => ['@compiler_optimized'], 'scope' => 'namespaced'],
        // Keep global classes fully-qualified (\DateTimeImmutable) rather than importing them.
        'global_namespace_import' => ['import_classes' => false, 'import_functions' => false, 'import_constants' => false],
        'ordered_imports' => ['sort_algorithm' => 'alpha'],
        'no_unused_imports' => true,
        // Descriptive snake_case test method names (it_does_x) read better than camelCase.
        'php_unit_method_casing' => ['case' => 'snake_case'],
    ])
    ->setFinder($finder);

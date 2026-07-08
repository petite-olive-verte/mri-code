#!/usr/bin/env node
// Désinstalle le module « mri-code » d'un projet cible.
//   Usage : node bin/uninstall.mjs [target] [--yes|-y]
//   - target : dossier du projet (défaut : dossier courant)
//   - --yes / -y : ne pas demander confirmation
//
// Retire tout ce que l'install/update a déposé (skills, hooks, settings.json, AGENTS.md,
// CLAUDE.md, .mcp.json, miroir .agents/skills, config.json/constitution/models/templates dans
// .mri_code/). Ne touche JAMAIS .mri_code/docs/ : ce sont les documents produits par l'agent
// en cours de travail (brief/spec/plan...) — systématiquement conservés, avec ou sans --yes.
import fs from 'node:fs';
import { join } from 'node:path';
import readline from 'node:readline/promises';
import { MANAGED_PATHS, manifestPath, readManifest, rm } from './lib/core.mjs';

export async function runUninstall(argv) {
  const yes = argv.includes('--yes') || argv.includes('-y');
  const targetArg = argv.find((a) => !a.startsWith('-'));
  const TARGET = fs.realpathSync(targetArg || process.cwd());

  const manifest = readManifest(TARGET);
  const paths = manifest ? manifest.paths : MANAGED_PATHS;
  const existing = paths.filter((p) => fs.existsSync(join(TARGET, p)));

  if (existing.length === 0 && !fs.existsSync(manifestPath(TARGET))) {
    console.log(`Nothing to uninstall in ${TARGET}.`);
    return;
  }
  if (!manifest) {
    console.log('(No manifest found — using the current file list as a best-effort fallback; this install predates version tracking.)');
  }

  console.log(`==> Will remove from ${TARGET}:`);
  for (const p of existing) console.log(`    - ${p}`);
  console.log('    - .mri_code/.manifest.json');
  console.log('==> Preserved (never touched): .mri_code/docs/');

  if (!yes) {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    const ans = (await rl.question('Proceed? [y/N] ')).trim().toLowerCase();
    rl.close();
    if (ans !== 'y' && ans !== 'yes') { console.log('Aborted.'); return; }
  }

  for (const p of existing) rm(join(TARGET, p));
  rm(manifestPath(TARGET));

  // Nettoie les dossiers conteneurs devenus vides. Jamais .mri_code/ lui-même : docs/ doit survivre.
  for (const dir of ['.claude', '.agents']) {
    const p = join(TARGET, dir);
    if (fs.existsSync(p) && fs.readdirSync(p).length === 0) fs.rmdirSync(p);
  }

  console.log('==> Uninstalled. .mri_code/docs/ (if any) was kept.');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  await runUninstall(process.argv.slice(2));
}

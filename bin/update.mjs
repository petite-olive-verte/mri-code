#!/usr/bin/env node
// Met à jour un module « mri-code » déjà installé dans un projet cible, en place (COPIE).
//   Usage : node bin/update.mjs [target] [--lang <lang>] [--doc-lang <lang>] [--user <name>]
//   - target : dossier du projet (défaut : dossier courant), doit déjà contenir .mri_code/config.json
//   - les flags manquants réutilisent la config déjà enregistrée (pas de re-prompt)
//
// Re-dépose les fichiers du module (skills, hooks, settings, AGENTS.md, CLAUDE.md, .mcp.json,
// constitution, models, templates) et retire ceux devenus obsolètes entre deux versions.
// Ne touche JAMAIS .mri_code/docs/ : ce sont les documents produits par l'agent en cours de
// travail (brief/spec/plan...), toujours conservés.
import fs from 'node:fs';
import { join } from 'node:path';
import { deploy, mkdirp, readConfig, readManifest, rm, VERSION } from './lib/core.mjs';

export async function runUpdate(argv) {
  const flag = (n) => { const i = argv.indexOf(n); return i >= 0 && i + 1 < argv.length ? argv[i + 1] : null; };
  const TARGET = fs.realpathSync(mkdirp(argv.find((a) => !a.startsWith('--')) || process.cwd()));

  const existing = readConfig(TARGET);
  if (!existing) {
    console.error(`No mri-code installation found in ${TARGET} (.mri_code/config.json missing). Run the installer first.`);
    process.exit(1);
  }
  const lang = flag('--lang') ?? existing.communication_language;
  const docLang = flag('--doc-lang') ?? existing.document_language;
  const user = flag('--user') ?? existing.user_name ?? '';

  const oldManifest = readManifest(TARGET);
  console.log(`==> Updating mri-code module in: ${TARGET}`);
  console.log(`    lang=${lang} · doc-lang=${docLang} · user=${user || '(unset)'}` +
    (oldManifest ? ` · ${oldManifest.version} → ${VERSION}` : ` · → ${VERSION}`));

  const newManifest = deploy(TARGET, { lang, docLang, user });

  // Retire les chemins qui existaient dans l'ancienne installation mais plus dans la nouvelle
  // (fichier renommé/supprimé entre versions). .mri_code/docs/ n'apparaît jamais dans ces
  // listes, donc jamais concerné.
  if (oldManifest) {
    const kept = new Set(newManifest.paths);
    for (const p of oldManifest.paths) {
      if (!kept.has(p)) { rm(join(TARGET, p)); console.log(`    removed stale: ${p}`); }
    }
  }

  console.log('==> Update done.');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  await runUpdate(process.argv.slice(2));
}

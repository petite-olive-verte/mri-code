#!/usr/bin/env node
// Installe le module « mri-code » dans un projet cible (COPIE — pas de symlink).
//   Usage : node bin/install.mjs [target] [--lang <lang>] [--doc-lang <lang>] [--user <name>]
//   - target    : dossier du projet (défaut : dossier courant)
//   - --lang     : langue de communication de l'agent (défaut : English)
//   - --doc-lang : langue d'écriture des documents (défaut : = --lang)
//   - --user     : comment l'agent appelle l'utilisateur (défaut : vide)
//   En terminal interactif, les valeurs manquantes sont demandées ; sinon défauts (npx piped).
//
// Voir aussi : bin/update.mjs (mise à jour en place), bin/uninstall.mjs (retrait).
//
// Produit dans la cible :
//   .claude/  = skills · hooks · settings.json  (VRAIS FICHIERS, copiés ; les skills sont les slash /mri-code-*)
//   .mri_code/ = config.json · constitution.md · models.md · templates/ · docs/ (généré)
//   AGENTS.md CLAUDE.md .mcp.json à la racine ; .agents/skills/ (miroir Codex)
import fs from 'node:fs';
import readline from 'node:readline/promises';
import { deploy, mkdirp } from './lib/core.mjs';

export async function runInstall(argv) {
  const flag = (n) => { const i = argv.indexOf(n); return i >= 0 && i + 1 < argv.length ? argv[i + 1] : null; };
  const TARGET = fs.realpathSync(mkdirp(argv.find((a) => !a.startsWith('--')) || process.cwd()));

  // --- Config (flags, sinon prompt interactif, sinon défauts) ---
  let lang = flag('--lang'), docLang = flag('--doc-lang'), user = flag('--user');
  if (process.stdin.isTTY && (lang === null || user === null || docLang === null)) {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    if (lang === null) lang = (await rl.question('Communication language [English]: ')).trim();
    if (docLang === null) docLang = (await rl.question(`Document language [${lang || 'English'}]: `)).trim();
    if (user === null) user = (await rl.question('How should the agent address you? []: ')).trim();
    rl.close();
  }
  lang = lang || 'English';
  docLang = docLang || lang;
  user = user || '';

  console.log(`==> Installing mri-code module into: ${TARGET}`);
  console.log(`    lang=${lang} · doc-lang=${docLang} · user=${user || '(unset)'}`);
  deploy(TARGET, { lang, docLang, user });
  console.log('==> Done. Open an agent in the target (welcome message → /mri-code-brainstorm).');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  await runInstall(process.argv.slice(2));
}

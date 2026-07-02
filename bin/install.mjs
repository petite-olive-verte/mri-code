#!/usr/bin/env node
// Installe le module « mri » dans un projet cible (COPIE — pas de symlink).
//   Usage : node bin/install.mjs [target] [--lang <lang>] [--doc-lang <lang>] [--user <name>]
//   - target    : dossier du projet (défaut : dossier courant)
//   - --lang     : langue de communication de l'agent (défaut : English)
//   - --doc-lang : langue d'écriture des documents (défaut : = --lang)
//   - --user     : comment l'agent appelle l'utilisateur (défaut : vide)
//   En terminal interactif, les valeurs manquantes sont demandées ; sinon défauts (npx piped).
//
// Produit dans la cible :
//   .claude/  = skills · hooks · settings.json  (VRAIS FICHIERS, copiés ; les skills sont les slash /mri-*)
//   .mri_devtools/ = config.json · constitution.md · models.md · templates/ · docs/ (généré)
//   AGENTS.md CLAUDE.md .mcp.json à la racine ; .agents/skills/ (miroir Codex)
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import fs from 'node:fs';
import readline from 'node:readline/promises';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const PAYLOAD = join(SCRIPT_DIR, '..', 'payload');
const args = process.argv.slice(2);
const flag = (n) => { const i = args.indexOf(n); return i >= 0 && i + 1 < args.length ? args[i + 1] : null; };
const mkdirp = (p) => { fs.mkdirSync(p, { recursive: true }); return p; };
const cp = (src, dst) => fs.cpSync(src, dst, { recursive: true });

const TARGET = fs.realpathSync(mkdirp(args.find((a) => !a.startsWith('--')) || process.cwd()));
const MRI = join(TARGET, '.mri_devtools');

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

if (!fs.existsSync(PAYLOAD)) { console.error(`payload/ introuvable (${PAYLOAD})`); process.exit(1); }
console.log(`==> Installing mri module into: ${TARGET}`);
console.log(`    lang=${lang} · doc-lang=${docLang} · user=${user || '(unset)'}`);

// 1) .mri_devtools/ = config + data (PAS de skills ici)
mkdirp(join(MRI, 'docs'));
cp(join(PAYLOAD, 'constitution.md'), join(MRI, 'constitution.md'));
cp(join(PAYLOAD, 'models.md'), join(MRI, 'models.md'));
cp(join(PAYLOAD, 'templates'), join(MRI, 'templates'));
fs.writeFileSync(join(MRI, 'config.json'),
  JSON.stringify({ communication_language: lang, document_language: docLang, user_name: user }, null, 2) + '\n');

// 2) .claude/ = vrais fichiers copiés (les skills SONT les slash commands /mri-*, pas de dossier commands)
const cl = mkdirp(join(TARGET, '.claude'));
for (const sub of ['skills', 'hooks']) { fs.rmSync(join(cl, sub), { recursive: true, force: true }); cp(join(PAYLOAD, sub), join(cl, sub)); }
for (const h of fs.readdirSync(join(cl, 'hooks'))) fs.chmodSync(join(cl, 'hooks', h), 0o755);
cp(join(PAYLOAD, 'settings.json'), join(cl, 'settings.json'));

// 3) Racine + injection de la config dans AGENTS.md / CLAUDE.md
cp(join(PAYLOAD, 'AGENTS.md'), join(TARGET, 'AGENTS.md'));
cp(join(PAYLOAD, 'CLAUDE.md'), join(TARGET, 'CLAUDE.md'));
cp(join(PAYLOAD, 'mcp', 'servers.json'), join(TARGET, '.mcp.json'));
const subst = (p) => {
  if (!fs.existsSync(p)) return;
  let s = fs.readFileSync(p, 'utf8');
  s = s.replaceAll('{{COMMUNICATION_LANGUAGE}}', lang)
       .replaceAll('{{DOCUMENT_LANGUAGE}}', docLang)
       .replaceAll('{{USER_NAME}}', user || 'the user');
  fs.writeFileSync(p, s);
};
subst(join(TARGET, 'AGENTS.md'));
subst(join(TARGET, 'CLAUDE.md'));

// 4) Miroir Codex (copies)
const ag = mkdirp(join(TARGET, '.agents', 'skills'));
for (const name of fs.readdirSync(join(cl, 'skills'))) { fs.rmSync(join(ag, name), { recursive: true, force: true }); cp(join(cl, 'skills', name), join(ag, name)); }

console.log('==> Done. Open an agent in the target (welcome message → /mri-brainstorm).');

#!/usr/bin/env node
// Installeur du module « mri » dans un projet cible.
//   Usage : node bin/install.mjs [cible] [--copy]
//   - cible : dossier du projet (défaut : dossier courant)
//   - --copy : copie .claude/{skills,commands} au lieu de les lier (fallback si Claude ne
//              découvre pas les symlinks)
//
// Produit dans la cible :
//   .mri_devtools/   = LE MODULE (skills, commands, hooks, templates, constitution, models) + docs/ (généré)
//   .claude/         = câblage : commands (à plat), skills, hooks, settings.json
//   AGENTS.md CLAUDE.md .mcp.json à la racine ; .agents/skills/ (miroir Codex)
import { fileURLToPath } from 'node:url';
import { dirname, join, basename } from 'node:path';
import fs from 'node:fs';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const REPO = join(SCRIPT_DIR, '..');
const PAYLOAD = join(REPO, 'payload');

const args = process.argv.slice(2);
const MODE = args.includes('--copy') ? 'copy' : 'link';
const TARGET = fs.realpathSync(mkdirp(args.find(a => !a.startsWith('--')) || process.cwd()));
const MRI = join(TARGET, '.mri_devtools');

function mkdirp(p) { fs.mkdirSync(p, { recursive: true }); return p; }
function cp(src, dst) { fs.cpSync(src, dst, { recursive: true }); }
function link(rel, dst) { fs.rmSync(dst, { recursive: true, force: true }); fs.symlinkSync(rel, dst); }
function wire(srcDir, dstDir, relPrefix) {
  for (const name of fs.readdirSync(srcDir)) {
    const dst = join(dstDir, name);
    if (MODE === 'copy') { fs.rmSync(dst, { recursive: true, force: true }); cp(join(srcDir, name), dst); }
    else link(`${relPrefix}/${name}`, dst);
  }
}

if (!fs.existsSync(PAYLOAD)) { console.error(`payload/ introuvable (${PAYLOAD})`); process.exit(1); }
console.log(`==> Installation du module mri dans : ${TARGET}  (mode: ${MODE})`);

// 1) Module → .mri_devtools/
mkdirp(join(MRI, 'docs'));
for (const d of ['skills', 'commands', 'hooks', 'templates']) cp(join(PAYLOAD, d), join(MRI, d));
for (const f of ['constitution.md', 'models.md']) cp(join(PAYLOAD, f), join(MRI, f));

// 2) Câblage .claude/
mkdirp(join(TARGET, '.claude', 'skills'));
mkdirp(join(TARGET, '.claude', 'commands'));
mkdirp(join(TARGET, '.claude', 'hooks'));
wire(join(MRI, 'skills'), join(TARGET, '.claude', 'skills'), '../../.mri_devtools/skills');
wire(join(MRI, 'commands'), join(TARGET, '.claude', 'commands'), '../../.mri_devtools/commands');
for (const h of fs.readdirSync(join(MRI, 'hooks'))) {          // hooks toujours copiés (référencés par chemin)
  const dst = join(TARGET, '.claude', 'hooks', h);
  cp(join(MRI, 'hooks', h), dst); fs.chmodSync(dst, 0o755);
}
cp(join(PAYLOAD, 'settings.json'), join(TARGET, '.claude', 'settings.json'));

// 3) Racine
cp(join(PAYLOAD, 'AGENTS.md'), join(TARGET, 'AGENTS.md'));
cp(join(PAYLOAD, 'CLAUDE.md'), join(TARGET, 'CLAUDE.md'));
cp(join(PAYLOAD, 'mcp', 'servers.json'), join(TARGET, '.mcp.json'));

// 4) Miroir Codex
mkdirp(join(TARGET, '.agents', 'skills'));
wire(join(MRI, 'skills'), join(TARGET, '.agents', 'skills'), '../../.mri_devtools/skills');

console.log('==> OK. Ouvre un agent dans la cible (message d’accueil → /mri-brainstorm).');
if (MODE === 'link') console.log('    (Si Claude ne découvre pas les skills/commandes liées, relance avec --copy.)');

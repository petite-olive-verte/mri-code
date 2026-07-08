// Logique partagée par install / update / uninstall (bin/install.mjs, bin/update.mjs, bin/uninstall.mjs).
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import fs from 'node:fs';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url)); // bin/lib
export const REPO_ROOT = join(SCRIPT_DIR, '..', '..');
export const PAYLOAD = join(REPO_ROOT, 'payload');
export const VERSION = fs.readFileSync(join(REPO_ROOT, 'VERSION'), 'utf8').trim();

export const mkdirp = (p) => { fs.mkdirSync(p, { recursive: true }); return p; };
export const cp = (src, dst) => fs.cpSync(src, dst, { recursive: true });
export const rm = (p) => fs.rmSync(p, { recursive: true, force: true });

// Chemins (relatifs à TARGET) que l'outil possède entièrement : install les crée, update les
// réécrit, uninstall les retire. Calculés à partir du contenu réel de payload/ — les skills et
// hooks sont listés PAR NOM, jamais comme un dossier entier, pour ne jamais toucher un skill ou
// un hook que l'utilisateur aurait ajouté lui-même dans .claude/skills ou .claude/hooks.
// `.mri_code/docs/` n'y figure JAMAIS : ce sont les documents produits par l'agent pendant le
// travail (brief/spec/plan...) — on ne les touche jamais.
export function computeManagedPaths() {
  const skillNames = fs.readdirSync(join(PAYLOAD, 'skills'));
  const hookNames = fs.readdirSync(join(PAYLOAD, 'hooks'));
  return [
    'AGENTS.md',
    'CLAUDE.md',
    '.mcp.json',
    ...skillNames.map((n) => `.claude/skills/${n}`),
    ...hookNames.map((n) => `.claude/hooks/${n}`),
    '.claude/settings.json',
    ...skillNames.map((n) => `.agents/skills/${n}`),
    '.mri_code/constitution.md',
    '.mri_code/models.md',
    '.mri_code/templates',
    '.mri_code/config.json',
  ];
}
const MANIFEST_NAME = '.manifest.json';

export const manifestPath = (target) => join(target, '.mri_code', MANIFEST_NAME);

export function readManifest(target) {
  const p = manifestPath(target);
  if (!fs.existsSync(p)) return null;
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return null; }
}

export function readConfig(target) {
  const p = join(target, '.mri_code', 'config.json');
  if (!fs.existsSync(p)) return null;
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return null; }
}

function subst(p, { lang, docLang, user }) {
  if (!fs.existsSync(p)) return;
  let s = fs.readFileSync(p, 'utf8');
  s = s.replaceAll('{{COMMUNICATION_LANGUAGE}}', lang)
       .replaceAll('{{DOCUMENT_LANGUAGE}}', docLang)
       .replaceAll('{{USER_ADDRESS}}', user ? `as ${user}` : 'directly (no preferred name set)')
       .replaceAll('{{USER_NAME}}', user || 'the user');
  fs.writeFileSync(p, s);
}

// Dépose/écrase les fichiers du module dans TARGET, écrit config.json + le manifeste, et
// renvoie ce manifeste. Ne touche jamais à .mri_code/docs/. Utilisé par install ET update.
export function deploy(target, { lang, docLang, user }) {
  if (!fs.existsSync(PAYLOAD)) throw new Error(`payload/ introuvable (${PAYLOAD})`);
  const MRI = join(target, '.mri_code');

  mkdirp(join(MRI, 'docs'));
  cp(join(PAYLOAD, 'constitution.md'), join(MRI, 'constitution.md'));
  cp(join(PAYLOAD, 'models.md'), join(MRI, 'models.md'));
  rm(join(MRI, 'templates'));
  cp(join(PAYLOAD, 'templates'), join(MRI, 'templates'));
  fs.writeFileSync(join(MRI, 'config.json'),
    JSON.stringify({ communication_language: lang, document_language: docLang, user_name: user }, null, 2) + '\n');

  // .claude/skills et .claude/hooks : on gère chaque entrée du payload PAR NOM (on ne vide/écrase
  // jamais le dossier entier), pour ne jamais toucher un skill ou un hook ajouté par l'utilisateur.
  const clSkills = mkdirp(join(target, '.claude', 'skills'));
  const skillNames = fs.readdirSync(join(PAYLOAD, 'skills'));
  for (const name of skillNames) {
    rm(join(clSkills, name));
    cp(join(PAYLOAD, 'skills', name), join(clSkills, name));
    // Make skill scripts executable too (parity with hooks — they are invoked by bare path).
    const sdir = join(clSkills, name, 'scripts');
    if (fs.existsSync(sdir)) for (const s of fs.readdirSync(sdir)) fs.chmodSync(join(sdir, s), 0o755);
  }

  const clHooks = mkdirp(join(target, '.claude', 'hooks'));
  for (const name of fs.readdirSync(join(PAYLOAD, 'hooks'))) {
    rm(join(clHooks, name));
    cp(join(PAYLOAD, 'hooks', name), join(clHooks, name));
    fs.chmodSync(join(clHooks, name), 0o755);
  }

  cp(join(PAYLOAD, 'settings.json'), join(target, '.claude', 'settings.json'));

  cp(join(PAYLOAD, 'AGENTS.md'), join(target, 'AGENTS.md'));
  cp(join(PAYLOAD, 'CLAUDE.md'), join(target, 'CLAUDE.md'));
  cp(join(PAYLOAD, 'mcp', 'servers.json'), join(target, '.mcp.json'));
  subst(join(target, 'AGENTS.md'), { lang, docLang, user });
  subst(join(target, 'CLAUDE.md'), { lang, docLang, user });

  // Miroir Codex (copies) — même principe : uniquement les skills du payload, par nom.
  const ag = mkdirp(join(target, '.agents', 'skills'));
  for (const name of skillNames) { rm(join(ag, name)); cp(join(clSkills, name), join(ag, name)); }

  const manifest = { version: VERSION, installedAt: new Date().toISOString(), paths: computeManagedPaths() };
  fs.writeFileSync(manifestPath(target), JSON.stringify(manifest, null, 2) + '\n');
  return manifest;
}

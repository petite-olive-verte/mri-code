#!/usr/bin/env node
// Point d'entrée unique (npx mri-code ...). Sous-commandes :
//   npx mri-code [target] [--lang ..] [--doc-lang ..] [--user ..]   install (défaut)
//   npx mri-code update [target] [--lang ..] [--doc-lang ..] [--user ..]
//   npx mri-code uninstall [target] [--yes]        (alias : remove)
const argv = process.argv.slice(2);
const [cmd, ...rest] = argv;

if (cmd === 'update') {
  const { runUpdate } = await import('./update.mjs');
  await runUpdate(rest);
} else if (cmd === 'uninstall' || cmd === 'remove') {
  const { runUninstall } = await import('./uninstall.mjs');
  await runUninstall(rest);
} else if (cmd === 'install') {
  const { runInstall } = await import('./install.mjs');
  await runInstall(rest);
} else {
  // Pas de sous-commande reconnue : comportement historique — installation par défaut,
  // le premier argument (s'il n'est pas un flag) est le dossier cible.
  const { runInstall } = await import('./install.mjs');
  await runInstall(argv);
}

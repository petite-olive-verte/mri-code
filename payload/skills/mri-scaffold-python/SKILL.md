---
name: mri-scaffold-python
description: Use when initializing/scaffolding the Python project structure (uv + ruff + pytest + mypy, src/ layout) from .mri_devtools/templates/python-uv, once the spec and plan are ready and before writing feature code. Respects .mri_devtools/constitution.md.
---

# Scaffold d'un projet Python (uv + ruff + pytest)

Génère la structure d'un projet Python à partir de `.mri_devtools/templates/python-uv/`, en respectant
`.mri_devtools/constitution.md`. À utiliser **après** la spec et le plan, **avant** d'écrire le code des features.

## Avant de commencer
1. **Lis `.mri_devtools/constitution.md`** : applique sa stack et ses conventions. Si elles diffèrent du template,
   la constitution prime — adapte les fichiers générés en conséquence.
2. Détermine deux noms (déduis-les de la spec, sinon demande à l'utilisateur) :
   - `PROJECT_NAME` : nom de distribution (peut contenir des tirets), ex. `todo-api`.
   - `PACKAGE_NAME` : nom d'import Python, `snake_case`, ex. `todo_api`.
   - `PROJECT_DESCRIPTION` : une phrase.

## Procédure
Le projet se génère **à la racine du repo** (l'app vit dans le même dépôt que la toolbox).
N'écrase **aucun** fichier existant : si un fichier cible existe déjà (ex. `README.md`,
`.gitignore`), garde l'existant et signale-le à l'utilisateur.

```bash
# Depuis la racine du repo. Adapte les 3 variables.
PROJECT_NAME="todo-api"
PACKAGE_NAME="todo_api"
PROJECT_DESCRIPTION="Petite API de todo."

SRC=".mri_devtools/templates/python-uv"
# Copie les fichiers du template sans écraser l'existant (-n), en incluant les fichiers cachés.
cp -rn "$SRC/." . 2>/dev/null || true

# Renomme le package
if [ -d "src/__PACKAGE_NAME__" ]; then
  mv "src/__PACKAGE_NAME__" "src/$PACKAGE_NAME"
fi

# Substitue les jetons dans TOUS les fichiers du projet (hors .git/.venv)
grep -rlZ '__PACKAGE_NAME__\|__PROJECT_NAME__\|__PROJECT_DESCRIPTION__' . \
  --exclude-dir=.git --exclude-dir=.venv 2>/dev/null | \
  xargs -0 sed -i \
    -e "s/__PROJECT_DESCRIPTION__/$PROJECT_DESCRIPTION/g" \
    -e "s/__PROJECT_NAME__/$PROJECT_NAME/g" \
    -e "s/__PACKAGE_NAME__/$PACKAGE_NAME/g"
```

## Vérification (obligatoire avant de continuer)
```bash
uv sync                 # crée l'env + installe les dépendances dev
uv run pytest -q        # le smoke test doit passer (vert)
uv run ruff check .     # lint propre
```
- Si `pytest` ou `ruff` échouent, **corrige avant** de passer à l'implémentation.
- Vérifie qu'il **ne reste aucun** jeton `__PACKAGE_NAME__` / `__PROJECT_NAME__` :
  `grep -rn '__P[A-Z_]*__' . --include='*.py' --include='*.toml'` doit être vide.

## Ensuite
Passe à l'implémentation **en TDD** via **/mri-implement** (skill `mri-tdd` par tâche), feature par feature,
en traduisant les **critères d'acceptation de la spec** en tests qui échouent d'abord.

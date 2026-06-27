# Constitution du projet

> **Le règlement non-négociable de ce projet.** L'agent le lit à chaque session et s'y conforme.
> La spec dit *quoi* construire ; cette constitution dit *ce que « bien fait » veut dire ici*.
> **Édite ce fichier** pour imposer tes préférences — il prime sur les habitudes par défaut de l'agent.

## Stack (non-négociable)
- **Python 3.12+**.
- **uv** pour l'environnement et les dépendances (jamais `pip`/`poetry`/`venv` à la main).
- **Ruff** pour le lint **et** le format (pas de black/flake8/isort séparés).
- **ty** (Astral) pour le typage si dispo, sinon **mypy** en repli.
- **pytest** (+ `pytest-cov`) pour les tests.
- **pre-commit** pour les garde-fous avant commit.
- Config centralisée dans **`pyproject.toml`** (source unique ; pas de setup.cfg/requirements.txt).

## Qualité de code
- Tout le code public est **typé** ; `ruff check` et le type-checker doivent passer (zéro erreur).
- Docstrings sur les modules et fonctions publiques (style court, pas de roman).
- Préfère des fonctions petites et la **composition** à l'héritage.
- Pas de secret en dur ; configuration via variables d'environnement (`.env`, non commité).
- Pas d'`except` nu ; gère les erreurs explicitement.

## Tests (TDD obligatoire)
- **Red-Green-Refactor** : écrire un test qui échoue **avant** l'implémentation.
- L'humain / la spec possède l'**intention** du test ; l'agent l'**implémentation**.
- Les **critères d'acceptation de la spec deviennent des tests**.
- Couverture cible **≥ 80 %** ; au moins un test d'intégration par point d'entrée public (API/CLI).
- Les tests doivent passer (`pytest`) et le lint être propre avant de considérer une tâche terminée.

## Architecture
- Layout **`src/`** : code dans `src/<package>/`, tests dans `tests/`.
- La **logique métier** n'importe pas le framework web / l'I/O (garde le cœur testable).
- Dépendances orientées vers l'intérieur (I/O et frameworks en périphérie).

## Structure & nommage
- `tests/` **miroir** de `src/` (un module ↔ un fichier de test `test_<module>.py`).
- `snake_case` pour fichiers/fonctions/variables, `PascalCase` pour les classes.
- Documentation et artefacts de spec dans `docs/` (`docs/specs/<feature>/`).

## Workflow
- Commits petits et atomiques, message à l'impératif décrivant le *pourquoi*.
- Ne jamais `git push --force` ; ne jamais commiter de secrets ni le dossier `.venv`.

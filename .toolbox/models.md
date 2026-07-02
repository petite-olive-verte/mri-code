# Suggestions de modèle par étape (non forcées, éditable)

> Les commandes `mri-*` affichent une **suggestion** de modèle en fin d'étape (jamais imposée). Adapte
> cette table à tes providers/budget. Principe : **modèle « cerveau » cher** pour l'archi/le raisonnement,
> **modèle « bras » économe** pour le code en volume.

| Étape / commande | Type de tâche | Modèle suggéré | Pourquoi |
|---|---|---|---|
| `/mri-brainstorm` | idéation / cadrage | **Opus** | raisonnement ouvert, challenge |
| `/mri-forge` | pressure-test adversarial | **Opus** | argumentation multi-personas |
| `/mri-design` | architecture | **Opus** | conception multi-fichiers, trade-offs |
| `/mri-devplan` | planification | **Opus** | découpe en tâches, code complet |
| `/mri-elicit`, `/mri-adversarial-review` | critique / audit | **Opus** | profondeur de critique |
| `/mri-meta-prompt` | méta-prompting | **Opus** | reformulation précise |
| `/mri-*-research` | recherche web | **Sonnet** | rapide, synthèse sourcée |
| `/mri-scaffold-python` | mécanique | **Sonnet / DeepSeek-v4** | déterministe, peu de raisonnement |
| `/mri-implement` | code en volume (TDD) | **Sonnet / DeepSeek-v4** | économe, itératif |
| `/mri-debug` | débogage | **Sonnet / DeepSeek-v4** | cycles courts ; Opus si cause coriace |
| `/mri-review` | revue de code | **Sonnet** (ou **Opus** si exigeant) | lecture critique |
| `/mri-finish` | intégration git | indifférent | mécanique |

## Providers
- **Opus / Sonnet** : Claude Code natif (`/model`).
- **DeepSeek-v4** : très bon rapport coût/efficacité pour le code — à ajouter comme provider dans Claude
  Code (voir la config provider). Bon défaut « bras » quand le budget compte.

> Rien n'est automatique : ce sont des *suggestions*. Change de modèle avec `/model` si tu le souhaites.

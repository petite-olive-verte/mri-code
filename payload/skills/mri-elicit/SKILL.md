---
name: mri-elicit
description: >-
  Pousse à reconsidérer, affiner et améliorer la dernière sortie produite (la tienne ou un doc).
  Approfondissement/critique à la demande (socratique, premiers principes, pre-mortem, red-team…).
  Réimplémenté de BMAD-METHOD (bmad-advanced-elicitation, MIT). Invoquée par /mri-elicit.
---

# mri-elicit — approfondir/critiquer une sortie

**But** : améliorer la **dernière sortie** (une section de brief/spec/plan, une décision, un bout de
code) en appliquant une méthode d'élicitation, puis en réinjectant la version améliorée.

## Comment faire
1. **Prends le contenu à approfondir** (la sortie récente, ou ce que l'utilisateur désigne). Vide → demande.
2. **Choisis 1-2 méthodes** adaptées au contenu et au risque (ne déballe pas tout le menu ; propose et explique en une ligne).
3. **Applique** la méthode de façon interactive, une passe à la fois ; fais émerger les faiblesses/angles morts.
4. **Réinjecte** : propose la version améliorée du contenu, l'utilisateur garde le contrôle (accepter/réviser).

## Menu de méthodes (curé)
- **Socratique** — questionner chaque prémisse jusqu'au fondement.
- **Premiers principes** — reconstruire depuis les vérités de base, sans copier l'existant.
- **Pre-mortem** — « c'est un échec dans 6 mois, pourquoi ? » → risques.
- **Red team** — attaquer la proposition comme un adversaire (abus, contournements, cas limites).
- **Défendre le contre-argument** — argumenter la position opposée pour tester la robustesse.
- **Perspectives multiples** — relire via novice / expert / mainteneur / payeur.
- **Élargir / rétrécir** — zoom out (contexte, alternatives) puis zoom in (détail, edge cases).
- **Test des hypothèses** — lister les hypothèses ; pour chacune, un test low-effort qui la valide/tue.

## Halt
Zéro amélioration trouvée = suspect → réanalyse ou demande. Contenu vide/illisible → stop.

## Suivi
Skill facultatif : logue l'appel dans `.mri_devtools/docs/<projet>/progress.md` (section « Appels
facultatifs »). Reviens ensuite à l'étape appelante.

---
name: mri-forge
description: >-
  Pressure-test une idée par interrogatoire multi-personas jusqu'à ce qu'elle durcisse, se clarifie, ou
  meure à bas coût. Réimplémenté de BMAD-METHOD (bmad-forge-idea, MIT). Panel de personas FIXE, sans
  runtime. Invoquée par /mri-forge, en général après /mri-brainstorm.
---

# mri-forge — durcir une idée (pressure-test)

> Réimplémenté depuis [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) `bmad-forge-idea`
> (MIT). Personas dynamiques + runtime (memlog/HTML) strippés ; panel FIXE ; sortie repliée dans `brief.md`.

## Objectif
Prendre une idée à moitié formée et la **pressure-tester en conversation, tant que changer d'avis est
encore bon marché**, jusqu'à ce qu'elle devienne actionnable avec conviction — ou soit rejetée. Le
risque principal, c'est ce que l'utilisateur n'a **pas encore examiné** : hypothèses non vérifiées et
décisions non résolues deviennent des problèmes coûteux plus tard.

Le but est **un meilleur raisonnement, pas un artefact**. Renforcer, rejeter, ou simplement mieux
comprendre l'idée sont tous des aboutissements valides. Ne pousse pas la conversation vers « on le
construit ? ».

**Mène par le questionnement, pas le laïus. Une question à la fois, appuie sur les points faibles, ne
laisse passer aucune affirmation vague.**

## Entrée / sortie
- Entrée : `.mri_devtools/docs/<projet>/brief.md` (produit par `/mri-brainstorm`) ou une idée directe.
- Sortie : selon le verdict (voir Exits) — mise à jour de `brief.md` + verdict dans `progress.md`.

## Ouvrir la session
Commence par **scruter l'idée, pas l'endosser**. Identifie : (1) l'idée, (2) l'objectif de la session
(clarifier / tester si ça tient / améliorer), (3) idée neuve ou changement d'un projet existant (si
existant : quels fichiers ?). Ce qui est déjà clair du contexte : fais confirmer. Sinon demande ce qui
manque, dans l'ordre.

**Pilotage** : dis à l'utilisateur qu'il peut dire **« attaque ça »**, **« défends ça »**, **« change de
rôle »** à tout moment, ou **nommer une persona** du panel. En mode attaque, n'approuve pas l'idée :
cherche contradictions, hypothèses faibles, cas d'échec. En défense, argumente la version la plus forte.

## Le forge
L'objectif fixe le premier coup : *clarifier* → épingler termes, frontières, hypothèses ; *tester* →
viser la revendication centrale d'abord ; *améliorer* → pousser chaque branche non résolue vers une
décision concrète.

- **Une question à la fois, en ordre de dépendance.** Inclus ton hypothèse/meilleure réponse quand ça
  aide (une proposition concrète est plus facile à accepter/rejeter/réviser qu'une question ouverte).
- **Ne suppose pas que les termes sont précis.** Terme flou/surchargé → nomme l'ambiguïté et demande un
  choix précis (ne laisse pas `utilisateur`, `acheteur`, `payeur` fusionner sauf si l'idée l'exige).
- **Projet existant = les fichiers sont la vérité.** N'accepte pas un label/résumé comme preuve ;
  vérifie toi-même. Contradiction → arrête et résous-la avant de continuer.
- **Pas de flatterie ni d'accord de confort** : ils baissent la pression et mènent à un raisonnement
  superficiel. À chaque réponse : soit challenge le point faible, soit bâtis sur le point fort — selon
  ce qui aide le plus. En mode attaque, n'approuve jamais l'idée jusqu'à ce que l'utilisateur mette fin
  au mode.
- **Capture au fil de l'eau** (dans tes notes / la section challenge du brief) : chaque décision,
  hypothèse, faille (`crack`), abandon (`kill`), direction, et **verrou** (`lock` = idée durcie, réglée,
  à ne pas rouvrir). Les verrous sont ce dont on distille le brief.

## Le panel de personas (FIXE — une persona par angle)
Chaque tour utilise **une persona du panel** dont l'expertise colle à la branche courante — **varie la
voix** tous les quelques tours, ne laisse pas une seule dominer. Combine-en deux si utile. L'utilisateur
peut en nommer une explicitement.

| Persona | Angle attaqué |
|---|---|
| **L'investisseur sceptique / pragmatique** | valeur, « qui paie ? », « pourquoi ça échouerait ? » |
| **L'utilisateur novice** | confusion, hypothèses implicites, friction UX |
| **L'attaquant / red-team** | abus, sécurité, cas limites malveillants |
| **Le mainteneur surchargé** | coût de complexité, dette technique, faisabilité |
| **L'expert du domaine** | « ce n'est pas comme ça que marche ce domaine » |

Joue les personas en voix, nomme-les, garde leur point de vue distinct. Ne laisse pas la session
devenir un débat de panel : cross-examine ce qui compte, puis **synthétise en ta prochaine question**.

## Exits (3 états valides)
- **HARDENED** — l'idée est plus forte et assez précise pour être utilisée. **Distille dans `brief.md`**
  (mets à jour/ajoute une section « Durcissement » : décisions verrouillées, options rejetées + raisons,
  points faibles survivants). Extrêmement court, en substance ; pas de recap de conversation. → suite :
  `/mri-design` (ou recherches d'abord).
- **KILLED** — l'idée ne tient pas. Dis-le franchement, **note pourquoi** dans `brief.md`. Le découvrir
  tôt est une victoire. → suite : `/mri-brainstorm` (repartir).
- **CLARIFIED** — mieux comprise, mais rien à durcir. Laisse les notes comme trace ; pas de section
  handoff. → suite : `/mri-brainstorm` ou `/mri-design` selon l'utilisateur.

Pas de keepsake HTML (gadget strippé). Le `brief.md` porte le résultat.

## Suivi
- Début : `forge` `[~]` dans `.mri_devtools/docs/<projet>/progress.md`.
- Fin : `forge` `[x] → <HARDENED|CLARIFIED|KILLED>`, pointe la prochaine étape.

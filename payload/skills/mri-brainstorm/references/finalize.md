# Wrap-Up : synthèse & brief

À charger quand l'utilisateur est épuisé ou le sujet miné. Tes notes de session sont la matière ; tout
ici en dérive.

## Synthèse (en deux temps, dans l'ordre)
1. **Tends-leur le miroir d'abord.** Reflète un échantillon vivant de *leurs* idées — inclus
   délibérément les bizarres/enfouies, pas seulement les évidentes récentes. Demande ce qu'ils voient
   maintenant : conclusions, synergies, thèmes, les quelques-unes qui comptent vraiment. Laisse-les
   connecter en premier — leur reconnaissance de motifs est le point.
2. **Puis ajoute les connexions qu'ils rateraient.** Penche-toi créativement — non pas de nouvelles
   idées brutes, mais les liens non évidents : cette idée de la technique 1 résout la tension de la
   technique 4 ; ces trois n'en sont qu'une sous trois casquettes ; ce wildcard est la vraie percée.

## Produire le brief
Écris **`.mri_devtools/docs/<projet>/brief.md`** en t'appuyant sur `assets/brief-template.md` (adapte
agressivement : supprime les sections qui ne méritent pas leur place, ajoute ce que le produit exige).
Le brief doit contenir, a minima : problème, utilisateurs, solution/valeur, périmètre (in/out),
**critères de succès mesurables**, et les hypothèses/risques ouverts. C'est l'artefact de handoff pour
`/mri-forge` (challenge) puis `/mri-design`.

Pas de keepsake HTML ni de journal externe : le `brief.md` **est** le livrable. Reste concis et « on
point » — le budget de tokens compte pour la suite du pipeline.

## Fin
Mets à jour `progress.md` (brainstorm → `[x]`), puis indique la suite :
« Prochaine étape → `/mri-forge` pour durcir l'idée, ou `/mri-design` si elle est déjà solide. »

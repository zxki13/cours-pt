# Cours de prépa PT

Mes cours manuscrits, en libre accès. Le site se met à jour tout seul quand j'ajoute des fichiers dans `cours/`.

## Ajouter un cours

1. Sur la page du dépôt GitHub, ouvre le dossier `cours`, puis la matière (ou crée-la).
2. Clique sur **Add file → Upload files**, glisse tes PDF, puis **Commit changes**.
3. Attends environ une minute : la liste du site se régénère automatiquement.

Organisation :

    cours/Mathematiques/01-Reduction.pdf
    cours/Physique-Chimie/Thermodynamique/02-Premier-principe.pdf

- Un sous-dossier devient un chapitre.
- Les chiffres au début du nom servent à trier et ne s'affichent pas.
- Évite les accents dans les noms de dossiers.

## Personnaliser

Modifie `site.json` (titre, description, mention de licence) avec le crayon ✏️ sur GitHub.

## Si la liste ne se met pas à jour

Onglet **Actions** du dépôt : si le dernier passage est en rouge, va dans **Settings → Actions → General → Workflow permissions**, choisis **Read and write permissions**, puis relance le passage (**Re-run all jobs**).
Sinon, tu peux générer la liste toi-même : `python3 scripts/generer.py`, puis envoie le fichier `cours.json` modifié sur GitHub.

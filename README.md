# GenerateurPseudoAleatoireSNCF

Génère un nombre pseudo-aléatoire en utilisant le nombre de trains en retard et annulés de la SNCF.

Les données en temps réel sont récupérées via l'API SNCF. Elles servent à initialiser un modèle de double pendule (système chaotique).

Evidemment la répartition n'est pas uniforme ce qui en fait un générateur plutôt mauvais mais qui a le mérite d'être fun non?

## Utilisation

1. Renseigner votre clé API SNCF dans le fichier (`KEY`).
2. Lancer le script :
   ```bash
   python3 generateur.py
   ```

## Dépendances

- `requests`
- `numpy`
- `scipy`

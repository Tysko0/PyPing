<div align="center">
  <h2>PyPing</h2>
  <p>Une application de bureau open source permettant de tester la connectivité réseau grâce aux requêtes ping.</p>

  <img src="https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge" alt="Version 1.0.0">
  
  <a href="https://github.com/Tysko0/PyPing/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="Licence MIT">
  </a>
</div>

## Technologies utilisées

<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/GUI-Tkinter-306998?style=for-the-badge&logo=python&logoColor=white" alt="Tkinter">

## Fonctionnalités

- Test de connectivité réseau par ping.
- Prise en charge des noms de domaine et des adresses IP.
- Intervalle configurable entre les requêtes.
- Affichage du résultat du dernier ping.
- Mesure de la latence en millisecondes.
- Démarrage et arrêt du test à tout moment.
- Interface graphique sombre et minimaliste.
- Détection automatique d'un hôte inactif après 3 échecs consécutifs
- Statistiques : paquets envoyés, reçus, perdus et latences min./moy./max.
- Compatibilité Windows et Linux.

## Installation

### Prérequis

- Python 3.10 ou supérieur.
- Tkinter 

### Cloner le dépôt

```bash
git clone https://github.com/Tysko0/PyPing.git
cd PyPing
pip install -r requirements.txt
```

### Lancer l'application

**Windows :**

```powershell
py main.py
```

**Linux :**

```bash
python3 main.py
```

## Structure du projet

```text
PyPing/
├── main.py
├── components/
│   ├── __init__.py
│   ├── home.py
│   ├── stats.py
│   └── ping.py
└── services/
    ├── __init__.py
    ├── stats.py
    └── ping.py
```

## Licence

Ce projet est distribué sous licence MIT. Consulte le fichier `LICENSE` pour plus d'informations.

## Auteur

Développé par Tysko
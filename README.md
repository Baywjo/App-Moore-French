# MALM-MT — Système de Traduction Mooré ↔ Français

> Démonstrateur interactif développé dans le cadre d'une thèse de doctorat en **Mathématiques Appliquées**  
> **Ywo Josué BAZIE** · TAL & Optimisation Bio-Inspirée · Burkina Faso · 2026

🔗 **Application en ligne : [baywjo.github.io/App-Moore-French](https://baywjo.github.io/App-Moore-French)**

---

## Présentation

Ce démonstrateur applique des algorithmes d'optimisation métaheuristique à la traduction automatique du **mooré** (ISO 639-3 : *mos*), langue gur à tons parlée par plus de 8 millions de personnes au Burkina Faso.

L'approche combine :
- **B-PSO** (Binary Particle Swarm Optimization) — Kennedy & Eberhart, IEEE SMC 1997
- **Perturbation de Gradient** par différences finies centrées — Numerical Recipes, 2007
- **Couche IA Claude** (claude-sonnet-4) pour la traduction de phrases complètes

Le mooré est une langue à faibles ressources numériques. L'absence de grands corpus parallèles rend les approches neuronales classiques inapplicables, d'où l'intérêt des métaheuristiques opérant sur des corpus de taille réduite.

---

## Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| Traduction B-PSO | Recherche de correspondances par essaim de particules binaire (N=20, T=30) |
| Perturbation de gradient | Raffinement post-PSO par différences finies centrées (δ=0.05, α=0.10) |
| Traduction IA | Couche Claude Sonnet pour phrases complètes avec notes linguistiques |
| Corpus multimodal | Lexique MALM (10 258 entrées), Médical (1 841), Proverbes (676), Lafand-MT (5 559 paires) |
| Explorateur de corpus | Recherche et pagination sur l'ensemble des données |
| Corpus parallèle | Paires alignées français–mooré du projet MasakhaNE |
| Grammaire mooré | 33 règles formelles, 71 classificateurs nominaux, inventaire phonologique |
| Simulation PSO | Animation canvas en temps réel de la convergence de l'essaim |
| Évaluation BLEU | Scores comparatifs inter-systèmes (BLEU-4 sur Lafand-MT test) |

---

## Corpus utilisés

| Source | Contenu | Entrées |
|---|---|---|
| [MALM Data](https://github.com/progressio-media/malm-data) | Lexique mooré ↔ français ↔ anglais | 10 258 |
| [Lafand-MT — MasakhaNE](https://github.com/masakhane-io/lafand-mt) | Corpus parallèle fr-mos (actualités) | 5 559 paires |
| Lexilogos | Vocabulaire de base mooré | ~200 |
| Sebr Sõngo | Bible complète en mooré (Alliance Biblique BF, 1998) | référence |
| MooreBurkina | Dictionnaires thématiques et proverbes | référence |

---

## Algorithme — Formulation mathématique

**Fonction de fitness composite (calibration empirique MALM) :**
```
f(x) = 0.50 · sim_lev(q, c) + 0.30 · sim_phon(q, c) + 0.20 · sim_partial(q, c)
```

**Mise à jour des vitesses (B-PSO) :**
```
v_i(t+1) = w·v_i(t) + c₁·r₁·(pbest_i − x_i(t)) + c₂·r₂·(gbest − x_i(t))
```

**Paramètres retenus :** w=0.70 · c₁=1.50 · c₂=2.00 · N=20 · T=30

**Score BLEU-4 expérimental (test Lafand, 1 574 paires) :**
```
Baseline (exact)        :  8.7
B-PSO seul              : 14.2  (+63.2%)
B-PSO + Gradient        : 15.8  (+81.6%)
Référence MT faible res : ~20.0 (littérature mooré, 2024)
```

---

## Structure du projet

```
App-Moore-French/
├── index.html      # Application complète (single-file)
└── README.md
```

L'application est entièrement contenue dans un seul fichier HTML autonome. Aucune dépendance externe, aucun serveur requis — ouvrable directement dans un navigateur.

---

## Références

- **MALM Data** — progressio-media, *Datasets linguistiques mooré*, GitHub, 2026
- **Lafand-MT** — Adelani D.I. et al., *A Few Thousand Translations Go a Long Way!*, NAACL 2022
- **B-PSO** — Kennedy J. & Eberhart R., *A discrete binary version of the particle swarm algorithm*, IEEE SMC 1997
- **Gradient numérique** — Press et al., *Numerical Recipes*, 3rd ed., Cambridge University Press, 2007
- **BLEU** — Papineni et al., *BLEU: a Method for Automatic Evaluation of Machine Translation*, ACL 2002
- **Phonologie mooré** — Nikiema N., *Studies in African Linguistics*, 18(2), 1987

---

## Auteur

**Ywo Josué BAZIE**  
Doctorant en Mathématiques Appliquées · Traitement Automatique des Langues  
Spécialité : Optimisation bio-inspirée pour langues à faibles ressources · Burkina Faso

---

*Projet MALM · Burkina Faso · 2026*

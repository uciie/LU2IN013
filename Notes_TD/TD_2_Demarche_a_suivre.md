# Séance de Td n°2 : Retour sur l'organistaion et les objectifs.

## Notes en vrac :

- Chaque semaine, avoir un **objectif** sur ce qui va être présenter le mercredi prochain (Penser à la **relation client**).

- L'apprentissage et les formations doivent toujours **servir le projet**. Donc lorsqu'on fait des exercices d'apprentissage, il faut les faire **directement sur le projet**.

- Les **réunions** doivent se faire dans l'idéal **vendredi ou samedi**. Elles servent à se mettre au point sur **l'avancement du sprint** de la semaine. La mise en place du **sprint** doit être finie le **mercredi** pendant le TME dans l'idéal.

- La réunion est un moment de **brainstorming** où chacun apporte ses idées utiles à l'avancement du projet et à la réalistaion du rpojet de la semaine.

- Le sprint doit contenir au alentour de **15 à 20 tâches** par semaine. 

- Les **temps consacrés** aux tâches du sprint doivent être le plus précis posible.

## Pour cette semaine :

- Mettre en place **l'environnement** et le **robot**.

- Démo possible : faire **bouger le robot** dans son environnement en montrant qu'il a changé de coordonnées par exemple.

## Comment faire : Les classes.

**Environnement :**

- L'**environnement** va permettre de **repérer/positionner** le robot dans l'espace.

- Modélisation :

| Matrice (représentaion discrète) |  Forme géometrique (représentaion continue)        |
| :--------------- |---------------:|
|  |   |
| **Représenation**  |         |
| nb lignes  | largeur |
| nb colonnes  | longueur          |
| échelle |   |
|  |   |
| **Intégrer le robot** |   |
| (int) coordonnés/position x et y (possibilités de caster en double pour gagner les avantages de la représenation continue) | coordonnés/position x et y  |
|  |   |
| **Avantages** |   |
| Plus facile pour **ajouter des objets** |  **Fidelité** à la réalité |
|  |   |
| **Inconvénients** |   |
| **Moins précise** que continue car les distances sont arrondies |  Difficile **d'ajouter des objets** |
| Représentation du **mouvement** compliquée |  **Traitement de l'image** difficile à cause d'un passage à la 3D (modelisation de la caméra) |
|  |  **Detection d'objets** par le capteur difficile |

- Un **hybride** de matrice et de forme est possible.


**Robot :**

  **Attributs**
- Les **coordonnées** doivent être implémentées dans le robot. x et y.
- **Forme** du robot (Rectangle, Carré, Rond) ---> représenter la taille.
- **Direction** ---> angle

**Méthodes**
- **Vitesse** ---> il faut trouver une unité de temps et définir une horloge afin de définir la relation vitesse = temps / distance.
- **Déplacement** ---> utiliser le cours 2 sur les vecteurs pour créer les fonctions correspondantes.
- **Réduction du bruit** ---> réduire la marge d'erreur produite par les différents capteurs.

Le Robot et l'Envronnement doivent être **indépendants** et **flexibles**. Ils doivent pouvoir fonctionner seuls et pouvoir être intégrés à n'importe quelle interface graphique pour l'affichage.






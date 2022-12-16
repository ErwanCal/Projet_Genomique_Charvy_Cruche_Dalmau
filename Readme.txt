
Explications des differents dossiers :
  DC3_save : Contient les DC3 de chaque chromosome pour ne pas avoir à les recalculer à chaque fois.
  Result_save : Contient les sorties de notre notebook pour différents intervalles de reads.
  Notebook_Complets : Contient les anciens assemblages des fonction pour obtenir le notebook final.
  Notebook_Secondaires : Contient des notebooks de tests, ou avec des fonctions sans assemblage.
  programmes_pythons : Contient les versions .py des fonctions utilisées dans le notebook final.

Pour lancer le mapping, il suffit d'avoir le notebook "Rendu_final.ipynb", le dossier contenant les DC3,le fichier fastQ des reads et le fichier fna du génome.
Dans le cas où l'on veut recalculer les DC3, le dossier n'est pas nécessaire.

Pour lancer le calcul des DC3 des chromosomes, il est possible que le notebook final plante, dans ce cas il est possible d'utiliser le notebook "Association_codes.ipynb"
qui se trouve dans le dossier Notebooks_Complets.
  

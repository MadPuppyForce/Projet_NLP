# Projet_NLP

## Contexte
Des documents sur les différents titres de presse du groupe Ouest-France datent de la fin du XIXème siècle. L'ensemble de ces documents a été numérisé et accessible en images. Un OCR a été utilisé pour traiter ces images et restituer le texte des articles, mais les performances de cette reconnaissance automatique varient considérablement. Il faudrait réduire considérablement le taux d'erreur OCR pour pouvoir exploiter ces articles d'archives et les mettre en ligne. L'objectif de ce projet est d'identifier des moyens de corriger automatiquement ces erreurs de reconnaissance optique.


## Introduction
Dans ce contexte, nous disposons de 12 articles de presse automatiquement extraits comportant des erreurs d'orthographe, des lettres manquantes, des mots coupés, des ponctuations manquantes et des erreurs de mise en page. Nous possèdons aussi la version corrigée de ces articles.

Dans ce projet, nous allons tout d'abord évaluer la qualité des articles automatiquement extraits (OCR actuel). Puis, nous allons évaluer une méthode de base de correction d'erreur (spell checker). Ensuite, nous allons évaluer des modèles LLM pré-entraînés pour la correction des articles. Et enfin, nous entraînerons des modèles et évaluerons leur qualité pour la correction des articles.

## Évaluer la qualité des articles automatiquement extraits par l'OCR

Je n'ai pas personnelement traiter cette partie, mais plutôt Nadir.  
En évaluant la qualité, il a obtenu 8.48% de CER et 20.47% WER.
On peut expliquer ce score de reconnaissance par le faite que:
* Les OCR peuvent avoir du mal avec des images de texte de qualité médiocre. Une résolution d'image insuffisante peut entraîner des erreurs de reconnaissance.
* Parfois les polices de caractères non standard peuvent poser problème (mauvaise reconnaissance)
* Un OCR peut être optimisés pour certaines langues et avoir des difficultés à reconnaître des caractères spéciaux, ou des alphabets non latins.
* Les documents avec une mise en page complexe peuvent entraîner des erreurs d'interprétation de la mise en page.
* Parfois le document a des taches ou est endommagé.
* Et il peut avoir des difficultés à détecter les zones de texte.

Pour pouvoir améliorer la convertion des images de texte imprimé ou manuscrit en texte éditable (puisque c'est le but d'un OCR), nous pouvons utiliser en parallèle de l'OCR un LLM pour la correction des articles et ainsi générer le texte manquant et corriger les erreurs de l'OCR.
## Évaluer le spell checker
Nadir a aussi évalué le spell checker, il a obtenu 9.79% de CER et 22.47% WER. Un spell checker est un outil conçu pour identifier et corriger les fautes d'orthographe dans un texte. Il analyse les mots d'un document et compare chaque mot à une base de données de mots correctement orthographiés. Si un mot du texte ne correspond pas à un mot correct dans la base de données, le correcteur orthographique suggère des corrections possibles.



## Évaluation des modèles LLM pré-entraînés

Pour cette partie, j'ai évalué  deux LLM pré-entraînés sur la reconnaissance des 12 articles extraits par l'OCR: 
* LanguageTool qui est un outil de grammaire open-source et le correcteur orthographique d'OpenOffice.
* et Gemini.

Pour l'évaluation, je choisis d'utiliser comme métrique le CER (taux d'erreur de caractère) et le WER (taux d'erreur de mot). De plus, pour le prompt de Gemini, je lui précise.
Le code est dans le fichier *evaluation.py* .
Pour le LanguageTool, j'utilise simplement la bibliothèque "language_tool_python".
Pour Gemini, je réalise un prompt où je précise  le contexte des articles, leurs 2 thèmes principaux (les 24h du Mans et l'affaire Seznec) ainsi que la tâche qu'il doit réaliser, c-a-d corriger les textes et je lui ajoute ensuite le texte à tester. Je recueille sa réponse dans le csv des données d'entraînement.

J'obtiens comme résultats:
* LanguageTool: WER =22.4806% et CER = 8.8525%
* Gemini avec contexte: WER =100% et CER = 99.9715%

Le LanguageTool a des résultats satisfaisants et Gemini a des résultats catastrofiques. Les résultats de Gemini peuvent s'expliquer par le faite qu'il a surtout générer un texte en se basant sur le texte qui lui était donné au lieux de tout simplement le corriger. Il est vrai que le prompt était souvent mal interprété par Gemini, c-a-d qu'il corrigeait et générait du texte avec les informations qui lui étaient fournis. Cela montre l'importance des prompts passés à ces modèles. Les résultats de Gemini varient beaucoup en fonction des prompt différents.

## Entraînement de modèles pour la correction des articles

Dans cette sous-paprtie, je vais entraîner un modèle pour la correction d'articles.

### Données d'entraînement et de validation
Pour les données d'entraînement, nous avons utiliser l'ensemble de données Wikitex-fr: https://huggingface.co/datasets/asi/wikitext_fr
L'ensemble de données de modélisation linguistique Wikitext-fr se compose de plus de 70 millions de tokens extraits de l'ensemble des articles français de Wikipedia qui sont classés comme "articles de qualité" ou "bons articles". Maintenant que nous avons ces données, nous allons les altérées (introduire des erreurs) avec un script python. C'est Valentin qui a créé et altéré les données avec le script *bruitage.py* . L'idée est d'introduire un certain pourcentage d'altération au texte. Pour cela, on a une fonction permettant d'intorduire une erreur de type aléatoire à une position aléatoire dans un texte. Nous avons comme type d'erreur: enlever un charactère, ajouter un charactère, erreur sur un charactère, enlever un espace, ajouter un espace, ajouter un retour à la ligne, enlever de la ponctuation et mettre un charactère en majuscule. De plus, nous avons réalisé des dictionnaires N-grammes avec les erreurs fréquentes en OCR et leurs associations.

Nous avons donc split le dataset Wikitext-fr en données d'entraînement et de validation et nous avons altéré les textes à 5% d'alteration.
Les données d'entraînement sont stockées dans le fichier JSONL *notes.jsonl* et les données de validation dans *notes_validations.jsonl* .

### Le Modèle
J'ai rencontré pas mal de problèmes pour trouver un modèle. Les problèmes que j'ai rencontré était souvent liés à des soucis de code et de comptatibilité entre les bibliothèques. J'ai essayé le modèle de Deep Spell et un modèle de la bibliothèque CamembertForTokenClassification.

Au final je suis partie sur un modèle Text2Text Generation. C'est un T5 de Google ("google/flan-t5-base"): https://huggingface.co/google/flan-t5-base

Les modèles T5 (Text-To-Text Transfer Transformer) sont développés par Google et sont des modèles de traitement du langage naturel qui ont été formés pour effectuer une variété de tâches en traitant le texte sous forme de paires entrée-sortie.

### Protocole expérimental
Le code de l'entraînement et des expérimentations de mon modèle se trouve dans le notebook *Projet_NLP.ipynb* . 

Tout d'abord, je charge que 2.5% des données de *notes.jsonl* et *notes_validations.jsonl* car les données d'entraînement sont trop volumineuses pour ma capacité de CPU. 

Ensuite, je pré-traite avec tokenisation mes données pour qu'elles puissent entrer en paramètre de mon modèle. Je choisis un batch-size égale à 4 en fonction de ma capacité de calcul.

Je charge ensuite le modèle et fixe des hyperparamètres (nombre d'époque et le learning rate). Je vais essayer d'améliorer mon modèle en fixant de nouveaux hyperparamètres en fonction des performances de mon modèle, de mon entraînement et des capacités de calcul que je possède. Bien sûr, je calcul ces performances sur mes données de validation. 

Pour évaluer les performances de mon entraînement, je récupère la loss d'entraînement et j'affiche la courbe. 

Pour évaluer les performances de mon modèle, j'affiche les scores WER et CER au fil des époques.

Enfin, je regarde aussi le temps d'éxécution d'un entraînement.

### Expérimentations et résultats

Lors de mes expérimentations, je me suis heurtée à la capacité de calcul que m'offrait Google Colab et au temps de calcul très long.

Je n'ai donc fait que très peu d'expérimentations.

Au départ, je fixais mon nombre d'époque à 10 et mon learning rate à 0.01 avec un batch_size égale à 8, mais mon entraînement n'aboutissait pas puisque je dépassait les ressources disponibles par le GPU de Google Colab.

J'ai donc essayé de réduire au fur à mesure mon batch-size, puis mon learning rate et enfin mon nombre d'époque.

Je suis parvenue à réaliser une expérimentation avec un batch-size = 4, un learning rate = 0.1 et un nombre d'époque = 3. Le temps d'éxécution était de 54 min.


Le nombre d'époque est très insufisant et et le learning rate doit diminuer pour que mon modèle apprenne beaucoup plus. Et on peut voir sur la courbe de ma loss qu'il faudrait continuer d'entraîner mon modèle.

Les résultats sont nuls puisque j'obtiens sur mes données de validation un WER =100%  et un CER = 100%, ce qui montre qu'il y a un problème.

Ma remarque est que les articles sont trop longs pour la fenêtre de tokens du modèles. Du coup, cela coupe au milieu d’une phrase. Sauf que le modèle n'a pas appris à gérer des paragraphes non finis,et donc au lieu de renvoyer l’article corrigé, il le continue et invente.

Je pense que ce modèle "google/flan-t5-base" n'est peut-être pas adapter à notre cas puisque sa fenêtre de tokens est trop petite. Je devrais mieux trouver un autre modèle, mais je n'ai malheuresement pas assez de temps.


Quant aux autres membres de mon groupe:
* Valentin a utilisé un Vigogne-2-7B , un modèle basé sur LLaMa-2 mais surentraîné sur la traduction française du dataset Stanford-Alpaca; il a rencontré les mêmes difficultés que moi.
* Nadir a aussi entraîné un T5, mais son code d'entraînement comporte des erreurs qu'il ne comprends pas.

## Conclusion

Nous avons vu comment évaluer les performances d'un OCR pour la reconnaissance d'un texte sur une image, d'un spell checker et de modèle LLM pré-entraîné pour la correction d'articles. 

Nous avons vu qu'il est intéressant de combiner un OCR avec un modèle de correction d'erreur comme un LLM pour pouvoir récupérer le texte d'un article provenant d'une image de journal. 

Nous avons aussi essayé d'entraîner notre propre correcteur d'articles. Mais le problème que nous avons rencontré était que ces modèles demandaient beaucoup trop de capacités de calcul et de temps pour les entraîner. Peut-être que nous n'avons pas réussi à trouver les LLM plus adapter à notre cas et à nos possibilités. Avec plus de temps, nous aurions peut-être pu obtenir de meilleurs résultats.  

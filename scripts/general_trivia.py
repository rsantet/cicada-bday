"""Pool de questions scientifiques (maths, physique, biologie) pour
l'étape 5 - niveau difficile, pensé pour un public à l'aise en maths
(bac+5) et curieux de culture scientifique générale.
"""

GENERAL_TRIVIA = [
    {
        "q": (
            "Qui a démontré le dernier théorème de Fermat en 1994, "
            "résolvant un problème vieux de plus de 350 ans ?"
        ),
        "choices": [
            "Andrew Wiles",
            "Grigori Perelman",
            "Terence Tao",
            "David Hilbert",
        ],
        "answer": "Andrew Wiles",
    },
    {
        "q": "Combien existe-t-il de solides de Platon ?",
        "choices": ["4", "5", "6", "7"],
        "answer": "5",
    },
    {
        "q": "Quelle est la valeur approchée de la constante d'Euler-Mascheroni ?",
        "choices": ["0,58", "0,71", "0,43", "0,29"],
        "answer": "0,58",
    },
    {
        "q": (
            "Quel mathématicien est considéré comme le fondateur "
            "de la théorie des ensembles ?"
        ),
        "choices": [
            "Georg Cantor",
            "David Hilbert",
            "Giuseppe Peano",
            "Bertrand Russell",
        ],
        "answer": "Georg Cantor",
    },
    {
        "q": (
            "Sur les sept problèmes du prix du millénaire, combien "
            "restent non résolus aujourd'hui ?"
        ),
        "choices": ["4", "5", "6", "7"],
        "answer": "6",
    },
    {
        "q": "Quelle lettre grecque désigne traditionnellement le nombre d'or ?",
        "choices": ["Pi", "Phi", "Tau", "Psi"],
        "answer": "Phi",
    },
    {
        "q": "Qui a démontré en 1882 que pi est un nombre transcendant ?",
        "choices": [
            "Charles Hermite",
            "Ferdinand von Lindemann",
            "Joseph Liouville",
            "Georg Cantor",
        ],
        "answer": "Ferdinand von Lindemann",
    },
    {
        "q": "Laquelle de ces conjectures a été démontrée, par Grigori Perelman ?",
        "choices": [
            "La conjecture de Poincaré",
            "La conjecture de Goldbach",
            "L'hypothèse de Riemann",
            "La conjecture des nombres premiers jumeaux",
        ],
        "answer": "La conjecture de Poincaré",
    },
    {
        "q": "En topologie, une tasse à café est homéomorphe à quel autre objet ?",
        "choices": [
            "Une sphère",
            "Un tore (donut)",
            "Un cube",
            "Un ruban de Möbius",
        ],
        "answer": "Un tore (donut)",
    },
    {
        "q": "Qui a introduit la notation moderne dy/dx pour les dérivées ?",
        "choices": [
            "Isaac Newton",
            "Gottfried Leibniz",
            "Leonhard Euler",
            "Joseph-Louis Lagrange",
        ],
        "answer": "Gottfried Leibniz",
    },
    {
        "q": "Combien de faces possède un icosaèdre régulier ?",
        "choices": ["12", "20", "8", "30"],
        "answer": "20",
    },
    {
        "q": (
            "D'après le théorème des quatre couleurs, combien de couleurs "
            "suffisent pour colorer n'importe quelle carte plane ?"
        ),
        "choices": ["3", "4", "5", "6"],
        "answer": "4",
    },
    {
        "q": "Quel boson est le vecteur de la force électromagnétique ?",
        "choices": [
            "Le gluon",
            "Le photon",
            "Le boson Z",
            "Le boson de Higgs",
        ],
        "answer": "Le photon",
    },
    {
        "q": "Qui a formulé les trois lois fondamentales du mouvement classique ?",
        "choices": [
            "Galileo Galilei",
            "Isaac Newton",
            "Johannes Kepler",
            "René Descartes",
        ],
        "answer": "Isaac Newton",
    },
    {
        "q": "Quelle est la vitesse de la lumière dans le vide, arrondie ?",
        "choices": [
            "150 000 km/s",
            "300 000 km/s",
            "3 000 000 km/s",
            "30 000 km/s",
        ],
        "answer": "300 000 km/s",
    },
    {
        "q": (
            "Pour quelle découverte Albert Einstein a-t-il reçu le prix "
            "Nobel de physique (pas la relativité) ?"
        ),
        "choices": [
            "L'effet photoélectrique",
            "La relativité restreinte",
            "La relativité générale",
            "Le mouvement brownien",
        ],
        "answer": "L'effet photoélectrique",
    },
    {
        "q": (
            "Quelle expérience historique a mis en évidence la nature "
            "ondulatoire de la lumière ?"
        ),
        "choices": [
            "L'expérience de Rutherford",
            "L'expérience des fentes de Young",
            "L'expérience de Millikan",
            "L'expérience de Michelson-Morley",
        ],
        "answer": "L'expérience des fentes de Young",
    },
    {
        "q": (
            "Quel principe stipule qu'on ne peut connaître simultanément, "
            "avec une précision arbitraire, la position et la quantité de "
            "mouvement d'une particule ?"
        ),
        "choices": [
            "Le principe d'exclusion de Pauli",
            "Le principe d'incertitude de Heisenberg",
            "Le principe de complémentarité de Bohr",
            "Le théorème de Noether",
        ],
        "answer": "Le principe d'incertitude de Heisenberg",
    },
    {
        "q": (
            "Quelle particule composite est formée de deux quarks up "
            "et un quark down ?"
        ),
        "choices": ["Le neutron", "Le proton", "Le pion", "L'électron"],
        "answer": "Le proton",
    },
    {
        "q": (
            "Quel boson découvert au CERN en 2012 explique l'origine "
            "de la masse des particules ?"
        ),
        "choices": [
            "Le photon",
            "Le boson de Higgs",
            "Le gluon",
            "Le boson W",
        ],
        "answer": "Le boson de Higgs",
    },
    {
        "q": (
            "Qui a proposé le premier modèle quantifié de l'atome, avec "
            "des électrons sur des orbites discrètes ?"
        ),
        "choices": [
            "Ernest Rutherford",
            "Niels Bohr",
            "J.J. Thomson",
            "Max Planck",
        ],
        "answer": "Niels Bohr",
    },
    {
        "q": (
            "Quel physicien a émis l'hypothèse que toute matière possède "
            "une nature ondulatoire ?"
        ),
        "choices": [
            "Erwin Schrödinger",
            "Louis de Broglie",
            "Werner Heisenberg",
            "Paul Dirac",
        ],
        "answer": "Louis de Broglie",
    },
    {
        "q": (
            "Que ne peut jamais faire l'entropie d'un système isolé, "
            "selon le second principe de la thermodynamique ?"
        ),
        "choices": ["Augmenter", "Diminuer", "Rester constante", "Être nulle"],
        "answer": "Diminuer",
    },
    {
        "q": (
            "Quelle molécule porte l'information génétique chez la "
            "quasi-totalité des organismes vivants ?"
        ),
        "choices": ["L'ARN", "L'ADN", "Une protéine", "Un lipide"],
        "answer": "L'ADN",
    },
    {
        "q": "Qui a formulé la théorie de l'évolution par sélection naturelle ?",
        "choices": [
            "Gregor Mendel",
            "Charles Darwin",
            "Louis Pasteur",
            "Jean-Baptiste Lamarck",
        ],
        "answer": "Charles Darwin",
    },
    {
        "q": "Combien de paires de chromosomes possède un être humain typique ?",
        "choices": ["21", "22", "23", "24"],
        "answer": "23",
    },
    {
        "q": (
            "Quel organite cellulaire est surnommé la centrale "
            "énergétique de la cellule ?"
        ),
        "choices": [
            "Le noyau",
            "La mitochondrie",
            "Le ribosome",
            "L'appareil de Golgi",
        ],
        "answer": "La mitochondrie",
    },
    {
        "q": "Quel scientifique a découvert la pénicilline en 1928 ?",
        "choices": [
            "Louis Pasteur",
            "Alexander Fleming",
            "Robert Koch",
            "Joseph Lister",
        ],
        "answer": "Alexander Fleming",
    },
    {
        "q": "Quelle enzyme réplique l'ADN lors de la division cellulaire ?",
        "choices": [
            "L'ARN polymérase",
            "L'ADN polymérase",
            "La ligase",
            "L'hélicase",
        ],
        "answer": "L'ADN polymérase",
    },
    {
        "q": (
            "Quel processus permet aux plantes de convertir la lumière "
            "en énergie chimique ?"
        ),
        "choices": [
            "La respiration cellulaire",
            "La photosynthèse",
            "La fermentation",
            "La glycolyse",
        ],
        "answer": "La photosynthèse",
    },
    {
        "q": (
            "Quelle scientifique a fourni les clichés de diffraction aux "
            "rayons X essentiels à la découverte de la structure de "
            "l'ADN, sans jamais recevoir le prix Nobel ?"
        ),
        "choices": [
            "Rosalind Franklin",
            "Barbara McClintock",
            "Dorothy Hodgkin",
            "Marie Curie",
        ],
        "answer": "Rosalind Franklin",
    },
    {
        "q": (
            "Quelle scientifique a reçu deux prix Nobel, en physique et "
            "en chimie, pour ses travaux sur la radioactivité ?"
        ),
        "choices": [
            "Marie Curie",
            "Irène Joliot-Curie",
            "Lise Meitner",
            "Rosalind Franklin",
        ],
        "answer": "Marie Curie",
    },
    {
        "q": (
            "Quel chimiste a construit le premier tableau périodique "
            "organisé par masse atomique croissante ?"
        ),
        "choices": [
            "Dmitri Mendeleïev",
            "Antoine Lavoisier",
            "John Dalton",
            "Amedeo Avogadro",
        ],
        "answer": "Dmitri Mendeleïev",
    },
    {
        "q": (
            "Quelle est l'unité de mesure de la quantité de matière "
            "dans le Système International ?"
        ),
        "choices": ["Le gramme", "La mole", "Le becquerel", "L'ampère"],
        "answer": "La mole",
    },
]

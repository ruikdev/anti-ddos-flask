# anti-ddos-flask



Flask Anti-DDoS Implementation
Description

Ce script implémente une protection simple contre les attaques par déni de service distribué (DDoS) en utilisant Flask, un micro-framework web en Python. L'objectif est de limiter le nombre de requêtes envoyées par une adresse IP donnée sur une période de temps définie afin de prévenir les abus.

Le système de protection repose sur la limitation du débit (rate-limiting) et l'utilisation d'un cache pour stocker l'historique des requêtes par adresse IP. Lorsqu'une adresse IP dépasse le nombre maximal de requêtes autorisées, elle est temporairement bloquée pendant un temps défini.
Fonctionnalités

    Protection contre le DDoS : Le script limite le nombre de requêtes par adresse IP dans une fenêtre de temps spécifique (par exemple, 100 requêtes par minute).
    Cache des requêtes : Un cache est utilisé pour stocker l'historique des requêtes et déterminer si une adresse IP doit être bloquée temporairement.
    Blocage des IP : Si une adresse IP dépasse la limite de requêtes, elle est bloquée pendant une période de temps configurable (par exemple, 5 minutes).
    Messages d'erreur : Si une adresse IP est bloquée, une réponse HTTP 429 est renvoyée, indiquant que l'utilisateur a dépassé la limite de requêtes et qu'il doit attendre avant de réessayer.

Structure du Code
1. SimpleCache

SimpleCache est une classe qui implémente un cache thread-safe pour stocker les données temporaires (comme les horodatages des requêtes). Elle utilise un dictionnaire pour garder les informations en mémoire et un verrou (Lock) pour éviter les problèmes d'accès simultané dans un environnement multi-thread.

    Méthodes principales :
        get(key) : Récupère la valeur associée à la clé si elle n'a pas expiré.
        set(key, value, timeout) : Stocke une valeur avec une date d'expiration (timeout).

2. AntiDDoS

La classe AntiDDoS est responsable de la gestion des requêtes et de l'application de la limitation du débit.

    Attributs :
        max_requests : Le nombre maximal de requêtes autorisées par adresse IP.
        time_window : La fenêtre de temps (en secondes) durant laquelle les requêtes sont comptabilisées.
        block_time : Le temps de blocage (en secondes) d'une adresse IP après avoir dépassé la limite de requêtes.

    Méthodes principales :
        check_request() : Méthode exécutée avant chaque requête (before_request), qui vérifie si l'adresse IP a dépassé la limite de requêtes et si elle est bloquée.
        init_app(app) : Méthode qui lie l'anti-DDoS à une application Flask en ajoutant le contrôle des requêtes avant chaque requête entrante.

3. Flask App

L'application Flask expose une route principale (/) qui renvoie un message de bienvenue. Ce script est principalement destiné à tester la logique de limitation de requêtes.

    Route :
        / : Affiche un message de bienvenue indiquant que les requêtes sont surveillées.

4. Exécution du Serveur

Le serveur Flask peut être lancé en exécutant le script avec la commande python <nom_du_script>.py.
Paramétrage

Les paramètres de protection contre les DDoS peuvent être ajustés lors de l'initialisation de la classe AntiDDoS :

anti_ddos = AntiDDoS(app=app, max_requests=100, time_window=60, block_time=300)

    max_requests : Le nombre maximal de requêtes autorisées par adresse IP dans la fenêtre de temps (time_window).
    time_window : La période (en secondes) sur laquelle les requêtes sont comptées. Par défaut, il est fixé à 60 secondes (1 minute).
    block_time : La durée de blocage (en secondes) d'une adresse IP après avoir dépassé la limite. Par défaut, elle est de 300 secondes (5 minutes).

Utilisation

    Installation des dépendances : Installez Flask via pip si ce n'est pas déjà fait :

pip install flask

Exécution du script : Lancez le serveur Flask en exécutant le script Python :

    python <nom_du_script>.py

    Tests : Utilisez un outil comme curl ou un navigateur pour envoyer des requêtes à l'API :
        Si vous envoyez plus de requêtes que la limite définie (max_requests), vous recevrez une erreur HTTP 429 : "Too Many Requests".

Exemple de réponse bloquée

Si vous dépassez la limite de requêtes :

{
  "error": "Too many requests. Please try again later."
}

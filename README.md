# Eco-Stock API — Documentation Globale

Eco-Stock est une API REST développée avec **Django REST Framework** et sécurisée par **JWT**. Elle sert de passerelle intelligente pour gérer des hangars de stockage agricole et automatiser les flux de produits, tout en évitant la surcharge des infrastructures et la manipulation de denrées périmées.

---

##  1. Guide des Adresses de l'API (Endpoints)

1. **Connexion (Obtenir son badge) :**
  Connexion (Obtenir son badge)
  Corps de la requête (JSON) :
  {
    "username": "votre_username",
    "password": "votre_mot_de_passe"
  }

Réponse de l'API : Renvoie un token access. Copiez ce grand texte et collez-le dans l'onglet Authorization (type Bearer Token) sur Postman pour déverrouiller le reste des URLs.

2. **Gestion des Hangars (Warehouses) :**
   Lister les hangars : GET http://127.0.0.1:8000/api/warehouses/
   
   Créer un hangar (Admin) : POST http://127.0.0.1:8000/api/warehouses/
   
   Audit en temps réel : GET http://127.0.0.1:8000/api/warehouses/{id}/audit/
   (Calcule automatiquement le taux d'occupation et liste les produits périmés à l'intérieur).

3. **Gestion des Produits (Products) :**
Lister tous les produits : GET http://127.0.0.1:8000/api/products/

Filtrer le stock d'un hangar : GET http://127.0.0.1:8000/api/products/?warehouse={id_du_hangar}

Créer un produit (Admin) : POST http://127.0.0.1:8000/api/products/

Transférer un produit (Admin) : POST http://127.0.0.1:8000/api/products/{id}/transfer_product/

##  2.Flux Métier : Logique du Transfert de Stock

[ Client (Postman) ]
              │
              │  1. Requête POST (destination_id, quantite)
              ▼
    [ Contrôleur Django ] ──▶ [ Vérification JWT ] ──▶ [ 401 Unauthorized ] (Si pas de token)
              │
              │ 2. Sécurité valide (Vérification du rôle)
              ▼
   [ IsAdminOrReadOnly ] ──▶ [ 403 Forbidden ] (Si utilisateur simple)
              │
              │ 3. Droits Admin OK (Début des règles métiers)
              ▼
   [ Validation Statut ] ──▶ [ 400 Bad Request ] (Si le produit est 'perime')
              │
              │ 4. Produit consommable
              ▼
   [ Validation Stock ] ──▶ [ 400 Bad Request ] (Si quantité demandée > stock source disponible)
              │
              │ 5. Quantité disponible suffisante
              ▼
 [ Validation Capacité ] ──▶ [ 400 Bad Request ] (Si stock actuel + ajout > capacité du hangar cible)
              │
              │ 6. Espace disponible suffisant dans le hangar de destination
              ▼
     [ Enregistrement en Base de Données ] ➔ Retrait à la source + Ajout à la destination
              │
              ▼
    [ Réponse de l'API : 200 OK Transfert Réussi ]
  
   

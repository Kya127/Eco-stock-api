from rest_framework import viewsets, status
from .models import Warehouse, Product
from .serializers import WarehouseSerializer, ProductSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .permissions import IsAdminOrReadOnly

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAdminOrReadOnly]

    # --------- BOUTON PERSONNALISÉ : AUDIT --------------
    # URL : GET /api/warehouses/{id}/audit/
    @action(detail=True, methods=['get'])
    def audit(self, request, pk=None):
        hangar = self.get_object()
        tous_les_produits = hangar.products.all()
        quantite_totale = tous_les_produits.aggregate(Sum('quantite'))['quantite__sum'] or 0
        taux_occupation = (quantite_totale / hangar.capacite) * 100 if hangar.capacite > 0 else 0
        produits_perimes = tous_les_produits.filter(etat='perime')
        serializer_perimes = ProductSerializer(produits_perimes, many=True)
        
        return Response({
            "hangar_nom": hangar.nom,
            "capacite_maximale": hangar.capacite,
            "quantite_actuelle_stockee": quantite_totale,
            "taux_occupation_pourcentage": round(taux_occupation, 2),
            "alerte_produits_perimes": serializer_perimes.data
        }, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    # --- BOUTON PERSONNALISÉ : DÉPLACER ------------
    # URL : POST /api/products/{id}/transfer_product/
    @action(detail=True, methods=['post'])
    def transfer_product(self, request, pk=None):
        produit = self.get_object()
        
        # Récupération des données envoyées par l'utilisateur dans Postman
        destination_id = request.data.get('destination_id')
        quantite_a_deplacer = request.data.get('quantite')
        
        # --- RÈGLE 1 : Validation des données reçues ---
        if not destination_id or not quantite_a_deplacer:
            return Response({"error": "Veuillez fournir 'destination_id' et 'quantite'."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            quantite_a_deplacer = int(quantite_a_deplacer)
            hangar_destination = Warehouse.objects.get(id=destination_id)
        except (ValueError, Warehouse.DoesNotExist):
            return Response({"error": "Quantité invalide ou hangar de destination introuvable."}, status=status.HTTP_400_BAD_REQUEST)
        
        # --- RÈGLE 2 : Interdire le déplacement de produits périmés ---
        if produit.etat == 'perime':
            return Response({"error": "Impossible de déplacer un produit périmé ! Il doit être traité sur place."}, status=status.HTTP_400_BAD_REQUEST)
            
        # --- RÈGLE 3 : Vérifier le stock disponible à la source ---
        if quantite_a_deplacer > produit.quantite:
            return Response({"error": f"Stock insuffisant. Vous essayez de déplacer {quantite_a_deplacer} mais il n'en reste que {produit.quantite}."}, status=status.HTTP_400_BAD_REQUEST)
            
        # --- RÈGLE 4 : Vérifier la capacité du hangar de destination ---
        produits_destination = hangar_destination.products.all()
        stock_actuel_destination = produits_destination.aggregate(Sum('quantite'))['quantite__sum'] or 0
        
        if stock_actuel_destination + quantite_a_deplacer > hangar_destination.capacite:
            return Response({"error": "Le hangar de destination n'a pas la capacité suffisante pour accueillir ces produits."}, status=status.HTTP_400_BAD_REQUEST)
            
        # --- TOUT EST BON : On applique le mouvement de stock ---
        if quantite_a_deplacer == produit.quantite:
            produit.warehouse = hangar_destination
            produit.save()
        else:
            # Si on déplace une PARTIE, on réduit le stock actuel et on crée une nouvelle ligne à destination
            produit.quantite -= quantite_a_deplacer
            produit.save()
            
            Product.objects.create(
                nom=produit.nom,
                quantite=quantite_a_deplacer,
                date_expiration=produit.date_expiration,
                etat=produit.etat,
                warehouse=hangar_destination
            )
            
        return Response({"message": f"Transfert réussi de {quantite_a_deplacer} unités de {produit.nom} vers {hangar_destination.nom}."}, status=status.HTTP_200_OK)



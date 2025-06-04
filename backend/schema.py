# On importe graphene, le module principal de GraphQL pour Python
import graphene

# On importe les requêtes (Query) qu’on définira dans notre application principale (app/schema.py)
from pwa.schema import Query as AppQuery

# On crée une classe principale Query qui hérite des requêtes de AppQuery
class Query(AppQuery, graphene.ObjectType):
    # Pour l'instant, on ne rajoute rien ici, on se contente de regrouper les requêtes
    pass

# On crée le schéma principal qui va regrouper toutes les requêtes GraphQL de l’application
schema = graphene.Schema(query=Query)

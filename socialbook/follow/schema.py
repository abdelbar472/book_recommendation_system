import graphene
from graphene_django import DjangoObjectType
from .models import *

# Add your GraphQL schema here
class Query(graphene.ObjectType):
    pass

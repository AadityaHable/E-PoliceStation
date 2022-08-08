from import_export import resources
from .models import *

class UserResource(resources.ModelResource):
    class Meta:
        model= User
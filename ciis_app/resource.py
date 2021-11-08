from import_export import resources
from .models import DataCIIS

class DataCIISResource(resources.ModelResource):
    class meta:
        model= DataCIIS 
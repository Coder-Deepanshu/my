from django_elasticsearch_dsl import Document, Index
from django_elasticsearch_dsl.registries import registry
from .models import Department

department_index = Index('departments')

department_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@registry.register_document
class DepartmentDocument(Document):

    class Index:
        name = 'departments'

    class Django:
        model = Department
        fields = [
            'name',
            'code',
        ]

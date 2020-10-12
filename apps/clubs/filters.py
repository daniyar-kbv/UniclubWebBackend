from rest_framework.filters import BaseFilterBackend
import coreapi


class ClubsFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='city',
                location='query',
                required=False,
                type='int',
                example=1
            ),
            coreapi.Field(
                name='grade_type',
                location='query',
                required=False,
                type='int',
                example=1
            ),
            coreapi.Field(
                name='club',
                location='query',
                required=False,
                type='int',
                example=1
            ),
            coreapi.Field(
                name='age',
                location='query',
                required=False,
                type='int',
                example=1
            ),
            coreapi.Field(
                name='favorite',
                location='query',
                required=False,
                type='bool',
                example=False
            ),
        ]

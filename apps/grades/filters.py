from rest_framework.filters import BaseFilterBackend
import coreapi


class CoursesFilterBackend(BaseFilterBackend):
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
            coreapi.Field(
                name='latitude',
                location='query',
                required=False,
                type='float',
                example=False
            ),
            coreapi.Field(
                name='longitude',
                location='query',
                required=False,
                type='float',
                example=False
            ),
            coreapi.Field(
                name='distance',
                location='query',
                required=False,
                type='int',
                example=False
            ),
            coreapi.Field(
                name='date',
                location='query',
                required=False,
                type='string',
                example=False
            ),
        ]

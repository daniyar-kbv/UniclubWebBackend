from rest_framework.filters import BaseFilterBackend
import coreapi, coreschema


class CoursesFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='city',
                location='query',
                required=False,
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                name='grade_type',
                location='query',
                required=False,
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                name='club',
                location='query',
                required=False,
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                name='age',
                location='query',
                required=False,
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                name='favorite',
                location='query',
                required=False,
                schema=coreschema.Boolean()
            ),
            coreapi.Field(
                name='latitude',
                location='query',
                required=False,
                schema=coreschema.Number()
            ),
            coreapi.Field(
                name='longitude',
                location='query',
                required=False,
                schema=coreschema.Number()
            ),
            coreapi.Field(
                name='distance',
                location='query',
                required=False,
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                name='date',
                location='query',
                required=False,
                schema=coreschema.String()
            ),
            coreapi.Field(
                name='product_type',
                location='query',
                required=False,
                schema=coreschema.String()
            ),
        ]

from rest_framework.filters import BaseFilterBackend
import coreapi, coreschema


class CoursesMobileFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='age_group',
                location='query',
                required=True,
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                name='attendance_type',
                location='query',
                required=True,
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                name='grade_type',
                location='query',
                required=True,
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                name='time',
                location='query',
                required=False,
            ),
        ]

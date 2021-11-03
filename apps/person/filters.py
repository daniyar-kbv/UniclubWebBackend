from rest_framework.filters import BaseFilterBackend
import coreapi, coreschema


class ScheduleFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='from_date',
                location='query',
                required=False,
                schema=coreschema.String()
            ),
            coreapi.Field(
                name='to_date',
                location='query',
                required=False,
                schema=coreschema.String()
            ),
        ]

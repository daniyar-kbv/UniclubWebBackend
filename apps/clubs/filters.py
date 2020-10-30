from rest_framework.filters import BaseFilterBackend
import coreapi, coreschema


class ClubCalendarFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='month',
                location='query',
                required=False,
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                name='year',
                location='query',
                required=False,
                schema=coreschema.Integer()
            )
        ]


class ClubScheduleFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='date',
                location='query',
                required=False,
                schema=coreschema.String()
            )
        ]


class ClubScheduleWeekFilterBackend(BaseFilterBackend):
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


class ClubsFilterBackend(BaseFilterBackend):
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
        ]

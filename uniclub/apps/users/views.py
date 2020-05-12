from typing import List, Optional

from django.shortcuts import render

from apps.clubs.models import Club

from .permissions import IsPartner


class PartnerAPIMixin:
    permission_classes = (IsPartner,)
    related_fields: List[str] = []
    _club: Optional[Club] = None

    @property
    def club(self):
        if not self._club:
            user = self.request.user
            if hasattr(user, "club"):
                self._club = user.club
        return self._club

    def get_object(self):
        if not self.club:
            return None
        return self._club

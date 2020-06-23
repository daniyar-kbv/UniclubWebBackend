from typing import List, Optional

from django.shortcuts import render

from apps.clubs.models import Club

from .permissions import IsPartner, IsClient


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

    def get_club(self):
        return self.club


class ClientAPIMixin:
    permission_classes = (IsClient,)

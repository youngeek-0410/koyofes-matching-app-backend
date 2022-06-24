from enum import Enum

from django.utils.translation import gettext_lazy as _


class Sex(Enum):
    man = _("man")
    woman = _("woman")
    other = _("other")

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

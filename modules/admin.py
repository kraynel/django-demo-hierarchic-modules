from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Module


@admin.register(Module)
class ModuleAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "nom"
    list_display = (
        "tree_actions",
        "indented_title",
        "nom",
        "formule",
        "poids_total",
    )
    list_display_links = ("indented_title",)
    search_fields = ("nom",)

    def poids_total(self, obj):
        return obj.calculer_poids_total()

    poids_total.short_description = "Poids total"

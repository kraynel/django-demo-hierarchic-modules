from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Module(MPTTModel):
    nom = models.CharField(max_length=200)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    params = models.JSONField(default=dict, blank=True)
    formule = models.CharField(max_length=500, blank=True)

    class MPTTMeta:
        order_insertion_by = ["nom"]

    def get_all_params(self):
        """
        Paramètres hérités de tous les ancêtres + les siens.
        """
        inherited = {}
        for ancestor in self.get_ancestors(include_self=True):
            inherited.update(ancestor.params)
        return inherited

    def calculer_poids_propre(self):
        context = {"params": self.get_all_params()}
        try:
            return eval(self.formule, {}, context) if self.formule else 0
        except Exception as e:
            raise ValueError(f"Erreur dans {self.nom}: {e}")

    def calculer_poids_total(self):
        poids = self.calculer_poids_propre()
        for enfant in self.get_children():
            poids += enfant.calculer_poids_total()
        return poids

    def __str__(self):
        return self.nom

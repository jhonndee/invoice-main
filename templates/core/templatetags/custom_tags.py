from django import template

register = template.Library()

@register.filter
def pluck(list_of_tuples, index):
    """Extrait l’élément `index` de chaque tuple dans la liste"""
    return [t[index] for t in list_of_tuples]

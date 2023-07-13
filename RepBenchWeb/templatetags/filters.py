from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from repair.algorithms_config import CDREP, SCREEN, RPCA, IMR , SPEEDandAcceleration
# from RepBenchWeb.catch22.features import features
register = template.Library()

WebAppTitle = "RepBench"
# algo_names = { RPCA : "RPCA", CDREP : "CDrep", SCREEN : "SCREEN", IMR : "IMR"  , SPEEDandAcceleration : "Speed+Acceleration"
# }

## catch22 filters
paper_link = "https://www.biorxiv.org/content/10.1101/532259v1.full.pdf"
# @register.filter()
# def c22_description(feature_name):
#     return features[feature_name]["description"]

@register.filter()
def cc2_paper_link():
    return paper_link

# @register.filter()
# def c22_abr(feature_name):
#     return features[feature_name]["abr"]


@register.filter()
def parse_alg_name(alg_name):
    from repair  import get_main_alg_name
    return get_main_alg_name(alg_name)



@register.filter(safe=True)
def add_class(value, css_class):
    """
    Adds a CSS class to an HTML element.
    Usage: {{ some_html_element|add_class:"class-name" }}
    """
    value = str(value)
    if "class" in value:
        value = value.replace("class=\"", f"class=\"{css_class} ")
    else: # no class attribute yet
        value =  value.replace(">", f" class=\"{css_class}\">")
    return mark_safe(value)

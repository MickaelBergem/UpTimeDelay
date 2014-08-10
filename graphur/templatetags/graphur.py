from django import forms
from django.template import Context
from django.template.loader import get_template
from django import template

from django.db.models.query import QuerySet
import datetime

register = template.Library()

@register.filter
def graph(object_list, graph_title=""):
    """ Graph the object list """

    if not isinstance(object_list, QuerySet):
        return "[ object_list should be a queryset ]"

    points = []

    for object in object_list:
        points.append({
            'x':object.x_value(),
            'y':object.y_value()
        })

    return render(points, graph_title)

@register.filter
def graph_delay_pastNd(object_list, nb_days):
    """ Graph the delay for the N last days only """

    points = []

    for object in object_list:

        if object.time.date() >= datetime.date.today() - datetime.timedelta(days=nb_days):

            points.append({
                'x':object.x_value(),
                'y':object.y_value()
            })

    return render(points, "Delay")


def render(points, graph_title):

    template = get_template("graphique/base.html")
    context = Context({ 'plot':{
                            'graph_title': graph_title,
                            'points': points
                            }
                     })

    return template.render(context)

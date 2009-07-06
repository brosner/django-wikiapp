# -*- coding: utf-8 -*-
""" Provides util tags to work with markup and other wiki stuff.
"""

from django import template
from django.conf import settings

from template_utils.markup import formatter
# importing here so it is possible to use its filters
# when loading this module.
from template_utils.templatetags.generic_markup import *

try:
    from creoleparser.dialects import Creole10 as Creole
    from creoleparser.core import Parser as CreoleParser
    # create it only once, because it is fairly expensive
    # (e.g., all the regular expressions it uses are compiled)
    dialect = Creole(use_additions=True)
except ImportError:
    Creole = None

def creole(text, **kw):
    """Returns the text rendered by the Creole markup.
    """
    if Creole is None and settings.DEBUG:
        raise template.TemplateSyntaxError("Error in creole filter: "
            "The Creole library isn't installed, try easy_install Creoleparser.")
    parser = CreoleParser(dialect=dialect)
    return parser.render(text)

if Creole is not None:
    formatter.register('creole', creole)

register = template.Library()

@register.inclusion_tag('wiki/article_content.html')
def render_content(article, content_attr='content', markup_attr='markup'):
    """ Display an the body of an article, rendered with the right markup.

    - content_attr is the article attribute that will be rendered.
    - markup_attr is the article atribure with the markup that used
      on the article.

    Use examples on templates:

        {# article have a content and markup attributes #}
        {% render_content article %}

        {# article have a body and markup atributes #}
        {% render_content article 'body' %}

        {# we want to display the  summary instead #}
        {% render_content article 'summary' %}

        {# post have a tease and a markup_style attributes #}
        {% render_content post 'tease' 'markup_style' %}

        {# essay have a content and markup_lang attributes #}
        {% render_content essay 'content' 'markup_lang' %}

    """
    return {
        'content': getattr(article, content_attr),
        'markup': getattr(article, markup_attr)
    }


@register.inclusion_tag('wiki/article_teaser.html')
def show_teaser(article):
    """ Show a teaser box for the summary of the article.
    """
    return {'article': article}


@register.inclusion_tag('wiki/wiki_title.html')
def wiki_title(group):
    """ Display a <h1> title for the wiki, with a link to the group main page.
    """
    return {'group_name': group.name,
            'group_type': group._meta.verbose_name.title(),
            'group_url': group.get_absolute_url()}

from django import template


register = template.Library()


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

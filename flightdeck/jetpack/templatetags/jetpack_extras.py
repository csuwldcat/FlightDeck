from django.template import Template, Library, loader, Context, TemplateSyntaxError, Node
from django.utils.safestring import mark_safe
from django.utils import simplejson
from django.template.defaultfilters import escapejs

register = Library()

@register.filter
def tab_link_id(item, value):
	slug = item.slug if item else ''
	return "%s_%s" % (slug, value)

# this switched of temporarily
@register.filter
def dependency_link_id(item):
	try:
		slug = item.slug
	except: 
		slug = ''
	return "dependency_%s" % slug


@register.filter
def recently_modified_link_id(item):
	slug = item.slug if item else ''
	return "modified_%s" % slug


@register.filter
def render_fullname(item):
	return mark_safe("%s <em>%s</em>" % (item.listname, item.fullname))


@register.filter
def render_base_link(item):
	t = loader.get_template('_gallery_item_link.html')
	return mark_safe(t.render(Context(locals())))


@register.tag
def escape_template(parser, token):
    try:
        tag_name, template_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, \
				"%r tag requires exactly one argument" % token.contents.split()[0]
    if not (template_name[0] == template_name[-1] and template_name[0] in ('"', "'")):
        raise TemplateSyntaxError, \
				"%r tag's argument should be in quotes" % tag_name
    return EscapeTemplate(template_name[1:-1])

class EscapeTemplate(Node):
    def __init__(self, template_name):
		self.t = loader.get_template(template_name)

    def render(self, context):
		return escapejs(self.t.render(context))

from django import template

register = template.Library()


@register.filter(name='get_current_settings')
def get_current_settings(exercise, set_id):
    '''
    Does a filter on the sets

    We need to do this here because it's not possible to pass arguments to function in the template,
    and we are only interested on the settings that belong to the current set
    '''
    return exercise.setting_set.filter(set_id=set_id)


@register.inclusion_tag('tags/render_day.html')
def render_day(day):
    '''
    Renders a day as it will be displayed in the workout overview
    '''
    return {'day':     day,
            'workout': day.training}


@register.inclusion_tag('tags/pagination.html')
def pagination(page, page_range):
    '''
    Renders the necessary links to paginating a long list
    '''
    return {'page':       page,
            'page_range': page_range}


@register.inclusion_tag('tags/render_weight_log.html')
def render_weight_log(log, div_uuid):
    '''
    Renders a weight log series
    '''

    return {'log': log,
            'div_uuid': div_uuid}


@register.inclusion_tag('tags/yaml_form_element.html')
def yaml_form_field(field, css_class='ym-fbox-text'):
    '''
    Renders a form field in a <tr> with all necessary CSS
    '''

    return {'field':     field,
            'css_class': css_class}


@register.inclusion_tag('tags/cc-by-sa-sidebar.html')
def cc_by_sa_sidebar(language):
    '''
    Renders a form field in a <tr> with all necessary CSS
    '''

    return {'language': language}

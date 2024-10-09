from management import models as management_models
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def check(context, url):
    user = context['request'].user

    # if page doesn't have any restriction
    query = management_models.RestrictedPage.objects.filter(url__contains=url)
    if not query:
        return True

    # if user doesn't logined, it can't access
    if not user.is_authenticated:
        return False

    # if user is staff, it can access
    if user.is_staff:
        return True

    # check depending on user
    query = management_models.UserAccessAuthorization.objects.select_related(
        'restricted_page_object').filter(
            user_object=user, restricted_page_object__url__contains=url)
    if query:
        return True

    # check depending on user type
    if not hasattr(user, 'employeeinformation'):
        return False
    if not user.employeeinformation.employee_type_object:
        return False
    type = user.employeeinformation.employee_type_object
    query = management_models.EmployeeTypeAccessAuthorization.objects.select_related(
        'restricted_page_object').filter(
            employee_type_object=type, restricted_page_object__url__contains=url)
    if query:
        return True
    
    # if user has no authorization
    return False
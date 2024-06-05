from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from . import models
from common.functions import get_current_user

@receiver(pre_save, sender=models.User)
def make_user_log(sender, instance, created, raw, **kwargs):
    # if load raw data, skip
    if raw:
        return
    
    base_data = {
        'user_object': instance,
        'editor_object': get_current_user(),
        'timestamp': timezone.now(),
    }
    if created:
        for f in ['email', 'first_name', 'last_name']:
            data = base_data.copy()
            data['field'] = f
            data['after'] = getattr(instance, f)
            models.Log.objects.create(**data)
    else:
        pre_instance = models.User.objects.get(pk=instance.pk)
        for f in ['email', 'phone_number', 'first_name', 'last_name']:
            if getattr(instance, f) != getattr(pre_instance, f):
                data = base_data.copy()
                data['field'] = f
                data['before'] = getattr(pre_instance, f)
                data['after'] = getattr(instance, f)
                models.Log.objects.create(**data)


@receiver(pre_save, sender=models.EmployeeInformation)
def make_emoployeeinfomation(sender, instance, created, raw, **kwargs):
    # if load raw data, skip
    if raw:
        return
    
    base_data = {
        'user_object': instance,
        'editor_object': get_current_user(),
        'timestamp': timezone.now(),
    }
    for f in ['sin_number', 'wage', 'wage_is_based_on', 'employee_type_object']:
        data = base_data.copy()
        data['field'] = f
        data['after'] = getattr(instance, f)
        models.Log.objects.create(**data)
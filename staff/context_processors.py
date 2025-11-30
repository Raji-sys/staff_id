from django.conf import settings

def hospital_settings(request):
    return {
        'HOSPITAL_NAME': settings.HOSPITAL_NAME,
        'SITE_DOMAIN': settings.SITE_DOMAIN,
    }
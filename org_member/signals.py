'''
Created on May 10, 2012

@author: vencax
'''
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

def google_extra_values(**kwargs):
    """
    This can check if there is already user object created based on
    another attributes than email.
    TBD.
    """
    pass


def on_user_become_member(instance, **kwargs):
    
    mail = render_to_string('org_member/new_member_welcome.html', {
         'user' : instance,
         'accountnum' : settings.ORG_MEMBER_ACCOUNT_NUMBER,
         'fee' : settings.ORG_MEMBER_FEES[instance.typee],
         'site' : Site.objects.get_current()
    })
    send_mail(_('Welcome'), mail, 
              settings.ADMINS[0][0],
              [instance.user.email], fail_silently=True)
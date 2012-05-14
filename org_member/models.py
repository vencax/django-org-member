from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField
from social_auth.backends.google import GoogleBackend
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from groupagenda.models import Event

MEMBERSHIP_TYPE_CHOICES = (
    (1, _('person')),
    (2, _('company')),
)

class OrgMember(models.Model):
    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')

    def __unicode__(self):
        return '%s %s' % (ugettext('member'), self.user)

    user = models.OneToOneField(User)
    desc = models.TextField(_('desc'), max_length=1024, null=True, blank=True)
    place = models.CharField(_('place'), max_length=32, null=True, blank=True)
    typee = models.IntegerField(_('mebership type'), 
                                choices=MEMBERSHIP_TYPE_CHOICES, default=1)
    joined = models.DateField(_('member since'), auto_now_add=True)
    tel = models.IntegerField(_('phone number'), null=True, blank=True)
    photo = models.ImageField(upload_to='OrgMemberPictures', null=True, blank=True)
    event_attendance = ManyToManyField(Event, null=True, blank=True)
    
    def first_name(self): return self.user.first_name
    def last_name(self): return self.user.last_name

# -----------------------------------------------------------------------------
    
YEAR_CHOICES = [(y, str(y)) for y in range(2000, 2050)]
    
class FeesPayment(models.Model):
    user = models.ForeignKey(OrgMember)
    year = models.IntegerField(_('year'), choices=YEAR_CHOICES, default=2012)

# ------------- facility for checking if there is already member user -----
# This can happen when we have already database of organization members
# without social-auth associations.
try:
    from social_auth.signals import socialauth_registered, pre_update
    from existing_member_checker import check_if_memberuser_already_exists, \
        google_extra_values
    
    socialauth_registered.connect(check_if_memberuser_already_exists, 
                                  sender=None)
    
    pre_update.connect(google_extra_values, sender=GoogleBackend)
except ImportError:
    pass


if not hasattr(settings, 'ORG_MEMBER_DEFAULT_MEMBER_GROUP'):
    raise ImproperlyConfigured('You must define ORG_MEMBER_DEFAULT_MEMBER_GROUP in your settings')
if not hasattr(settings, 'ORG_MEMBER_ACCOUNT_NUMBER'):
    raise ImproperlyConfigured('You must define ORG_MEMBER_ACCOUNT_NUMBER in your settings')
if not hasattr(settings, 'ORG_MEMBER_FEES'):
    raise ImproperlyConfigured('You must define ORG_MEMBER_FEES in your settings')
elif not isinstance(settings.ORG_MEMBER_FEES, dict):
    raise ImproperlyConfigured('ORG_MEMBER_FEES settings variable must be dictionary')


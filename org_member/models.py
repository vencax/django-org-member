from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.fields.related import ManyToManyField
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
        return _('Member %s') % self.user

    user = models.OneToOneField(User)
    desc = models.CharField(_('desc'), max_length=512)
    place = models.CharField(_('place'), max_length=32)
    typee = models.IntegerField(_('mebership type'), 
                                choices=MEMBERSHIP_TYPE_CHOICES, default=1)
    joined = models.DateField(_('member since'), auto_now_add=True)
    tel = models.IntegerField(_('phone number'))
    event_attendance = ManyToManyField(Event, null=True, blank=True)
    
    def full_name(self):
        return self.user.get_full_name()
    
YEAR_CHOICES = [(y, str(y)) for y in range(2000, 2050)]
    
class FeesPayment(models.Model):
    user = models.ForeignKey(OrgMember)
    year = models.IntegerField(_('year'), choices=YEAR_CHOICES, default=2012)


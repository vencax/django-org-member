'''
Created on Feb 14, 2012

@author: vencax
'''
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.views.generic.base import View
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView

from .models import OrgMember
from .forms import ProfileForm
    
class MemberDetailView(View):
    def get(self, request, *args, **kwargs):
        return get_object_or_404(User, username=kwargs['user'])
    
class MembershipRequestView(View):
    def get(self, request, *args, **kwargs):
        me = request.user
        try:
            members = Group.objects.get(name=settings.DEFAULT_MEMBER_GROUP)
        except Group.DoesNotExist:
            raise ImproperlyConfigured('You must create membership group called %s' % \
                            settings.DEFAULT_MEMBER_GROUP)
        me.groups.add(members)
        me.save()
        
        if not _user_is_member(request):
            memberinfo = OrgMember(user=request.user)
            memberinfo.save()
        
        return HttpResponseRedirect(request.GET.get('next', '/'))

class MemberInfoUpdateView(UpdateView):
    template_name = 'org_member/update_info.html'
    model = OrgMember
    form_class = ProfileForm
    
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/')
    
def on_update_view(request):
    if request.method == 'GET':
        if _user_is_member(request):
            profile = OrgMember.objects.get(user__exact=request.user)
            url = reverse('member_info_update', args=(profile.id, ))
            link = _('update membership info')
        else:
            url = reverse('membership_request')
            link = _('request for membership')
    return render_to_string('org_member/profile_update_extra_content.html', 
                            {'url' : url, 'link' : link})
            
def _user_is_member(request):
    return OrgMember.objects.filter(user__exact=request.user).exists()

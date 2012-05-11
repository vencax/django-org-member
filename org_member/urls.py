
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from .views import MembershipRequestView, MemberDetailView, MemberInfoUpdateView


urlpatterns = patterns('',
    url(r'^membership_request/$', login_required(MembershipRequestView.as_view()), 
        name='membership_request'),
    url(r'^member_detail/(?P<user>\w+)/$', MemberDetailView.as_view(), 
        name='member_detail'),
    url(r'^member_info_update/(?P<pk>[0-9]+)/$', login_required(MemberInfoUpdateView.as_view()), 
        name='member_info_update'),
)
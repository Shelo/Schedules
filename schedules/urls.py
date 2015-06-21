from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'schedules.views.index', name='index'),
    url(r'^home$', 'schedules.views.home', name='home'),
    url(r'^login$', 'schedules.views.log_in', name='login'),
    url(r'^logout$', "schedules.views.log_out", name="logout"),

    url(r'^query-users$', 'schedules.views.query_users'),

    url(r'^project/create$', 'schedules.views.create_project'),
    url(r'^project/s/(?P<project_slug>.+?)/all-members', 'schedules.views.query_project_members'),
    url(r'^project/s/(?P<project_slug>.+?)/remove-member', 'schedules.views.query_remove_member'),
    url(r'^project/s/(?P<project_slug>.+?)/add-member', 'schedules.views.add_member'),
    url(r'^project/s/(?P<project_slug>.+?)/submit$', 'schedules.views.submit_schedule'),
    url(r'^project/s/(?P<project_slug>.+?)/home$', 'schedules.views.project'),
]

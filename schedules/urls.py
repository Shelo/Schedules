from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'schedules.views.index', name='index'),
    url(r'^home$', 'schedules.views.home', name='home'),
    url(r'^login$', 'schedules.views.log_in', name='login'),
    url(r'^logout$', "schedules.views.log_out", name="logout"),

    url(r'project/create/submit$', 'schedules.views.submit_project', name="submit_project"),
    url(r'project/create$', 'schedules.views.create_project', name="create_project"),
    url(r'project/s/(?P<project_slug>.+)/submit$', 'schedules.views.submit_schedule', name="submit"),
    url(r'project/s/(?P<project_slug>.+)$', 'schedules.views.project', name='project'),
]

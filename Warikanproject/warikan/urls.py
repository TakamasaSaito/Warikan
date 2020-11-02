from django.urls import path
from .views import MemberList, DetailList, AddMember, AddDetail, DetailUpdate, DetailDelete ,AddPicture, Division, AddTrip, TripList, TripDelete
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('memberlist/', MemberList.as_view(),name='memberlist'),
    path('detaillist/<int:pk>', DetailList.as_view(),name='detaillist'),
    path('addmember/', AddMember.as_view(),name='addmember'),
    path('adddetail/<int:pk>', AddDetail.as_view(),name='adddetail'),
    path('detailupdate/<int:pk>', DetailUpdate.as_view(),name='detailupdate'),
    path('detaildelete/<int:pk>', DetailDelete.as_view(),name='detaildelete'),
    path('addpicture/', AddPicture.as_view(),name='addpicture'),
    path('division/', Division.as_view(),name='division'),
    path('addtrip/', AddTrip.as_view(),name='addtrip'),
    path('triplist/', TripList.as_view(),name='triplist'),
    path('tripdelete/<int:pk>', TripDelete.as_view(),name='tripdelete'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL1, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.MEDIA_URL2, document_root=settings.MEDIA_ROOT)
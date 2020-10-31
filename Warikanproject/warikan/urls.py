from django.urls import path
from .views import MemberList, DetailList, AddMember, AddDetail, DetailUpdate, DetailDelete ,AddPicture
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
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

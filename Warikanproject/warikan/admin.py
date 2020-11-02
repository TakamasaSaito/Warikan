from django.contrib import admin
from .models import MemberModel, DetailModel ,PictureModel, TripModel

admin.site.register(MemberModel)
admin.site.register(DetailModel)
admin.site.register(PictureModel)
admin.site.register(TripModel)
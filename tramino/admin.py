from django.contrib import admin

# Register your models here.
from .models import TeamInformations, EventPostPool, EventApplyPool, FavoriteEventPool,FavoriteTeamPool,PastGameRecords

admin.site.register(TeamInformations)
admin.site.register(EventPostPool)
admin.site.register(EventApplyPool)
admin.site.register(FavoriteEventPool)
admin.site.register(FavoriteTeamPool)
admin.site.register(PastGameRecords)


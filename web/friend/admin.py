from django.contrib import admin

from friend.models import FriendRequest, FriendList


class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user__username', 'friends__username']
    readonly_fields = ['user']

    class Meta:
        model = FriendList


admin.site.register(FriendList, FriendListAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver', 'is_active']
    list_display = ['sender', 'receiver', 'is_active']
    search_fields = ['sender__username', 'receiver__username']
    readonly_fields = ['sender', 'receiver', 'timestamp']

    class Meta:
        model = FriendRequest


admin.site.register(FriendRequest, FriendRequestAdmin)

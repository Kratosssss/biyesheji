from django.contrib import admin
from bs_app import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html
# Register your models here.
# 外键修改放这里

@admin.register(models.UserInfo)
class UserAdmin(admin.ModelAdmin):

    list_display = ['id', 'user_name', 'email', 'user_img_show']
    list_per_page = 10
    search_fields = ['user_name', ]


@admin.register(models.Pictures)
class PicAdmin(admin.ModelAdmin):
    list_display = ['img_show', 'predict_tag', 'final_tag',  'img_budget', 'img_tag_num']
    list_per_page = 10

@admin.register(models.Matchup)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('matchup_u', 'matchup_p', 'matchup_t')
    list_per_page = 10

    def matchup_u(self, obj):
        return '%s' % obj.matchup_user.user_name
    matchup_u.short_description = '标记者'

    def matchup_p(self, obj):
        return format_html(
                '<img src="{}" width="50px"/>',
                obj.matchup_picture.img_address.url,
            )
    matchup_p.short_description = '图片'

    def matchup_t(self, obj):
        return '%s' % obj.matchup_tag.tag_description
    matchup_t.short_description = '标签'

@admin.register(models.MissionPackage)
class MissionPackageAdmin(admin.ModelAdmin):
    list_display = ('mission_u', 'mission', 'total_price',  'begintime','description', 'isfinished')

    def total_price(self, obj):
        return '%.2f 元' % (obj.total_budget)
    total_price.short_description = '总价'
    def mission_u(self,obj):
        return '%s' % obj.client_id.client_name
    mission_u.short_description = '委托客户'


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_description', )


@admin.register(models.ClientInfo)
class ClientInfoAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'email', 'wallet' )


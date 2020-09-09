from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']
    list_per_page = 20
    list_display = ('question_text', 'pub_date', 'was_published_recently')
admin.AdminSite.site_title = "Polls"
admin.AdminSite.site_header = "Polls Administration"
admin.site.register(Question, QuestionAdmin)
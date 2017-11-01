from django.contrib import admin
from .models import Question,Choice
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [("Date Info",{'fields':["pub_date"],'classes':['collapse']}),
                (None,{'fields':["question_text"]}),]
    inlines = [ChoiceInline]
    search_fields = ['question_text']
    list_display = ('question_text','pub_date','was_published_recently')
admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)
# Register your models here.

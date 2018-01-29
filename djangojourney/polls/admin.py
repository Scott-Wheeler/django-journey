from django.contrib import admin

# Register your models here.
from .models import Question, Choice

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]})
    ]

#     fields = ["pub_date", "question_text"]  ## customize the order of fields

admin.site.register(Question, QuestionAdmin)

admin.site.register(Choice)
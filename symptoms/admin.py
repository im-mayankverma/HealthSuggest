from django.contrib import admin
from .models import Symptom, Condition, ConditionSymptom


admin.site.register(Symptom)
admin.site.register(Condition)
admin.site.register(ConditionSymptom)
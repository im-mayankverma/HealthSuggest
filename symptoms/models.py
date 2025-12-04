from django.db import models


class Symptom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    body_part = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Condition(models. Model):
    SEVERITY_CHOICES = [
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]

    name = models. CharField(max_length=100)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='mild')
    advice = models.TextField()
    home_remedies = models.TextField(blank=True)
    when_to_see_doctor = models.TextField()

    def __str__(self):
        return self.name


class ConditionSymptom(models.Model):
    condition = models.ForeignKey(Condition, on_delete=models. CASCADE)
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    weight = models.IntegerField(default=1)

    class Meta:
        unique_together = ('condition', 'symptom')

    def __str__(self):
        return f"{self.condition. name} - {self.symptom.name}"
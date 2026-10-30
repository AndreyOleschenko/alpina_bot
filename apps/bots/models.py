from django.db import models
from django.contrib.auth.models import User

class Bot(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bots')
    active_scenario = models.ForeignKey('Scenario', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    
    def __str__(self):
        return self.name

class Scenario(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name='scenarios')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.bot.name} - {self.name}"

class Step(models.Model):
    TRIGGER_TYPES = (
        ('exact', 'Exact match'),
        ('contains', 'Contains'),
        ('regex', 'Regex'),
        ('always', 'Always'),
    )
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField(default=0)
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_TYPES, default='always')
    trigger_value = models.CharField(max_length=255, blank=True, help_text="Keyword or pattern")
    prompt = models.TextField(help_text="Instruction for GPT, use {user_message} as placeholder")
    next_step = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='previous_steps')
    is_start = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
        unique_together = ('scenario', 'order')
    
    def __str__(self):
        return f"{self.scenario.name} - Step {self.order}"

class UserSession(models.Model):
    user_id = models.CharField(max_length=255)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    current_step = models.ForeignKey(Step, on_delete=models.SET_NULL, null=True, blank=True)
    context = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user_id', 'bot')
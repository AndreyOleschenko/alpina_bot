from django.contrib import admin
from .models import Bot, Scenario, Step, UserSession

class StepInline(admin.TabularInline):
    model = Step
    extra = 1

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('name', 'bot', 'is_active', 'created_at')
    list_filter = ('is_active', 'bot')
    inlines = [StepInline]

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('scenario', 'order', 'trigger_type', 'trigger_value', 'is_start', 'next_step')
    list_filter = ('trigger_type', 'is_start', 'scenario')

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'bot', 'current_step', 'updated_at')
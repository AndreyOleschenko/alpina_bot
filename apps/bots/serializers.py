from rest_framework import serializers
from .models import Bot, Scenario, Step, UserSession

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'
        read_only_fields = ('id',)

class ScenarioSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, read_only=True)
    
    class Meta:
        model = Scenario
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class BotSerializer(serializers.ModelSerializer):
    scenarios = ScenarioSerializer(many=True, read_only=True)
    
    class Meta:
        model = Bot
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
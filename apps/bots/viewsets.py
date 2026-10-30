from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Bot, Scenario, Step
from .serializers import BotSerializer, ScenarioSerializer, StepSerializer

class BotViewSet(viewsets.ModelViewSet):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class ScenarioViewSet(viewsets.ModelViewSet):
    serializer_class = ScenarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Scenario.objects.filter(bot__owner=self.request.user)
    
    def perform_create(self, serializer):
        bot_id = self.request.data.get('bot')
        bot = Bot.objects.get(id=bot_id, owner=self.request.user)
        serializer.save(bot=bot)
    
    @action(detail=True, methods=['get'])
    def steps(self, request, pk=None):
        scenario = self.get_object()
        steps = scenario.steps.all()
        serializer = StepSerializer(steps, many=True)
        return Response(serializer.data)

class StepViewSet(viewsets.ModelViewSet):
    serializer_class = StepSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        scenario_id = self.request.query_params.get('scenario_id')
        if scenario_id:
            return Step.objects.filter(scenario_id=scenario_id, scenario__bot__owner=self.request.user)
        return Step.objects.filter(scenario__bot__owner=self.request.user)
    
    def perform_create(self, serializer):
        scenario_id = self.request.data.get('scenario')
        scenario = Scenario.objects.get(id=scenario_id, bot__owner=self.request.user)
        serializer.save(scenario=scenario)
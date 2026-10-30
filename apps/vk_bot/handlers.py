import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from django.conf import settings
from apps.bots.models import Bot, Step, UserSession
from .utils import get_gpt_response

def handle_vk_message(vk, event, bot):
    user_id = event.user_id
    message = event.text

    session, _ = UserSession.objects.get_or_create(
        user_id=str(user_id),
        bot=bot,
        defaults={'current_step': None}
    )

    step = session.current_step
    if not step:
        step = Step.objects.filter(scenario=bot.active_scenario, is_start=True).first()
        if not step:
            step = Step.objects.filter(scenario=bot.active_scenario).order_by('order').first()

    if not step:
        vk.messages.send(user_id=user_id, message="Бот не настроен", random_id=0)
        return

    # Проверка триггера
    match = False
    if step.trigger_type == 'always':
        match = True
    elif step.trigger_type == 'exact' and message.lower() == step.trigger_value.lower():
        match = True
    elif step.trigger_type == 'contains' and step.trigger_value.lower() in message.lower():
        match = True

    if not match:
        # Поиск альтернативного шага
        for s in Step.objects.filter(scenario=bot.active_scenario):
            if s.trigger_type == 'always':
                step = s; match = True; break
            elif s.trigger_type == 'exact' and message.lower() == s.trigger_value.lower():
                step = s; match = True; break
            elif s.trigger_type == 'contains' and s.trigger_value.lower() in message.lower():
                step = s; match = True; break
        if not match:
            vk.messages.send(user_id=user_id, message="Не понимаю команду", random_id=0)
            return

    gpt_response = get_gpt_response(step.prompt, message, session.context)
    vk.messages.send(user_id=user_id, message=gpt_response, random_id=0)

    session.current_step = step.next_step
    session.context[step.prompt] = message
    session.save()
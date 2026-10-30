# run_vk_bot
from django.core.management.base import BaseCommand
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from django.conf import settings
from apps.bots.models import Bot
from apps.vk_bot.handlers import handle_vk_message

class Command(BaseCommand):
    help = 'Запуск VK бота'

    def handle(self, *args, **options):
        vk_session = vk_api.VkApi(token=settings.VK_GROUP_TOKEN)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)

        # Берём первого активного бота (или можно передать ID через аргумент)
        bot = Bot.objects.filter(is_active=True).first()
        if not bot:
            self.stdout.write(self.style.ERROR('Нет активных ботов'))
            return

        self.stdout.write(f'Бот "{bot.name}" запущен...')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                handle_vk_message(vk, event, bot)
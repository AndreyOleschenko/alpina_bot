from yandex_cloud_ml_sdk import YCloudML
from django.conf import settings

def get_gpt_response(prompt, user_message, context=None):
    """
    Отправляет запрос к YandexGPT.

    Args:
        prompt: Инструкция для модели. Может содержать плейсхолдер {user_message}.
        user_message: Текущее сообщение пользователя.
        context: Опциональный контекст (пока не используется, можно расширить).

    Returns:
        str: Ответ от модели YandexGPT.
    """
    # Подставляем сообщение пользователя в промпт
    formatted_prompt = prompt.format(user_message=user_message)

    # Создаём клиент Yandex Cloud ML SDK
    sdk = YCloudML(
        folder_id=settings.YC_FOLDER_ID,
        auth=settings.YC_API_KEY
    )

    # Берём модель (можно 'yandexgpt-lite' или 'yandexgpt')
    model = sdk.models.completions("yandexgpt-lite")

    try:
        result = model.configure(
            temperature=0.7,
            max_tokens=500
        ).run(formatted_prompt)
        return result[0].text
    except Exception as e:
        return f"Ошибка YandexGPT: {str(e)}"
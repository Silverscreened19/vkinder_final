from main import *
from db import *
from make_messages import *
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import token_app

'''токен сообщества'''
token = token_app


def current_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Хочу познакомиться', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Следующий', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Добавь в избранное', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Список избранных', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Очистить избранных', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Помощь', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {
              'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), 'keyboard': current_keyboard()})


for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text.capitalize()
            user_id = str(event.user_id)
            user = User()
            name_user = user.user_name(user_id)
            if request == "Привет":
                write_msg(event.user_id, f'Хай, {name_user}! Для запуска поиска введите Хочу познакомиться.\n'
                          f'\nСписок доступных команд: Следующий, Добавь в избранное, Список избранных, Очистить избранных')
            elif request == "Пока":
                write_msg(event.user_id, "Пока((")
            elif request == "Помощь":
                write_msg(event.user_id, f'\nДля запуска поиска введите Хочу познакомиться.'
                          f'\nСписок доступных команд: Следующий, Добавь в избранное, Список избранных, Очистить избранных')
            elif request == "Как дела?":
                write_msg(event.user_id, f"Отлично, {name_user}")
            elif request == "Хочу познакомиться":
                write_msg(event.user_id,
                          f"Минутку, {name_user}, подбираем пользователей:")
                count = 0
                create_db()
                insert_users(user_id)
                insert_matched_users(user_id)
                insert_photos(user_id)
                write_msg(
                    event.user_id, f"Отлично, {name_user}! Вам подошли следующие пользователи: ")
                main(user_id, count)

            elif request == "Список избранных":
                if len(show_favorites()) == 0:
                    write_msg(event.user_id, f"Список пуст!!!")
                else:
                    write_msg(event.user_id, f"Список избранных:")
                    list_of_favorites(user_id)
            elif request == "Следующий":
                count += 1
                main(user_id, count)
            elif request == "Добавь в избранное":
                set = insert_favorites(count)
                if set == 'Неверная команда':
                    write_msg(event.user_id, f"Неверная команда")
                else:
                    insert_favorites(count)
                    write_msg(event.user_id, f"Пользователь добавлен в избранное")
                    if request == "Следующий":
                        write_msg(event.user_id, "Список пуст...")
            elif request == "Очистить избранных":
                drop_favorite_users()
                write_msg(event.user_id, f"Список избранных пуст")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")

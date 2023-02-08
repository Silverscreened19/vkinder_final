from main import *
from db import *
from make_messages import *
from pprint import pprint
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

'''токен сообщества'''
token = 'vk1.a.H1O2MeQhqORWS_wXxjnarAEJEnwbbte2M6-dD9up-0tjdAKzGgnESWbgUb-OXm-SufX2uMlqhY9yjG7iIRtIi_J1sA_xJY0dpfMmIKvo3BF2hyg2eKCfDuoA4k5QvFhFtQDXCv5XKustiWYWpKzeFK00fIKJYGWlBRuXQPPe938V3ZVgLodatSCWnJPORofvo3OYGDxKEOcy6kwa7lKohQ'


def current_keyboard():
    """
    Creates a keyboard to interact with the chatbot.
    :return Keyboard JSON-object
    """
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Хочу познакомиться', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Следующий', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Добавь в избранное', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Список избранных', color=VkKeyboardColor.SECONDARY)
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
                          f'\nСписок доступных команд: Следующий, Добавь в избранное, Покажи избранных, Очистить избранных')
            elif request == "Пока":
                write_msg(event.user_id, "Пока((")
            elif request == "Помощь":
                write_msg(event.user_id, f'\nДля запуска поиска введите Хочу познакомиться.'
                          f'\nСписок доступных команд: Следующий, Добавь в избранное, Покажи избранных, Очистить избранных')
            elif request == "Как дела?":
                write_msg(event.user_id, f"Отлично, {name_user}")

            elif request == "Хочу познакомиться":
                write_msg(event.user_id,
                          f"Минутку, {name_user}, подбираем пользователей:")
                count = 0
                create_db()
                # vk_b.json_info(user_id)
                insert_users(user_id)
                insert_matched_users(user_id)
                insert_photos(user_id)
                # show_users()
                # show_matched_users()
                write_msg(
                    event.user_id, f"Отлично, {name_user}! Вам подошли следующие пользователи: ")
                main(user_id, count)
            elif request == "Добавь в избранное":
                insert_favorites(count)
                write_msg(event.user_id, f"Пользователь добавлен в избранное")
            elif request == "Покажи избранных":
                write_msg(event.user_id, f"Список избранных:")
                list_of_favorites(user_id)
            elif request == "Следующий":
                count += 1
                main(user_id, count)
            elif request == "Добавь в избранное":
                insert_favorites(count)
                write_msg(event.user_id, f"Пользователь добавлен в избранное")
                if request == "Следующий":
                    write_msg(event.user_id, "Не поняла вашего ответа...")
            elif request == "Очистить избранных":
                drop_favorite_users()
                write_msg(event.user_id, f"Список избранных пуст")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")


# создать функции получения имени, пола, возраста, города пользователя, который пишет в чат
# создаем бд с помощью функций create_table_user(), create_table_matched_users(),
# create_table_favorite_users(), create_table_photos()
# информация о пользователе, общающемся с ботом, записывается в бд функцией insert_users()
# когда пользователь вводит данные (пол, возраст, город), должна отработать функция vk.json_info() и
# информация должна выводиться в бот из базы данных
# с помощью команды из бота необходимо добавлять в бд инфу об избранных пользователях и выводить их
# в чат с помощью команды
# Должна быть возможность перейти к следующему человеку с помощью команды или кнопки

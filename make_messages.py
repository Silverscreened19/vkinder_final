from main import *
from pprint import pprint
from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
import requests
from io import BytesIO
from db import show_favorites


TOKEN = 'vk1.a.H1O2MeQhqORWS_wXxjnarAEJEnwbbte2M6-dD9up-0tjdAKzGgnESWbgUb-OXm-SufX2uMlqhY9yjG7iIRtIi_J1sA_xJY0dpfMmIKvo3BF2hyg2eKCfDuoA4k5QvFhFtQDXCv5XKustiWYWpKzeFK00fIKJYGWlBRuXQPPe938V3ZVgLodatSCWnJPORofvo3OYGDxKEOcy6kwa7lKohQ'
# PEER_ID = '8079094' # ID пользователя, которому отправляются подошедшие его профилю фото других пользователей

# def upload_photo(upload, url):
#     img = requests.get(url).content
    # f = BytesIO(img)

#     response = upload.photo_messages(f)[0]

#     owner_id = response['owner_id']
#     photo_id = response['id']
#     access_key = response['access_key']

#     return owner_id, photo_id, access_key


# def send_photo(vk, peer_id, owner_id, photo_id, access_key, message):
#     attachment = f'photo{owner_id}_{photo_id}_{access_key}'
#     vk.messages.send(
#         random_id=get_random_id(),
#         peer_id=peer_id,
#         attachment=attachment,
#         message=message
#     )

# def send_message(vk, peer_id):
#     set = vk_b.json_info(PEER_ID)
#     for item in set:
#         name = item[0]
#         user_link = item[1]
#         # print(name)
#         # print(user_link)
#         message = f'{name}\n{user_link}'
#         # print(message)
#         # vk.messages.send(
#         #     random_id=get_random_id(),
#         #     peer_id=peer_id,
#         #     message=message
#         # )

# def send_all_photo(vk, PEER_ID):
#     vk_session = VkApi(token=TOKEN)
#     vk = vk_session.get_api()
#     upload = VkUpload(vk)
#     set = vk_b.json_info(PEER_ID)
#     for item in set:
#         name = item[0][0]
#         user_link = item[0][1]
#         message = f'{name}\n{user_link}'
#         # for i in range(len(item)):
#         #     URL = item[1][i]
#         vk.send_message(
#             random_id=get_random_id(),
#             peer_id=PEER_ID,
#             message=message
#         )
#     # for item in set:
#     #     for i in range(len(item)):
#     #         URL = item[1][i]
#     #     send_photo(vk, PEER_ID, *upload_photo(upload, URL), message)

# def main(PEER_ID):
#     vk_session = VkApi(token=TOKEN)
#     vk = vk_session.get_api()
#     upload = VkUpload(vk)

#     send_all_photo(vk, PEER_ID)
#     # send_all_photo(vk, PEER_ID)
#     # vk_b.json_info(PEER_ID)



# #     print('ALL!!!')
# # if __name__ == '__main__':
# #     main(PEER_ID)

def upload_photo(upload, url):
    img = requests.get(url).content
    f = BytesIO(img)

    response = upload.photo_messages(f)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key


def send_photo(vk, peer_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment
    )
    return attachment

def send_message(vk, PEER_ID, message):
    set2 = vk_b.make_list_id_2(PEER_ID)
    for item2 in set2:
        name = item2['info']['name']
        user_link = item2['info']['user_link']
        message = f'{name}\n{user_link}'
        vk.messages.send(
            random_id=get_random_id(),
            peer_id=PEER_ID,
            message=message
        )

def send_all_photo(vk, PEER_ID): # изначальная функция
    vk_session = VkApi(token=TOKEN)
    vk = vk_session.get_api()
    upload = VkUpload(vk)
    set = vk_b.json_info(PEER_ID)
    for item2 in set:
        # print(item2)
        name = item2[0]
        user_link = item2[1]
        url_list = item2[2]
        message = f'{name}\n{user_link}'
        vk.messages.send(
            random_id=get_random_id(),
            peer_id=PEER_ID,
            message=message
        )
        for i in url_list:
            send_photo(vk, PEER_ID, *upload_photo(upload, i))

def send_all_photo_2(vk, PEER_ID, count):
    with open ('all_data.json') as f:
        set = json.load(f)
    vk_session = VkApi(token=TOKEN)
    vk = vk_session.get_api()
    upload = VkUpload(vk)
    if count < len(set):
        name = set[count][0]
        user_link = set[count][1]
        url_list = set[count][2]
        message = f'''{name} {user_link}'''
        for i in url_list:
            vk.messages.send(
                random_id=get_random_id(),
                peer_id=PEER_ID,
                message=message
            )
            send_photo(vk, PEER_ID, *upload_photo(upload, i))
    else:
        vk.messages.send(
                random_id=get_random_id(),
                peer_id=PEER_ID,
                message='Пользователей больше нет'
            )

def main(PEER_ID, count):
    vk_session = VkApi(token=TOKEN)
    vk = vk_session.get_api()
    upload = VkUpload(vk)
    send_all_photo_2(vk, PEER_ID, count)


def list_of_favorites(user_id):
    vk_session = VkApi(token=TOKEN)
    vk = vk_session.get_api()
    message = show_favorites()
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=user_id,
        message=message
        )


# pprint(show_favorites())

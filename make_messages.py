from main import *
from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
import requests
from io import BytesIO
from db import show_favorites
from config import token_app

'''токен сообщества'''
TOKEN = token_app


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
    set2 = vk_b.make_list_id(PEER_ID)
    for item2 in set2:
        name = item2['info']['name']
        user_link = item2['info']['user_link']
        message = f'{name}\n{user_link}'
        vk.messages.send(
            random_id=get_random_id(),
            peer_id=PEER_ID,
            message=message
        )


def send_all_photo_2(vk, PEER_ID, count):
    with open('all_data.json', encoding='utf-8') as f:
        set = json.load(f)
    vk_session = VkApi(token=TOKEN)
    vk = vk_session.get_api()
    upload = VkUpload(vk)
    if count < len(set):
        name = set[count][0]
        user_link = set[count][1]
        url_list = set[count][2]
        message = f'''{name} {user_link}'''
        vk.messages.send(
            random_id=get_random_id(),
            peer_id=PEER_ID,
            message=message
        )
        for i in url_list:
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

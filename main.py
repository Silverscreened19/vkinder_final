import requests
import json
from pprint import pprint
import time
import datetime
from dateutil.relativedelta import relativedelta
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType



class User:

    def __init__(self):
        # self.token = 'vk1.a.EX2R_0DLBhX4RKDq_RfJ1R0iJumj9P3UsWJBalAPrAEgOOZyIFDirGA_zS-984BXDeBXqxOSVj-JRndJw-9C0wgwQ4ybVaFNygIZJUxwEqGPeixpSLzTs167RVWJFt-cKuPdYXOrGWzjwNJoGS-jEno41Ron5jgNTfTSD124lcQmm5QONNau2WBenOkfB6WUJwQuS73L9dwnlPk1XfRJPQ'

        # self.token = 'vk1.a.WizWG1P2L55Y71Pw1_Nyee2FPnT6NW-RAPrXfu_8a9sq3G7n1PUepVbE5fhFCo-qjOgivGE8mwbVL2FOoTIDIyNLGvV2aK069lEdAyQvZ7UYxH-TVyYMSVIiyHBJfwgZynXMR_J27nTLDzeWLncwHH9WQELOz-0gG3_JGy9pEzeaDGAShmkRkj9lWwrZ6tjpn38O7nUvwfai6_aYmp4FzQ'
        self.token = 'vk1.a.H1O2MeQhqORWS_wXxjnarAEJEnwbbte2M6-dD9up-0tjdAKzGgnESWbgUb-OXm-SufX2uMlqhY9yjG7iIRtIi_J1sA_xJY0dpfMmIKvo3BF2hyg2eKCfDuoA4k5QvFhFtQDXCv5XKustiWYWpKzeFK00fIKJYGWlBRuXQPPe938V3ZVgLodatSCWnJPORofvo3OYGDxKEOcy6kwa7lKohQ'
        self.vk = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk)


    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {
                'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7)})

    def user_name(self, user_id):
        '''получаем имя пользователя, который общается с ботом'''
        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': self.token,
                  'user_ids': user_id,
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        name_dict = response['response']
        for i in name_dict:
            for key, value in i.items():
                name = i.get('first_name')
                return name


    def user_sex(self, user_id):
        '''получаем пол пользователя, который общается с ботом, возвращаем обратный пол'''
        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': self.token,
                  'user_ids': user_id,
                  'fields': 'sex',
                  'v': '5.131'}
        repl = requests.get(url, params=params)
        response = repl.json()
        for item in response['response']:
            if item['sex'] == 1:
                return 2
            elif item['sex'] == 2:
                return 1


    def user_info(self, user_id):
        '''вспомогательная функция, если не понадобится, удалить в финальном варианте'''
        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': self.token,
                  'user_ids': user_id,
                'fields': 'bdate, sex, city',
                'v': '5.131'}
        reply = requests.get(url, params=params).json()
        return reply


    def user_info_c(self):
        '''вспомогательная функция, если не понадобится, удалить в финальном варианте'''
        url = 'https://api.vk.com/method/users.search'
        params = {'access_token': self.token,
                'city_id': 859,
                'fields': 'bdate, sex, city',
                'v': '5.131'}
        reply = requests.get(url, params=params).json()
        return reply


    def user_city(self, user_id):
        '''получаем город пользователя, который общается с ботом'''
        url = 'https://api.vk.com/method/users.get'
        params = {'fields': 'city',
        'user_ids': user_id,
        'access_token': self.token, 'v': '5.131'}
        reply = requests.get(url, params=params).json()
        for item in reply['response']:
            return item['city']['id']

    def user_city_title(self, user_id):
        '''получаем город пользователя, который общается с ботом'''
        url = 'https://api.vk.com/method/users.get'
        params = {'fields': 'city',
        'user_ids': user_id,
        'access_token': self.token, 'v': '5.131'}
        reply = requests.get(url, params=params).json()
        for item in reply['response']:
            return item['city']['title']

    def user_age(self, user_id):
        '''получаем возраст пользователя, который общается с ботом'''
        url = 'https://api.vk.com/method/users.get'
        params = {'access_token': self.token,
                  'user_ids': user_id,
                  'fields': 'bdate',
                  'v': '5.131'}
        reply = requests.get(url, params=params).json()
        info_list = reply['response']
        for item in info_list:
            if 'bdate' in item.keys():
                byear = datetime.datetime.strptime(item['bdate'], '%d.%m.%Y')
                cur_year= datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
                age = relativedelta(cur_year, byear).years
                return age
                '''код ниже - для случая, если у пользователя, который общается с ботом, скрыта дата рождения,
                но в этом случае бот будет несколько раз запрашивать возраст, тк функция user_age используется
                в make_list_id_2()модуля main и в insert_users(), insert_matched_users() модуля db. По умолчанию
                у пользователя, общающегося с ботом, дата рождения должна быть открыта полностью.'''
            else:
                self.write_msg(user_id, 'Введите возраст (минимум 18 лет): ')
                for event in self.longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        age = event.text
                        return age


class VK_b:

    def __init__(self, version='5.131'):
        # self.token = 'vk1.a.H1O2MeQhqORWS_wXxjnarAEJEnwbbte2M6-dD9up-0tjdAKzGgnESWbgUb-OXm-SufX2uMlqhY9yjG7iIRtIi_J1sA_xJY0dpfMmIKvo3BF2hyg2eKCfDuoA4k5QvFhFtQDXCv5XKustiWYWpKzeFK00fIKJYGWlBRuXQPPe938V3ZVgLodatSCWnJPORofvo3OYGDxKEOcy6kwa7lKohQ'

        self.token = 'vk1.a.WizWG1P2L55Y71Pw1_Nyee2FPnT6NW-RAPrXfu_8a9sq3G7n1PUepVbE5fhFCo-qjOgivGE8mwbVL2FOoTIDIyNLGvV2aK069lEdAyQvZ7UYxH-TVyYMSVIiyHBJfwgZynXMR_J27nTLDzeWLncwHH9WQELOz-0gG3_JGy9pEzeaDGAShmkRkj9lWwrZ6tjpn38O7nUvwfai6_aYmp4FzQ'
        self.version = version
        self.params_2 = {'access_token': self.token, 'v': self.version}



    def make_list_id_2(self, user_id):
        '''собираем айдишники пользователей, подошедших под параметры поиска, собираем их инфу(фамилию, имя, ссылку на вк)'''
        list_id = []
        url = 'https://api.vk.com/method/users.search'
        sex = user.user_sex(user_id)
        city = user.user_city(user_id)
        city_title = user.user_city_title(user_id)
        age = user.user_age(user_id)
        json_data = []
        params = {'sex': sex, 'city': city,'fields': 'sex, city, bdate', 'age_from': age, 'age_to': age, 'count': 100}
        res = requests.get(url, params={**self.params_2, **params}).json()
        # pprint(res)
        # 'status': [1, 6], 'is_closed': False,
        for item in res['response']['items']:
            if 'city' in item and city_title in item['city']['title'] and 'bdate' in item and len(item['bdate'].split('.'))==3 and item['is_closed'] == False:
                f_name = item['first_name']
                l_name = item['last_name']
                u_id = item['id']
                user_data = {'u_id': u_id,
                'info': {'name': f'{f_name} {l_name}',
                'user_link': f'https://vk.com/id{u_id}'}
                }
                list_id.append(item['id'])
                json_data.append(user_data)
            with open ('user_info_2.json', 'w', encoding='utf8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
        return json_data

    def photo_profile(self, user_id):
        '''получаем список фото с максимальным количеством лайков (не более 3) по отобранным айдишникам'''
        name_list = []
        photo_list_2 = []
        photo_list_3 = []
        photo_list_all = []
        photo_list = []
        set = self.make_list_id_2(user_id) # теперь возвращает словарь с ключом u_id
        for item in set:
            id_ = item['u_id']
            url = 'https://api.vk.com/method/photos.get'
            params = {
                'owner_id': id_,
                'album_id': 'profile',
                'extended': '1',
                'photo_sizes': '1'
            }
            res = requests.get(url, params={**self.params_2, **params}).json()
            # pprint(res)
            time.sleep(2)
            all_photo = res['response']['items']
            height = 0
            width = 0
            photo_list_all = []
            for item in all_photo:
                for size in item['sizes']:
                    if height < size['height'] and width < size['width']:
                        height = size['height']
                        width = size['width']
                        url_max = size['url']
                        likes = item['likes']['count']
                photo_dict = [item['likes']['count'], size['url'], id_]
                photo_list_all.append(photo_dict)
                height = 0
                width = 0
                url_max = ''
            photo_list.append(photo_list_all)

        for item2 in photo_list:
            name_list = []
            if len(item2) > 3:
                for i in range(3):
                    max_number = max(item2)
                    name_list.append(max_number)
                    set = item2.index(max_number)
                    del (item2[set])
                photo_list_2.append(name_list)
            elif len(item2) <= 3:
                photo_list_3.append(item2)
        photo_list_3.extend(photo_list_2)
        with open ('photo_profile_3.json', 'w') as f:
            json.dump(photo_list_3, f, ensure_ascii=False, indent=4)
        return photo_list_3

    def json_info(self, user_id):
        json_all = []
        json_set = []
        json_data_2 = {}
        json_all_data2 = []
        set = self.make_list_id_2(user_id) # список ФИО пользователя и ссылки на профиль
        set2 = self.photo_profile(user_id) # список фото пользователей
        for id_ in set:
            for item in set2:
                if id_['u_id'] == item[0][2]:
                    json_data_2 = {}
                    if len(item) == 3:
                        json_data_2 = [
                                        item[0][1],
                                        item[1][1],
                                        item[2][1]
                        ]
                    elif len(item) == 2:
                        json_data_2 = [
                                        item[0][1],
                                        item[1][1]
                                        ]
                    elif len(item) == 1:
                        json_data_2 = [
                                        item[0][1]
                                        ]
                    json_all_data2.append(json_data_2)


        for i in range(len(json_all_data2)):
            name = set[i]["info"]["name"]
            user_link = set[i]["info"]["user_link"]
            # json_all.append([set[i]["info"]["user_link"]])
            # json_set.append(set[i]["info"]["name"])
            json_set.append(name)
            json_set.append(user_link)
            # json_all.append(json_set)
            json_set.append(json_all_data2[i])
            json_all.append(json_set)
            json_set = []

        with open("all_data.json", "w", encoding='utf8') as f:
            json.dump(json_all, f, ensure_ascii=False, indent=2)


        return json_all

# user_id = '8079094'
user = User()
vk_b = VK_b()
# vk_b.json_info(user_id)

# if __name__ == '__main__':


#     user = User()
#     vk_b = VK_b()
    # vk_b = VK_b('2', 'Санкт-Петербург', 23)
    # pprint(vk_b.make_list_id_2(8079094))
    # pprint(vk_b.photo_profile(8079094))
    # vk_b.json_info(1199790)
    # pprint(user.user_info_c())

    # for item in set:
    #     # print(item[0][1])
    #     pprint(item[0][1])
    #     pprint()
    # pprint(user.user_age(1199790))
    # pprint(user.user_city(2373876))
    # vk_b.make_list_id_2(8079094)
    # pprint(user.user_info(859))

#     vk_b = VK_b(user.user_sex(2373876), user.user_city(), user.user_age())  # вводим исходные данные пользователя
#     # vk_t.json_info()
#     # print(vk_t.name(2373876))
#     # print(vk_t.sex_user(2373876))
    # print(user.user_info(2373876))
#     print(user.user_age(2373876))

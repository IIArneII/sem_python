import requests
import re


class DataBase:
    def __init__(self, server: str):
        self.server = server

    @staticmethod
    def normal_dates(data: list, list_to_str=False, card=False):
        # Конвертирует даты в json в привычный вид. Так же может конвертировать списки данных в строки
        for i in range(len(data)):
            for key, value in data[i].items():
                if type(value) != list and re.search('^\d{4}-\d\d-\d\d', str(value)):
                    date = value[0: 10].split('-')
                    data[i][key] = f'{date[2]}.{date[1]}.{date[0]}'
                elif type(value) == list and list_to_str:
                    if value[0]:
                        data[i][key] = '\n'.join(value)
                    else:
                        data[i][key] = ''
                elif type(value) != list and not value:
                    data[i][key] = ''
                elif type(value) == list and card:
                    for l in range(len(value)):
                        for kk, vv in value[l].items():
                            if not vv:
                                data[i][key][l][kk] = ''
                            elif re.search('^\d{4}-\d\d-\d\d', str(vv)):
                                date = vv[0: 10].split('-')
                                data[i][key][l][kk] = f'{date[2]}.{date[1]}.{date[0]}'
        return data

    @staticmethod
    def type_data(data):
        # Возращает тип данных
        if type(data) == list:
            return 'list'
        if type(data) == dict:
            return 'dict'
        if re.search('^\d+.?\d*$', str(data)):
            return 'num'
        if re.search('^\d{4}-\d\d-\d\d', str(data)) or re.search('^\d\d.\d\d.\d{4}$', data):
            return 'date'
        return 'str'

    @staticmethod
    def make_match(match: dict):
        # Конвертирыет json в json, подходящий для принятия сервером. Пригоден для создания запросов с фильтрацией
        m = ''
        for key, val in match.items():
            if type(val) == list:
                if re.search('^\d\d.\d\d.\d{4}$', str(val[0])):
                    d1 = val[0].split('.')
                    d2 = val[1].split('.')
                    m += f'&{key}={d1[2]}-{d1[1]}-{d1[2]}*{d2[2]}-{d2[1]}-{d2[2]}'
                else:
                    m += f'&{key}={val[0]}*{val[1]}'
            elif re.search('^\d\d.\d\d.\d{4}$', str(val)):
                d1 = val[0].split('.')
                m += f'&{key}={d1[2]}-{d1[1]}-{d1[2]}'
            else:
                m += f'&{key}={val}'
        return m

    @staticmethod
    def make_proj(proj: list):
        # Конвертирыет json в json, подходящий для принятия сервером. Пригоден для создания проекции -
        # сервер вернет только те данные, которые были указаны в proj
        p = ''
        for i in proj:
            p += '&proj=' + i
        return p

    def find(self, coll: str, typ: str, match: dict = {}, proj: list = []):
        # Запрашивает у сервера документы из указанной коллекции с указанными фильтрами и указанной проекцией
        # можно указать тип запроса
        req = self.server + '?coll=' + coll + '&type=' + typ
        m = self.make_match(match)
        p = self.make_proj(proj)
        return requests.get(req + m + p).json()

    def delete(self, coll: str, match: dict = {}):
        # Посылает серверу команду на удаление документа из указанной коллекции по указанным фильтрам
        req = self.server + '?coll=' + coll
        m = self.make_match(match)
        return requests.delete(req + m).json()['value']

    def put(self, coll: str):
        # Посялает серверу команду на добавление новыго документа в указанной коллекции
        req = self.server + '?coll=' + coll
        return requests.put(req).json()

    def post(self, coll: str, set: dict):
        # Посылает серверу комнду на обновление документа из указанной коллекции
        return requests.post(self.server + '?coll=' + coll, json=set).json()

    def collection_list(self):
        # Запраашивает у сервера список всех коллекций
        return requests.get(self.server + '?type=collection_list').json()

    def publication_list(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=publication_list' + m).json(), True)

    def publication_doc(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=publication_doc' + m).json(), False)

    def racks_list(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=racks_list' + m).json(), True)

    def racks_doc(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=racks_doc' + m).json(), False)

    def storages_list(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=storages_list' + m).json(), True)

    def storages_doc(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=storages_doc' + m).json(), False)

    def shelfs_list(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=shelfs_list' + m).json(), True)

    def shelfs_doc(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=shelfs_doc' + m).json(), False)

    def fund_items_list(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=fund_items_list' + m).json(), True)

    def fund_items_doc(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=fund_items_doc' + m).json(), False)

    def librarians_list(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=librarians_list' + m).json(), True)

    def librarians_doc(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=librarians_doc' + m).json(), False)

    def authors_list(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=authors_list' + m).json(), True)

    def authors_doc(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=authors_doc' + m).json(), False)

    def reading_rooms_list(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=reading_rooms_list' + m).json(), True)

    def reading_rooms_doc(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=reading_rooms_doc' + m).json(), False)

    def libraries_list(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=libraries_list' + m).json(), True)

    def libraries_doc(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=libraries_doc' + m).json(), False)

    def library_cards_list(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=library_cards_list' + m).json(), True)

    def library_cards_doc(self, match: dict = {}):
        m = self.make_match(match)
        return self.normal_dates(requests.get(self.server + '?type=library_cards_doc' + m).json(), False, True)

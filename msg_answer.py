def go_msg(vk, id, msg='Введите запрос:'):
    vk.messages.send(peer_id=id, random_id=0, message=msg)


def main_msg(vk, id):
    vk.messages.send(peer_id=id, random_id=0, message=f'чтобы выйти пропишите /main')


def NotFound_msg(vk, id):
    vk.messages.send(peer_id=id, random_id=0, message=f'Упсс... Ничего не найдено.')


def error_msg(vk, id):
    vk.messages.send(peer_id=id, random_id=0, message=f'Ошибка, проверьте входные данные')

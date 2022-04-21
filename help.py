from Keyboard import help_keyboard

def help_msg(vk, id):
    vk.messages.send(peer_id=id, random_id=0,
                     message=f'"/info" - Получить информацию о адресе \n'
                             f'"/org" - Информация об организации \n'
                             f'"/map" - Получить информацию по координатам \n'
                             f'"/metro" - Поиск ближайшего метро \n'
                             f'"/wiki" - Поиск по запросу \n'
                             f'/get_vk_info - Поиск информации о юзере вк. \n')
    help_keyboard(vk, id)
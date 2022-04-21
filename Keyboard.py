from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def help_keyboard(vk, id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label='/wiki', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='/info', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='/org', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='/map', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='/metro', color=VkKeyboardColor.PRIMARY)
    vk.messages.send(peer_id=id, random_id=0, message='Клавиатура с возможными командами',
                     keyboard=keyboard.get_keyboard())

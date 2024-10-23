import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atom_chat.settings')
django.setup()

from django.contrib.auth import get_user_model
from chats.models import Channel, Message
from faker import Faker

User = get_user_model()

faker = Faker()

def populate():
    admin_user = User.objects.create(username = "admin", is_moderator = True, is_staff=True, is_superuser=True)
    admin_user.set_password("qwerty_wasd")
    admin_user.save()
    for i in range(5):
        username = faker.user_name()
        user = User.objects.create(username=username,)
        user.set_password("qwerty_wasd")
        user.save()
    channel1 = Channel.objects.create(name="Channel 1", password="qwerty_wasd")
    channel1.participants.set([User.objects.get(id=2)])
    channel2 = Channel.objects.create(name="Channel 2", password="qwerty_wasd",)
    channel2.participants.set([User.objects.get(id=3)])
    channel3 = Channel.objects.create(name="Channel 3", password="qwerty_wasd",)
    channel3.participants.set([User.objects.get(id=4)])
    channels = [channel1, channel2 ,channel3]
    for i in range(3):
        for j in range(3+i):
            text = faker.text()
            message = Message.objects.create(text=text, sender = User.objects.get(id=i+2), channel=channels[i])
    


if __name__ == "__main__":
    print("Заполняем базу данных...")
    populate()
    print("Готово!")

from api.models import Chat, Message, Profile
from django.contrib.auth.models import User

Profile.objects.all().delete()
User.objects.exclude(username='jessefurukawa').delete()
Chat.objects.all().delete()
Message.objects.all.delete()

u1 = User.objects.create(username='HPotter', email='hpot@email.com')
u1.set_password('dangshiz')
u1.save()

u2 = User.objects.create(username='RWeasley', email='RWeasley@email.com', password='dangshiz')
u2.set_password('dangshiz')
u2.save()

u3 = User.objects.create(username='HGranger', email='HGranger@email.com', password='dangshiz')
u3.set_password('dangshiz')
u3.save()

c1 = Chat.objects.create(creator=u1, title="3 wizards chat")

c1.subscribers.add(u1, u2, u3)

m1 = Message.objects.create(author=u1, chat=c1, text="Hihihihi")
m2 = Message.objects.create(author=u1, chat=c1, text="Bonjour")
m3 = Message.objects.create(author=u2, chat=c1, text="こんにちは")
m4 = Message.objects.create(author=u3, chat=c1, text="Hola")

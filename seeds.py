from api.models import Chat, Subscription, Message
from django.contrib.auth.models import User

u1 = User.objects.create(username='HPotter', email='hpot@email.com', password='dangshiz')
u2 = User.objects.create(username='RWeasley', email='RWeasley@email.com', password='dangshiz')
u3 = User.objects.create(username='HGranger', email='HGranger@email.com', password='dangshiz')

c1 = Chat.objects.create(creator=u1)

s1 = Subscription.objects.create(user=u1, chat=c1)
s2 = Subscription.objects.create(user=u2, chat=c1)
s3 = Subscription.objects.create(user=u3, chat=c1)

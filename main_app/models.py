from django.db import models
from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Crazybone(models.Model):
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=150)
    description = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cb = models.ManyToManyField(Crazybone, through='Cb_Profile')

    def __str__(self):
        return f"{self.user}"

    def get_absolute_url(self):
        return reverse("profile", kwargs={"user_id": self.id})


class Cb_Profile(models.Model):
    qty = models.IntegerField(default=1)

    cb = models.ForeignKey(Crazybone, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile}: {self.cb} x{self.qty}"


class Comment(models.Model):
    text = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cb = models.ForeignKey(Crazybone, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}"

    def get_absolute_url(self):
        cb = Crazybone.objects.get(comment=self)
        return reverse('cb_detail', kwargs={'cb_id': cb.id})

    def __str__(self):
        return f"{self.user} -> {self.cb}"

    def get_type(self):
        return 'comment'

    def time_passed(self):
        time = datetime.now(timezone.utc) - self.date
        if time.seconds <= 60:
            return 'Less than a minute ago'
            print('less than a minute')
        elif time.days >= 1:
            s = '' if time.days == 1 else 's'
            print('more than a day')
            return f'{time.days} day{s} ago'
        elif time.seconds >= 3600:
            res = int(time.seconds / 3600)
            s = '' if res == 1 else 's'
            print('more than a hour')
            return f'{res} hour{s} ago'
        else:
            print('else')
            res = int(time.seconds / 60)
            s = '' if res == 1 else 's'
            return f'{res} minute{s} ago'


class FriendList(models.Model):
    user = models.ForeignKey(Profile, related_name='a',
                             on_delete=models.CASCADE)
    myId = models.ForeignKey(Profile, related_name='b',
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.myId}"


TYPE_OF_NOTIFICATION = (
    ('T', 'Trade Request'),
    ('F', 'Friend Request'),
    ('B', 'Battle Request'),
    ('M', 'Battle Move'),
)


class Notification(models.Model):
    notification_type = models.CharField(
        max_length=1,
        choices=TYPE_OF_NOTIFICATION,
        default=TYPE_OF_NOTIFICATION[0][0]
    )
    noti_from = models.ForeignKey(
        Profile, related_name='noti_from', on_delete=models.CASCADE)
    noti_to = models.ForeignKey(
        Profile, related_name='noti_to', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.noti_from} sent you a  {self.get_notification_type_display()}"


TRADE_STATUS = (
    ('A', 'Accepted'),
    ('R', 'Rejected'),
    ('P', 'Pending')
)


class TradeRequest(models.Model):
    user_from = models.ForeignKey(
        Profile, related_name='user_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(
        Profile, related_name='user_to', on_delete=models.CASCADE)
    cb_wanted = models.ForeignKey(
        Crazybone, related_name='cb_wanted', on_delete=models.CASCADE)
    cb_offered = models.ForeignKey(
        Crazybone, related_name='cb_offered', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    created_notification = models.OneToOneField(
        Notification, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=1,
        choices=TRADE_STATUS,
        default='P'
    )

    def get_type(self):
        return 'trade'

    def time_passed(self):
        time = datetime.now(timezone.utc) - self.date
        if time.seconds <= 60:
            return 'Less than a minute ago'
        elif time.seconds >= 86400:
            res = int(time.seconds / 86400)
            s = '' if res == 1 else 's'
            return f'{res} day{s} ago'
        elif time.seconds >= 3600:
            res = int(time.seconds / 3600)
            s = '' if res == 1 else 's'
            return f'{res} hour{s} ago'
        else:
            res = int(time.seconds / 60)
            s = '' if res == 1 else 's'
            return f'{res} minute{s} ago'


class Clan(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Profile)

    def __str__(self):
        return f"{self.name} - {self.members}"


WINNER = (
    ('N', 'None'),
    ('C', 'Challenger'),
    ('D', 'Defender')
)
SHOT = (
    ('L', 'Left'),
    ('H', 'Hit'),
    ('R', 'Right')
)


class Battle(models.Model):
    winner = models.CharField(
        max_length=1,
        choices=WINNER,
        default=WINNER[0][0]
    )

    shot = models.CharField(
        max_length=1,
        choices=SHOT,
        default=SHOT[0][0]
    )

    turn = models.CharField(
        max_length=1,
        choices=WINNER[1:2],
        default=WINNER[1][0]
    )

    challenger = models.ForeignKey(
        Profile, related_name='challenger', on_delete=models.CASCADE)

    defender = models.ForeignKey(
        Profile, related_name='defender', on_delete=models.CASCADE)

    defender_cb = models.ForeignKey(
        Crazybone, related_name='defender_cb', on_delete=models.CASCADE)

    challenger_cb = models.ForeignKey(
        Crazybone, related_name='challenger_cb', on_delete=models.CASCADE)

    accepted = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now, blank=True)
    created_notification = models.OneToOneField(
        Notification, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Battle: {self.id}"

    def get_type(self):
        return 'battle'

    def time_passed(self):
        time = datetime.now(timezone.utc) - self.date
        if time.seconds <= 60:
            return 'Less than a minute ago'
            print('less than a minute')
        elif time.days >= 1:
            s = '' if time.days == 1 else 's'
            print('more than a day')
            return f'{time.days} day{s} ago'
        elif time.seconds >= 3600:
            res = int(time.seconds / 3600)
            s = '' if res == 1 else 's'
            print('more than a hour')
            return f'{res} hour{s} ago'
        else:
            print('else')
            res = int(time.seconds / 60)
            s = '' if res == 1 else 's'
            return f'{res} minute{s} ago'


class Photo(models.Model):
    url = models.CharField(max_length=200)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for user_id: {self.user_id} @{self.url}"

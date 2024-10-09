from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group

class GoogleSocialAdapterStudents(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):

        user = super().save_user(request, sociallogin, form)

        try:
            group = Group.objects.get(name='student')
            user.groups.add(group)
        except Group.DoesNotExist:
            group, created = Group.objects.get_or_create(name="student")
            if created:
                user.groups.add(group)
            else:
                print("C'é stato un errore nella creazione del gruppo")

        # Salva l'utente con il gruppo assegnato
        user.save()

        return user

from bs_app import models


def UserRegist(username, password , email):
    user = models.UserInfo.objects.filter(user_name=username)
    if user:
        return False
    else:
        new_user = models.UserInfo.objects.create()
        new_user.user_name = username
        new_user.password = password
        new_user.email = email
        new_user.save()
        return True


def ClientRegist(clientname, password, email):

    print(clientname)
    print(password)
    print(email)
    client = models.ClientInfo.objects.filter(client_name=clientname)
    if client:
        return False
    else:
        new_client = models.ClientInfo.objects.create()
        new_client.client_name = clientname
        new_client.password = password
        new_client.email = email
        new_client.save()
        return True

from bs_app import models


def UserLogin(request,username, password):
    user = models.UserInfo.objects.get(user_name=username)
    if user.password == password:
        request.session['is_login'] = True
        request.session['user_id'] = user.id
        request.session['user_name'] = user.user_name
        request.session['wallet'] = user.wallet
        return True
    else:
        return False

def ClientLogin(request,clientname,password):
    client = models.ClientInfo.objects.get(client_name=clientname)
    if client.password == password:
        request.session['is_login'] = True
        request.session['client_id'] = client.id
        request.session['client_name'] = client.client_name
        request.session['wallet'] = client.wallet
        return True
    else:
        return False

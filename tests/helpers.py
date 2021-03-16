import json

def signup(client, email, username, password):
    return client.post('/signup', data={
        'email': email,
        'username': username,
        'password': password,
        'confirm_password': password
    }, follow_redirects=True)


def login(client, email, password):
    return client.post('/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def get_headers(token=None):

        header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        if token:
            header['Authorization'] = "Bearer "+token

        return header


def api_signup(client, email, username, password):

    return client.post('/api/v1/auth/signup/',
                        headers=get_headers(),
                        data=json.dumps({
                            "email": email,
                            "username": username,
                            "password": password
                        }))


def api_login(client, email, password):

    return client.post('/api/v1/auth/login/',
                        headers=get_headers(),
                        data=json.dumps({
                            "email": email,
                            "password": password
                        }))
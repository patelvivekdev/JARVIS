from . password import hashing, connect_dbs, password_fetch


def user_authentication(user_name, user_pass):
    """Match user password.
    :param username: username.
    :param password: password.
    :return : True if user is authenticated
    :retun : username.
    """

    username = user_name
    password1 = hashing(user_pass)
    conn = connect_dbs(r'JARVIS\modules\face_identification\face_detection\password.db')
    try:
        password2 = password_fetch(conn, 'user', username)
        if password2:
            if password1 == password2[0][0]:
                return True, username
            else:
                return False, username
        else:
            return False, username
    except Exception as e:
        return {'Error', str(e)}

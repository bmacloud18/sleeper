class User:
    def __init__(self, id, username, _passwordhash, _salt, avatar):
        self.id = id
        self.username = username
        self._passwordhash = _passwordhash
        self._salt = _salt
        self.avatar = avatar
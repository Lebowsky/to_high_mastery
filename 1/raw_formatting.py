class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id}, name={self.name})'


if __name__ == '__main__':
    user = User(1, 'Name')

    print(user)  # User
    print(f'{user!r}')  # User(id=1, name=Name)

    print(user.name)  # Name
    print(f'{user.name!r}')  # 'Name'

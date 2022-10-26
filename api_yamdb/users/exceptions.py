class TokenGenError(Exception):
    """Ошибка генерации токена"""

    def __init__(
        self,
        message='Ошибка во время исполнения User.token'
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'

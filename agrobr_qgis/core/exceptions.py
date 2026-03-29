class agrobrError(Exception):
    pass


class FetchError(agrobrError):
    pass


class ContractError(agrobrError):
    pass


class JoinError(agrobrError):
    pass


class AuthError(agrobrError):
    pass


class DependencyError(agrobrError):
    pass


class ChecksumError(agrobrError):
    pass

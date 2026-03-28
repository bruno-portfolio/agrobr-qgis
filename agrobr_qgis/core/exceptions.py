class AgroBRError(Exception):
    pass


class FetchError(AgroBRError):
    pass


class ContractError(AgroBRError):
    pass


class JoinError(AgroBRError):
    pass


class AuthError(AgroBRError):
    pass


class DependencyError(AgroBRError):
    pass


class ChecksumError(AgroBRError):
    pass

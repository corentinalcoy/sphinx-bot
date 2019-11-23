from enum import Enum


class UserTypeEnum(Enum):
    organization = "organization"
    user = "user"
    enterprise = "enterprise"

    @staticmethod
    def keys():
        return [k.name for k in UserTypeEnum]

    @staticmethod
    def values():
        return [(k.value, k.name) for k in UserTypeEnum]

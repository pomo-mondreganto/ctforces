from rest_framework_extensions.key_constructor.bits import (
    QueryParamsKeyBit,
    UserKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor


class ScoreboardKeyConstructor(DefaultKeyConstructor):
    params_bit = QueryParamsKeyBit()


class ContestTaskListKeyConstructor(DefaultKeyConstructor):
    user_bit = UserKeyBit()

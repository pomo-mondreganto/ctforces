from rest_framework_extensions.key_constructor.bits import (
    QueryParamsKeyBit,
    KwargsKeyBit,
    ArgsKeyBit,
    UserKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor


class ScoreboardKeyConstructor(DefaultKeyConstructor):
    params_bit = QueryParamsKeyBit()
    args_bit = ArgsKeyBit()
    kwargs_bit = KwargsKeyBit()


class ContestTaskListKeyConstructor(DefaultKeyConstructor):
    user_bit = UserKeyBit()
    args_bit = ArgsKeyBit()
    kwargs_bit = KwargsKeyBit()


class ContestTaskSolvedKeyConstructor(DefaultKeyConstructor):
    args_bit = ArgsKeyBit()
    kwargs_bit = KwargsKeyBit()

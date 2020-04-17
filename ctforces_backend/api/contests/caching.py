from rest_framework_extensions.key_constructor.bits import (
    ArgsKeyBit,
    KwargsKeyBit,
    UserKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor


class ScoreboardKeyConstructor(DefaultKeyConstructor):
    args_bit = ArgsKeyBit()
    kwargs_bit = KwargsKeyBit()


class ContestTaskListKeyConstructor(DefaultKeyConstructor):
    user_bit = UserKeyBit()

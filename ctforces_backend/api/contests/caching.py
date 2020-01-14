from rest_framework_extensions.key_constructor.bits import (
    ArgsKeyBit,
    KwargsKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor


class CTFTimeScoreboardKeyConstructor(DefaultKeyConstructor):
    args_bit = ArgsKeyBit()
    kwargs_bit = KwargsKeyBit

from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor


class ScoreboardKeyConstructor(DefaultKeyConstructor):
    params_bit = bits.QueryParamsKeyBit()
    args_bit = bits.ArgsKeyBit()
    kwargs_bit = bits.KwargsKeyBit()


class ContestTaskListKeyConstructor(DefaultKeyConstructor):
    user_bit = bits.UserKeyBit()
    args_bit = bits.ArgsKeyBit()
    kwargs_bit = bits.KwargsKeyBit()


class ContestTaskSolvedKeyConstructor(DefaultKeyConstructor):
    params_bit = bits.QueryParamsKeyBit()
    args_bit = bits.ArgsKeyBit()
    kwargs_bit = bits.KwargsKeyBit()

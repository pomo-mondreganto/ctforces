from rest_framework_extensions.key_constructor import bits
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor


class PostListKeyConstructor(DefaultKeyConstructor):
    params_bit = bits.QueryParamsKeyBit()
    args_bit = bits.ArgsKeyBit()
    kwargs_bit = bits.KwargsKeyBit()

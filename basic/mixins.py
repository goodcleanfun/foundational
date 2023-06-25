import inspect


class MixinHooks:
    __include_subclass__ = True

    @classmethod
    def call_mixin_hooks(cls, bases=None, **kwargs):
        for base in bases or inspect.getmro(cls):
            if "mixin_hook" in base.__dict__:
                base.mixin_hook(cls, **kwargs)

    @classmethod
    def all_base_classes(cls, with_cls=None):
        if with_cls is None:
            with_cls = cls.__include_subclass__

        mro = inspect.getmro(cls)
        return mro if with_cls else mro[1:]

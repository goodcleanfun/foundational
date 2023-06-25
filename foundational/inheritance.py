def update_from_bases(
    cls,
    name,
    bases,
    initial_cls=dict,
    override_with_child=False,
    update_with_child=True,
):
    if name in cls.__dict__ and override_with_child:
        return cls.__dict__[name]

    val = initial_cls()
    for base in bases:
        if base.__dict__.get(name):
            val.update(base.__dict__[name])

    if update_with_child and cls.__dict__.get(name):
        val.update(cls.__dict__[name])

    return val

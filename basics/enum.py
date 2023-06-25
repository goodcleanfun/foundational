import enum


class StringEnum(str, enum.Enum):
    def __str__(self):
        return str(self.value)

    @classmethod
    def display_name(cls, choice):
        return choice.name

    @property
    def display(self):
        return self.value.replace("_", " ").title()

    @classmethod
    def choices(cls):
        return [(choice.value, cls.display_name(choice)) for choice in cls]

    @classmethod
    def from_value(cls, value):
        return cls(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema["enum"] = {m.name: m.value for m in cls}


class LabeledEnum(enum.Enum):
    label: str

    def __new__(cls, value, label):
        obj = object.__new__(cls)
        obj._value = value
        obj.label = label
        return obj

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema["enum"] = {m._value: m.label for m in cls}

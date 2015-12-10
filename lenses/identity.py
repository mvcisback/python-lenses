from .typeclass import ap


class Identity:
    def __init__(self, item):
        self.item = item

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__qualname__, self.item)

    def fmap(self, fn):
        return Identity(fn(self.item))

    @classmethod
    def pure(cls, item):
        return cls(item)

    def ap(self, fn):
        return Identity(fn.item(self.item))

    def traverse(self, fn):
        applicative = fn(self.item)
        return ap(applicative, applicative.pure(Identity))

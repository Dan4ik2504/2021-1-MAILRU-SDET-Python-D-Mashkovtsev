import pytest


def patch_test_method(attrs, scope):
    for k, v in list(attrs.items()):
        if callable(v) and (k.startswith('test') or k.endswith('test')):
            if scope:
                scope_mark = getattr(pytest.mark, scope)
                attrs[k] = scope_mark(attrs[k])


class AddMarks(type):
    def __new__(mcs, name, bases, attrs):
        scope = attrs.get('scope', None) or next((getattr(b, 'scope', None) for b in bases), None)

        patch_test_method(attrs, scope)
        return type.__new__(mcs, name, bases, attrs)

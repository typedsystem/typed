def names(*terms: tuple[object], typesystem=None) -> str:
    from typed.mods.typesystem import nameof
    return ', '.join(nameof(t, typesystem=typesystem) for t in terms)

def prod(*discourses, limit: int = -1):
    from typed.mods.logic import Discourse
    from typed.mods.check import check
    from itertools import islice

    check.every.isinstance(discourses, Discourse)

    zipped_iterator = zip(*discourses, strict=True)

    if limit > 0:
        yield from islice(zipped_iterator, limit)
    else:
        yield from zipped_iterator

def diag(*discourses, limit: int = -1):
    from typed.mods.logic import Discourse
    from typed.mods.check import check
    from itertools import islice

    check.every.isinstance(discourses, Discourse)

    yielded_count = 0

    for i, discourse in enumerate(discourses):
        if 0 < limit <= yielded_count:
            break

        iterator = iter(discourse)

        diagonal_element = list(islice(iterator, i, i + 1))

        if not diagonal_element:
            raise ValueError(f"Discourse at index {i} is too short to form a complete diagonal.")

        yield diagonal_element[0]
        yielded_count += 1

def coprod(*discourses, limit: int = -1):
    from typed.mods.logic import Discourse
    from typed.mods.check import check
    from itertools import islice

    check.every.isinstance(discourses, Discourse)

    def _coprod_generator():
        for i, discourse in enumerate(discourses):
            for x in discourse:
                yield (i, x)

    if limit > 0:
        yield from islice(_coprod_generator(), limit)
    else:
        yield from _coprod_generator()

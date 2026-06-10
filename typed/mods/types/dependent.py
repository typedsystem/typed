from typed.mods.meta.dependent import (
    RELATED, SUBS, SUPS, SAME, EQUIV,
    FILTERED, BOUNDED, HAS
)

from typed.mods.flags import Flags

class Related(metaclass=RELATED):
    """
    The dependent 'bounded' type.

    : kindof(Related)     is  type
    : typeof(Related)     is  BOUNDED
    : isterm(x, Related)  iff issub(typeof(x), Related)
    : nullof(Related)     is  NotDefined
    : builtin(Related)    is  NotDefined
    : flags(Related)      is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)

class Subs(metaclass=SUBS):
    """
    The dependent 'issub of them' type.

    : kindof(Subs)     is  type
    : typeof(Subs)     is  SUBS
    : isterm(x, Subs)  iff issub(typeof(x), Subs)
    : nullof(Subs)     is  NotDefined
    : builtin(Subs)    is  NotDefined
    : flags(Subs)      is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)

class Sups(metaclass=SUPS):
    """
    The dependent 'issub of them' type.

    : kindof(Sups)     is  type
    : typeof(Sups)     is  SUPS
    : isterm(x, Sups)  iff issub(typeof(x), Sups)
    : nullof(Sups)     is  NotDefined
    : builtin(Sups)    is  NotDefined
    : flags(Sups)      is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)

class Same(metaclass=SAME):
    """
    The dependent 'isequiv to them' type.

    : kindof(Same)     is  type
    : typeof(Same)     is  SAME
    : isterm(x, Same)  iff issub(typeof(x), Same)
    : nullof(Same)     is  NotDefined
    : builtin(Same)    is  NotDefined
    : flags(Same)      is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)

class Equiv(metaclass=EQUIV):
    """
    The dependent 'isequiv to them' type.

    : kindof(Equiv)     is  type
    : typeof(Equiv)     is  EQUIV
    : isterm(x, Equiv)  iff issub(typeof(x), Equiv)
    : nullof(Equiv)     is  NotDefined
    : builtin(Equiv)    is  NotDefined
    : flags(Equiv)      is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)

class Filtered(metaclass=FILTERED):
    """
    The dependent 'bounded' type.

    : kindof(Filtered)     is  type
    : typeof(Filtered)     is  FILTERED
    : isterm(x, Filtered)  iff issub(typeof(x), Filtered)
    : nullof(Filtered)     is  NotDefined
    : builtin(Filtered)    is  NotDefined
    : flags(Filtered)      is  is_dependent, is_filtered
    """
    __flags__ = Flags(is_dependent=True, is_filtered=True)

class Bounded(metaclass=BOUNDED):
    """
    The dependent 'bounded' type.

    : kindof(Bounded)     is  type
    : typeof(Bounded)     is  BOUNDED
    : isterm(x, Bounded)  iff issub(typeof(x), Bounded)
    : nullof(Bounded)     is  NotDefined
    : builtin(Bounded)    is  NotDefined
    : flags(Bounded)      is  is_dependent, is_enumerable, is_finite, is_bounded
    """
    __flags__ = Flags(is_dependent=True, is_enumerable=True, is_finite=True, is_bounded=True)

class Has(metaclass=HAS):
    """
    The dependent 'has' type.

    : kindof(Has)    is  type
    : typeof(Has)    is  HAS
    : isterm(x, Has) iff issub(typeof(x), Has)
    : nullof(Has)    is  NotDefined
    : builtin(Has)   is  NotDefined
    : flags(Has)     is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)

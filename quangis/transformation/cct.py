"""
Module containing the core concept transformation algebra.
"""

from quangis.transformation.type import TypeOperator, TypeVar
from quangis.transformation.algebra import TransformationAlgebra

# Some type variables for convenience
x, y, z, q, q1, q2, rel = (TypeVar() for _ in range(0, 7))


class CCT(TransformationAlgebra):
    """
    Core concept transformation algebra. Usage:

        >>> from quangis import CCT
        >>> cct = CCT()
        >>> expr = cct.parse("pi1 (objects data)")
        >>> print(expr.type)
        R(Obj)

    """

    ###########################################################################
    # Types and type synonyms

    Val = TypeOperator("Val")
    Obj = TypeOperator("Obj", supertype=Val)  # O
    Reg = TypeOperator("Reg", supertype=Val)  # S
    Loc = TypeOperator("Loc", supertype=Val)  # L
    Qlt = TypeOperator("Qlt", supertype=Val)  # Q
    Nom = TypeOperator("Nom", supertype=Qlt)
    Bool = TypeOperator("Bool", supertype=Nom)
    Ord = TypeOperator("Ord", supertype=Nom)
    Itv = TypeOperator("Itv", supertype=Ord)
    Ratio = TypeOperator("Ratio", supertype=Itv)
    Count = TypeOperator("Count", supertype=Ratio)
    R = TypeOperator.R

    SpatialField = R(Loc, Qlt)
    InvertedField = R(Qlt, Reg)
    FieldSample = R(Reg, Qlt)
    ObjectExtent = R(Obj, Reg)
    ObjectQuality = R(Obj, Qlt)
    NominalField = R(Loc, Nom)
    BooleanField = R(Loc, Bool)
    NominalInvertedField = R(Nom, Reg)
    BooleanInvertedField = R(Bool, Reg)

    ###########################################################################
    # Data inputs

    pointmeasures = R(Reg, Itv), 1
    amountpatches = R(Reg, Nom), 1
    contour = R(Ord, Reg), 1
    objects = R(Obj, Ratio), 1
    objectregions = R(Obj, Reg), 1
    contourline = R(Itv, Reg), 1
    objectcounts = R(Obj, Count), 1
    field = R(Loc, Ratio), 1
    object = Obj, 1
    region = Reg, 1
    in_ = Nom, 0
    countV = Count, 1
    ratioV = Ratio, 1
    interval = Itv, 1
    ordinal = Ord, 1
    nominal = Nom, 1

    ###########################################################################
    # Math/stats transformations

    # functional
    compose = (y ** z) ** (x ** y) ** (x ** z)

    # derivations
    ratio = Ratio ** Ratio ** Ratio
    leq = Ord ** Ord ** Bool
    eq = Val ** Val ** Bool

    # aggregations of collections
    count = R(Obj) ** Ratio
    size = R(Loc) ** Ratio
    merge = R(Reg) ** Reg
    centroid = R(Loc) ** Loc

    # statistical operations
    avg = R(Val, Itv) ** Itv
    min = R(Val, Ord) ** Ord
    max = R(Val, Ord) ** Ord
    sum = R(Val, Count) ** Count

    ###########################################################################
    # Geographic transformations

    # conversions
    reify = R(Loc) ** Reg
    deify = Reg ** R(Loc)
    get = R(x) ** x, x.limit(Val)
    invert = \
        R(Loc, Ord) ** R(Ord, Reg), \
        R(Loc, Nom) ** R(Reg, Nom)
    revert = \
        R(Ord, Reg) ** R(Loc, Ord), \
        R(Reg, Nom) ** R(Loc, Nom)

    # quantified relations
    oDist = R(Obj, Reg) ** R(Obj, Reg) ** R(Obj, Ratio, Obj)
    lDist = R(Loc) ** R(Loc) ** R(Loc, Ratio, Loc)
    loDist = R(Loc) ** R(Obj, Reg) ** R(Loc, Ratio, Obj)
    oTopo = R(Obj, Reg) ** R(Obj, Reg) ** R(Obj, Nom, Obj)
    loTopo = R(Loc) ** R(Obj, Reg) ** R(Loc, Nom, Obj)
    nDist = R(Obj) ** R(Obj) ** R(Obj, Ratio, Obj) ** R(Obj, Ratio, Obj)
    lVis = R(Loc) ** R(Loc) ** R(Loc, Itv) ** R(Loc, Bool, Loc)
    interpol = R(Reg, Itv) ** R(Loc) ** R(Loc, Itv)

    # amount operations
    fcont = R(Loc, Itv) ** Ratio
    ocont = R(Obj, Ratio) ** Ratio

    ###########################################################################
    # Relational transformations

    # Projection (π). Projects a given relation to one of its attributes,
    # resulting in a collection.
    pi1 = rel ** R(x), rel.has_param(R, x, at=1)
    pi2 = rel ** R(x), rel.has_param(R, x, at=2)
    pi3 = rel ** R(x), rel.has_param(R, x, at=3)

    # Selection (σ). Selects a subset of the relation using a constraint on
    # attribute values, like equality (eq) or order (leq).
    select = (x ** x ** Bool) ** rel ** x ** rel, \
        x.limit(Val), rel.has_param(R, x)

    # Join (⨝). Subset a relation to those tuples having an attribute value
    # contained in a collection.
    join_subset = rel ** R(x) ** rel, \
        x.limit(Val), rel.has_param(R, x)

    # Join (⨝*). Substitute the quality of a quantified relation to some
    # quality of one of its keys.
    join_key = R(x, Qlt, y) ** rel ** R(x, q, y), \
        x.limit(Val), y.limit(Val), q.limit(Qlt), \
        rel.limit(R(x, q), R(y, q))

    # Join with (⨝_f). Generate a unary concept from two other unary concepts
    # of the same type:
    join_with = (q1 ** q1 ** q2) ** R(x, q1) ** R(x, q1) ** R(x, q2), \
        q1.limit(Qlt), q2.limit(Qlt), x.limit(Val)

    # Group by (β). Group quantified relations by the left (right) key,
    # summarizing lists of quality values with the same key value into a new
    # value per key, resulting in a unary core concept relation.
    groupbyL = (rel ** q) ** R(x, q, y) ** R(x, q), \
        x.limit(Val), y.limit(Val), \
        q.limit(Qlt), \
        rel.limit(R(x), R(x, q1))

    groupbyR = (rel ** q) ** R(x, q, y) ** R(y, q), \
        x.limit(Val), y.limit(Val), \
        q.limit(Qlt), \
        rel.limit(R(y), R(y, q))

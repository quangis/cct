#!/usr/bin/env python3
import unittest
import rdflib  # type: ignore
from transformation_algebra import error

from cct import algebra, R1, R2, Obj, Ratio


class TestCCT(unittest.TestCase):
    def parse(self, string, result=None):
        if result is None:
            # if the result is unknown, just check if it contains any
            # unresolved variables
            self.assertTrue(
                not any(algebra.parse(string).type.plain().variables()))
        elif isinstance(result, type) and issubclass(result, Exception):
            self.assertRaises(result, algebra.parse, string)
        else:
            self.assertEqual(algebra.parse(string).type.plain(),
                    result.plain())

    def test_projection(self):
        self.parse(
            "pi1 (objectregions xs)",
            R1(Obj))

    def test_select_match(self):
        self.parse(
            "select leq (objectratios xs) (interval x)",
            R2(Obj, Ratio))

    def test_select_mismatch(self):
        self.parse(
            "select leq (objectratios xs) (nominal x)",
            error.SubtypeMismatch)

    def test01(self):
        self.parse(
            "compose deify reify (pi1 (field something))")

    def test02(self):
        self.parse(
            "select eq (objectregions x) (object y)")

    def test03(self):
        self.parse(
            "select eq (amountpatches x) (nominal y)")

    def test04(self):
        self.parse(
            "select leq (contour x) (ordinal y)")

    def test05(self):
        self.parse(
            "join_subset (objectregions x) (pi1 (select eq (otopo "
            "(objectregions x) (objectregions y)) in))")

    def test06(self):
        self.parse(
            "groupbyL sum (join_key (select eq (otopo (objectregions x) "
            "(objectregions y)) in) (objectcounts z))")

    def test07(self):
        self.parse(
            "groupbyL sum (join_key (select eq (otopo (objectregions x) "
            "(objectregions y)) in) (objectratios z))")

    def test08(self):
        self.parse(
            "groupbyL avg (join_key (select eq (otopo (objectregions x) "
            "(objectregions y)) in) (objectratios z))")

    def test09(self):
        self.parse(
            "groupbyL avg (join_key (select eq (otopo (objectregions x) "
            "(objectregions y)) in) (objectcounts z))")

    def test10(self):
        self.parse(
            "groupbyR count (select eq (otopo (objectregions x) "
            "(objectregions y)) in)")

    def test11(self):
        self.parse(
            "revert (contour x)")

    def test12(self):
        self.parse(
            "revert (nomcoverages x)")

    def test13(self):
        self.parse(
            "invert (field x)")

    def test14(self):
        self.parse(
            "select leq (field x) (ordinal y)")

    def test15(self):
        self.parse(
            "groupbyR size (select eq (lotopo (pi1 (field x))"
            "(objectregions y)) in)")

    def test16(self):
        self.parse(
            "groupbyR size (select eq (lotopo (deify (merge (pi2 "
            "(objectregions x)))) (objectregions x)) in)")

    def test17(self):
        self.parse(
            "apply2 ratio (objectratios x) (objectratios y)")

    def test18(self):
        self.parse(
            "interpol (pointmeasures x) "
            "(deify (merge (pi2 (objectregions y))))")

    def test19(self):
        self.parse(
            "groupbyL avg (join_key (select eq (lotopo (pi1 (field x)) "
            "(objectregions y)) in) (field b))")

    def test20(self):
        self.parse(
            "join_subset (field x) (deify (merge (pi2 (objectregions x))))")

    def test21(self):
        self.parse(
            "reify (pi1 (field x))")

    def test22(self):
        self.parse(
            "groupbyR count (select eq (otopo (objectregions _:source3) "
            "(join_subset (objectregions _:source2) (pi1 (select eq (otopo "
            "(objectregions _:source2) (select eq (objectregions _:source1)"
            "(object Amsterdam))) in)))) in)")

    def test23(self):
        self.parse(
            "join_subset (objectregions roads) (pi3 (select eq (lotopo (deify "
            "(region 1234)) (objectregions roads)) in))")

    def test24(self):
        self.parse(
            "reify (pi1 (select leq (join_subset (revert (contour noise)) "
            "(deify (merge (pi2 (select eq (objectregions muni) "
            "(object Utrecht)))))) (ordinal 70)))")

    def test25(self):
        self.parse(
            "apply2 ratio (groupbyR size (select eq (lotopo (pi1 (select "
            "leq (revert (contour noise)) (ordinal 70))) (select eq "
            "(objectregions muni) (object Utrecht))) in)) (groupbyR size "
            "(select eq (lotopo (deify (merge (pi2 (objectregions muni)))) "
            "(select eq (objectregions muni) (object Utrecht))) in))")

    def test26(self):
        self.parse(
            "groupbyR sum (join_key (select eq (otopo (objectregions "
            "households) (join_subset (objectregions neighborhoods) (pi1 "
            "(select eq (otopo (objectregions neighborhoods) (select eq "
            "(objectregions muni) (object Utrecht))) in)))) in) "
            "(objectcounts households))")

    def test27(self):
        self.parse(
            "groupbyR avg (join_key (select eq (lotopo (deify (merge (pi2 "
            "(select eq (objectregions muni) (object Utrecht))))) "
            "(join_subset (objectregions neighborhoods) (pi1 (select eq "
            "(otopo (objectregions neighborhoods) (select eq (objectregions "
            "muni) (object Utrecht))) in)))) in) (interpol (pointmeasures "
            "temperature) (deify (merge (pi2 (select eq (objectregions muni) "
            "(object Utrecht)))))))")

    @unittest.skip("This one seems incorrect.")
    def test28(self):
        self.parse("""
        ratio
            (fcont avg
                (interpol
                    (pointmeasures temperature)
                    (deify (merge (pi2 (
                        select eq (objectregions muni) (object Utrecht)
                    ))))
                )
                (region x)
            )
            (size (pi1
                (interpol
                    (pointmeasures temperature)
                    (deify (merge (pi2 (
                        select eq (objectregions muni) (object Utrecht)
                    ))))
                )
            ))""")


# Also test algebra expressions from RDF file
TOOLS = rdflib.Namespace("http://geographicknowledge.de/vocab/GISTools.rdf#")
path = "ToolDescription_TransformationAlgebra.ttl"
g = rdflib.Graph()
g.parse(path, format=rdflib.util.guess_format(path))
for s, o in g.subject_objects(TOOLS.algebraexpression):
    setattr(TestCCT, f"test_{s}", lambda x: x.parse(o))


if __name__ == '__main__':
    unittest.main()

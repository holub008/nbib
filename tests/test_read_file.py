from nbib import read, read_file

from tests.test_read import single_ref


def test_read_single():
    file_results = read_file('tests/resources/single.nbib')
    str_results = read(single_ref)

    assert file_results == str_results


def test_read_many():
    # this test is more about facing a variety of refs & not throwing an exception or taking too long
    results = read_file('tests/resources/pubmed-balloongui-set.nbib')
    assert len(results) == 75  # the number of results reported to be in the file by PubMed

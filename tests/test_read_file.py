import datetime

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


def test_read_medlars():
    results = read_file('tests/resources/pmc_medlars.txt')
    assert len(results) == 5
    res0 = results[0]
    assert res0['pmcid'] == 6055010
    assert res0['pubmed_id'] == 30042925
    assert res0['electronic_issn'] == '2215-0161'
    assert res0['journal_volume'] == '5'
    assert res0['publication_date'] == '2018'
    assert res0['title'] == 'A method package for electrophysiological evaluation of reconstructed or regenerated ' \
                            'facial nerves in rodents.'
    assert res0['doi'] == '10.1016/j.mex.2018.03.007'
    assert len(res0['authors']) == 6
    assert res0['language'] == 'eng'

    res1 = results[1]
    abstract_parts = """Background: Traditionally perceived as a disorder of women, Eating Disorders
      (EDs) are known to have impacts on people irrespective of their gender. This
      study is designed to synthesise the available qualitative research studies to
      more broadly understand the diverse experiences of ED and their treatment,
      specifically in relationship to issues of gender. Methods: The methodology
      involved a systematic search and quality appraisal of the literature published
      after 1980 using terms that aimed to represent the primary concepts of “role of
      gender” and “treatment experiences” and “eating disorders”. Nine qualitative
      studies met the inclusion criteria. Meta-themes were inductively generated
      through a synthesis of data across themes from the relevant included papers.
      Results: Analysis of data was constructed around three meta-themes, each with
      subthemes. The first meta-theme “Out of sight, out of mind” depicted the
      experience of gender issues that were marginalised in treatment. More
      specifically for transgender people, when gender issues were ignored by treatment
      providers, this frequently led to non-disclosure of their gender identity.
      Furthermore, men were less likely to be assessed for an eating disorder and
      within this context; diagnosis of an ED and referral to specialist treatment was 
      frequently hindered. The second meta-theme “Lack of literacy among health care
      providers” focused on issues related to misdiagnosis of EDs, and the question of 
      whether this was related to a lack of health literacy amongst health
      professionals. The final theme “Pathways into treatment that address stigma and
      other barriers” highlighted the need for the development of future treatment
      interventions address the complex social reality of the experiencing person,
      including questions of gender. Conclusion: Gender issues impact upon the ED
      experience and require broader consideration in the development and evaluation of
      ED treatment interventions, including the further development of gender-informed 
      interventions. Trial registration: Protocol registered on PROSPERO 2017
      CRD42017082616. Electronic supplementary material: The online version of this
      article (10.1186/s40337-018-0207-1) contains supplementary material, which is
      available to authorized users.""".split('\n')
    expected_abstract = ' '.join(ap.strip() for ap in abstract_parts)
    assert res1['pmcid'] == 6088416
    assert res1['pubmed_id'] == 30123504
    assert res1['abstract'] == expected_abstract

    assert results[4]['publication_date'] == '2010 Mar 15'
    assert results[4]['electronic_publication_date'].year == 2010
    assert results[4]['electronic_publication_date'].month == 3

from datetime import datetime

from nbib import read, read_file


single_ref = """PMID- 28754806
OWN - NLM
STAT- MEDLINE
DCOM- 20180731
LR  - 20181202
IS  - 1759-8486 (Electronic)
IS  - 1759-8478 (Linking)
VI  - 10
IP  - 4
DP  - 2018 Apr
TI  - Impact of balloon guide catheter on technical and clinical outcomes: a systematic 
      review and meta-analysis.
PG  - 335-339
LID - 10.1136/neurintsurg-2017-013179 [doi]
AB  - BACKGROUND AND PURPOSE: Flow arrest with balloon guide catheters (BGCs) is becoming 
      increasingly recognized as critical to optimizing patient outcomes for mechanical 
      thrombectomy. And I could go on...
CI  - © Article author(s) (or their employer(s) unless otherwise stated in the text of the 
      article) 2018. All rights reserved. No commercial use is permitted unless otherwise 
      expressly granted.
FAU - Brinjikji, Waleed
AU  - Brinjikji W
AD  - Department of Radiology, Mayo Clinic, Rochester, Minnesota, USA.
AD  - Department of Neurosurgery, Mayo Clinic, Rochester, Minnesota, USA.
AD  - Department of Neuroradiology, Toronto Western Hospital, University of Toronto, 
      Toronto, Ontario, Canada.
FAU - Pereira, Vitor M
AU  - Pereira VM
AD  - Department of Neuroradiology, Toronto Western Hospital, University of Toronto, 
      Toronto, Ontario, Canada.
FAU - Kallmes, David F
AU  - Kallmes DF
AD  - Department of Radiology, Mayo Clinic, Rochester, Minnesota, USA.
AD  - Department of Neurosurgery, Mayo Clinic, Rochester, Minnesota, USA.
LA  - eng
PT  - Journal Article
PT  - Meta-Analysis
PT  - Review
PT  - Systematic Review
DEP - 20170728
PL  - England
TA  - J Neurointerv Surg
JT  - Journal of neurointerventional surgery
JID - 101517079
SB  - IM
MH  - Aged
MH  - Brain Ischemia/diagnostic imaging/*surgery
MH  - Clinical Trials as Topic/methods
OTO - NOTNLM
OT  - mechanical thrombectomy
OT  - stroke
EDAT- 2017/07/30 06:00
MHDA- 2018/08/01 06:00
CRDT- 2017/07/30 06:00
PHST- 2017/05/05 00:00 [received]
PHST- 2017/06/02 00:00 [revised]
PHST- 2017/06/09 00:00 [accepted]
PHST- 2017/07/30 06:00 [pubmed]
PHST- 2018/08/01 06:00 [medline]
PHST- 2017/07/30 06:00 [entrez]
AID - neurintsurg-2017-013179 [pii]
AID - 10.1136/neurintsurg-2017-013179 [doi]
PST - ppublish
SO  - J Neurointerv Surg. 2018 Apr;10(4):335-339. doi: 10.1136/neurintsurg-2017-013179. 
      Epub 2017 Jul 28.

"""


############
# top level (study category) attribute appendable tags
############

def test_pmid():
    results = read("PMID- 12345\n")

    assert len(results) == 1
    assert 'pubmed_id' in results[0]
    assert results[0]['pubmed_id'] == 12345


def test_ref_dates():
    results = read('LR  - 20200604\nDEP - 20191231\n')
    assert len(results) == 1
    assert 'last_revision_date' in results[0]
    assert results[0]['last_revision_date'] == datetime(2020, 6, 4)

    assert 'electronic_publication_date' in results[0]
    assert results[0]['electronic_publication_date'] == datetime(2019, 12, 31)


############
# terminal list appendable categories
############


def test_publication_type():
    results = read("PT  - Journal Article\nPT  - Meta-Analysis\nPT  - Systematic Review\n")

    assert len(results) == 1
    assert 'publication_types' in results[0]
    assert set(results[0]['publication_types']) == {'Journal Article', 'Meta-Analysis', 'Systematic Review'}


def test_read_keywords():
    results = read("OT  - thing1\nOT  - thing2\n")

    assert len(results) == 1
    assert 'keywords' in results[0]
    assert set(results[0]['keywords']) == {'thing1', 'thing2'}


def test_descriptors():
    results = read("MH  - Male\nMH  - *Humans\nMH  - Head/*Sub\n\n")

    assert len(results) == 1
    assert 'descriptors' in results[0]
    assert results[0]['descriptors'] == [{'descriptor': 'Male', 'major': False},
                                         {'descriptor': 'Humans', 'major': True},
                                         {'descriptor': 'Head', 'qualifier': 'Sub', 'major': True}]


def test_grants():
    results = read('GR  - NIH 1234\nGR  - NLM RO1\n')
    assert len(results) == 1
    assert 'grants' in results[0]
    assert set(results[0]['grants']) == {'NIH 1234', 'NLM RO1'}

#############
# attribute appendable nested beneath list appendable
#############


def test_read_authors():
    results = read("FAU - Karl J Holub\nAU  - KJ Holub\nAD  - Nested Knowledge Inc., Minneapolis, MN\nAD  - Duluth, MN\nFAU - Other Author\n")

    assert len(results) == 1
    assert 'authors' in results[0]
    assert len(results[0]['authors']) == 2
    assert {'author': 'Other Author'} in results[0]['authors']
    assert {'author': 'Karl J Holub',
            'author_abbreviated': 'KJ Holub',
            'affiliations': ['Nested Knowledge Inc., Minneapolis, MN',
                             'Duluth, MN']} in results[0]['authors']

############
# full refs with mixed categories
############


def test_read_full_single_ref():
    results = read(single_ref)

    assert len(results) == 1

    result = results[0]
    target_study_attributes = {
        'pubmed_id': 28754806,
        'citation_owner': 'NLM',
        'electronic_issn': '1759-8486',
        'linking_issn': '1759-8478',
        'journal_volume': '10',
        'journal_issue': '4',
        'publication_date': '2018 Apr',
        'title': 'Impact of balloon guide catheter on technical and clinical outcomes: a systematic review and meta-analysis.',
        'pages': '335-339',
        'doi': '10.1136/neurintsurg-2017-013179',
        'abstract': 'BACKGROUND AND PURPOSE: Flow arrest with balloon guide catheters (BGCs) is becoming increasingly recognized as critical to optimizing patient outcomes for mechanical thrombectomy. And I could go on...',
        'copyright': '© Article author(s) (or their employer(s) unless otherwise stated in the text of the article) 2018. All rights reserved. No commercial use is permitted unless otherwise expressly granted.',
        'language': 'eng',
        'electronic_publication_date': datetime(2017, 7, 28),
        'place_of_publication': 'England',
        'journal_abbreviated': 'J Neurointerv Surg',
        'journal': 'Journal of neurointerventional surgery',
        'nlm_journal_id': '101517079',
        'publication_status': 'ppublish',
        'entrez_time': datetime(2017, 7, 30, 6),
        'medline_time': datetime(2018, 8, 1, 6),
        'received_time': datetime(2017, 5, 5)
    }

    for att, value in target_study_attributes.items():
        assert att in result
        assert result[att] == value

    target_authors = [
        {
            "author": "Brinjikji, Waleed",
            "author_abbreviated": "Brinjikji W",
            "affiliations": [
                "Department of Radiology, Mayo Clinic, Rochester, Minnesota, USA.",
                "Department of Neurosurgery, Mayo Clinic, Rochester, Minnesota, USA.",
                "Department of Neuroradiology, Toronto Western Hospital, University of Toronto, Toronto, Ontario, Canada."
            ],
            'first_name': 'Waleed',
            'last_name': 'Brinjikji',
        },
        {
            "author": "Pereira, Vitor M",
            "author_abbreviated": "Pereira VM",
            "affiliations": [
                "Department of Neuroradiology, Toronto Western Hospital, University of Toronto, Toronto, Ontario, Canada."
            ],
            'first_name': 'Vitor M',
            'last_name': 'Pereira',
        },
        {
            "author": "Kallmes, David F",
            "author_abbreviated": "Kallmes DF",
            "affiliations": [
                "Department of Radiology, Mayo Clinic, Rochester, Minnesota, USA.",
                "Department of Neurosurgery, Mayo Clinic, Rochester, Minnesota, USA."
            ],
            'first_name': 'David F',
            'last_name': 'Kallmes'
        }
    ]

    for auth in target_authors:
        assert auth in result['authors']

    target_keywords = ['mechanical thrombectomy', 'stroke']
    for key in target_keywords:
        assert key in result['keywords']

    target_publication_types = ['Journal Article', 'Meta-Analysis', 'Systematic Review', 'Review']
    for pt in target_publication_types:
        assert pt in result['publication_types']

    target_mesh = [
        {'descriptor': 'Aged',  'major':  False},
        {'descriptor': 'Brain Ischemia', 'qualifier': 'diagnostic imaging', 'major': False},
        {'descriptor': 'Brain Ischemia', 'qualifier': 'surgery', 'major': True},
        {'descriptor': 'Clinical Trials as Topic', 'qualifier': 'methods', 'major': False},

    ]
    for d in target_mesh:
        assert d in result['descriptors']

##########
# multiple refs
##########


def test_read_multiple_simple_refs():
    results = read('PMID- 1\n\nPMID- 2\n\nPMID- 3\n\n')

    assert len(results) == 3
    assert all(['pubmed_id' in ref for ref in results])
    assert set(ref['pubmed_id'] for ref in results) == {1, 2, 3}


def test_read_multiple_complex_refs():
    results = read('PMID- 1\nTI  - Nice Title\nFAU - Karl\nAD  - Minnesota\n\nPMID- 2\nTI  - Another \n      Continuation\nPT  - Journal Article\nOT  - fun\nOT  - stuff\n\n')

    assert len(results) == 2
    assert set(ref['pubmed_id'] for ref in results) == {1, 2}
    assert set(ref['title'] for ref in results) == {'Nice Title', 'Another Continuation'}



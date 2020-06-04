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
      thrombectomy. We performed a systematic review and meta-analysis of the literature 
      for studies that compared angiographic and clinical outcomes for patients who 
      underwent mechanical thrombectomy with and without BGCs. MATERIALS AND METHODS: In 
      April 2017 a literature search on BGC and mechanical thrombectomy for stroke was 
      performed. All studies included patients treated with and without BGCs using modern 
      techniques (ie, stent retrievers). Using random effects meta-analysis, we evaluated 
      the following outcomes: first-pass recanalization, Thrombolysis In Cerebral 
      Infarction (TICI) 3 recanalization, TICI 2b/3 recanalization, favorable outcome 
      (modified Rankin Scale (mRS) 0-2), mortality, and mean number of passes and 
      procedure time. RESULTS: Five non-randomized studies of 2022 patients were included 
      (1083 BGC group and 939 non-BGC group). Compared with the non-BGC group, patients 
      treated with BGCs had higher odds of first-pass recanalization (OR 2.05, 95% CI 1.65 
      to 2.55), TICI 3 (OR 2.13, 95% CI 1.43 to 3.17), TICI 2b/3 (OR 1.54, 95% CI 1.21 to 
      1.97), and mRS 0-2 (OR 1.84, 95% CI 1.52 to 2.22). BGC-treated patients also had 
      lower odds of mortality (OR 0.52, 95% CI 0.37 to 0.73) compared with non-BGC 
      patients. The mean number of passes was significantly lower for BGC-treated patients 
      (weighted mean difference -0.34, 95% CI-0.47 to -0.22). Mean procedure time was also 
      significantly shorter for BGC-treated patients (weighted mean difference -7.7 min, 
      95% CI-9.0to -6.4). CONCLUSIONS: Non-randomized studies suggest that BGC use during 
      mechanical thrombectomy for acute ischemic stroke is associated with superior 
      clinical and angiographic outcomes. Further randomized trials are needed to confirm 
      the results of this study.
CI  - © Article author(s) (or their employer(s) unless otherwise stated in the text of the 
      article) 2018. All rights reserved. No commercial use is permitted unless otherwise 
      expressly granted.
FAU - Brinjikji, Waleed
AU  - Brinjikji W
AD  - Department of Radiology, Mayo Clinic, Rochester, Minnesota, USA.
AD  - Department of Neurosurgery, Mayo Clinic, Rochester, Minnesota, USA.
AD  - Department of Neuroradiology, Toronto Western Hospital, University of Toronto, 
      Toronto, Ontario, Canada.
FAU - Starke, Robert M
AU  - Starke RM
AD  - Department of Neurological Surgery, Miami Miller School of Medicine, University of 
      Miami Hospital, Miami, Florida, USA.
AD  - Department of Radiology, University of Miami Hospital, Miami Miller School of 
      Medicine, Miami, Florida, USA.
FAU - Murad, M Hassan
AU  - Murad MH
AD  - Evidence-based Practice Center, Mayo Clinic, Rochester, Minnesota, USA.
FAU - Fiorella, David
AU  - Fiorella D
AD  - Department of Neurosurgery, State University of New York at Stony Brook, Stony Brook 
      University Medical Center, Stony Brook, New York, USA.
FAU - Pereira, Vitor M
AU  - Pereira VM
AD  - Department of Neuroradiology, Toronto Western Hospital, University of Toronto, 
      Toronto, Ontario, Canada.
FAU - Goyal, Mayank
AU  - Goyal M
AD  - Department of Diagnostic Imaging, University of Calgary, Calgary, Alberta, Canada.
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
MH  - Catheterization/instrumentation/*methods
MH  - Clinical Trials as Topic/methods
MH  - Female
MH  - Humans
MH  - Male
MH  - Middle Aged
MH  - Stents
MH  - Stroke/diagnostic imaging/*surgery
MH  - Thrombectomy/instrumentation/*methods
MH  - Treatment Outcome
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


def test_read_single_ref():
    results = read(single_ref)
    print(results)
    assert False

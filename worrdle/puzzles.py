"""The list of Worrdle puzzles, one per date."""

from datetime import date

from worrdle.game import Puzzle

PUZZLES: list[Puzzle] = [
    Puzzle(
        puzzle_date=date(2026, 10, 19),
        secret="acute",
        is_jargon=True,
        counterpart="sudden; it came on quickly",
        clinical_example="Acute Kidney Injury (AKI), defined as an abrupt loss in"
        " kidney function, is common, occurring in 5-20% of hospitalized patients, and"
        " carries a significant and independent risk of inpatient mortality.",
        plain_example="This study tested whether a kidney doctor and a pharmacist"
        " could help hospital teams care for patients whose kidneys suddenly stopped"
        " working well.",
        why_it_matters="This trial enrolled 4,003 hospital patients under a waiver of"
        " consent. If patients or families learn about a study like this later, from a"
        " notice or a results summary, the words have to make sense on their own. In"
        " CTSA-supported research at Vanderbilt, 80% of AKI survivors near discharge"
        " did not know they had AKI. 'Sudden kidney damage' says what happened.",
        source_name="ClinicalTrials.gov",
        nct_number="NCT04040296",
        study_title="Personalized Recommendations for Acute Kidney Injury (AKI) Care",
    ),
    Puzzle(
        puzzle_date=date(2026, 10, 20),
        secret="obese",
        is_jargon=True,
        counterpart="at a weight that is higher than is healthy; unhealthy weight",
        clinical_example="primary caregiver who is either overweight (BMI 25.0 to"
        " 29.9) or obese (BMI≥30) and willing to participate in treatment",
        plain_example="We are looking for Black teens ages 12 to 17 who want to reach"
        " a healthier weight, plus a parent or caregiver who lives with them and will"
        " take part too.",
        why_it_matters="In a national survey of 445 parents, 'obese' and 'extremely"
        " obese' were rated among the most stigmatizing and least motivating words a"
        " provider could use about a child's weight. Parents liked 'weight' and"
        " 'unhealthy weight' best. This study needs a teen and a caregiver to join"
        " together, and a family that feels judged by a flyer may never call.",
        source_name="ClinicalTrials.gov",
        nct_number="NCT04974554",
        study_title="FIT Families Multicomponent Obesity Intervention for African"
        " American Adolescents",
    ),
    Puzzle(
        puzzle_date=date(2026, 10, 21),
        secret="fetal",
        is_jargon=True,
        counterpart="the unborn baby's, as in 'the baby is not growing as expected'",
        clinical_example="This study proposes administering a daily dose of 40 mg of"
        " pravastatin between 24 and 29.6 weeks of gestation to mothers diagnosed with"
        " preeclampsia and/or fetal growth restriction.",
        plain_example="This study tests a daily pill for women 24 to 29 weeks pregnant"
        " who have serious blood pressure problems or whose baby is not growing as"
        " expected.",
        why_it_matters="In a 2026 study of 24 parents told their baby was not growing"
        " as expected, many searched online to learn what the medical terms in their"
        " care meant. This trial asks women to decide about a study drug soon after a"
        " frightening diagnosis. Words like 'your baby's growth' are easier to take in"
        " at that moment than 'fetal growth restriction.'",
        source_name="ClinicalTrials.gov",
        nct_number="NCT07098975",
        study_title="Statin Intervention for Severe Early-Onset Placental"
        " Insufficiency. (STATIN-PRE Trial)",
    ),
    Puzzle(
        puzzle_date=date(2026, 10, 22),
        secret="frail",
        is_jargon=True,
        counterpart="weaker, slower, or more tired than before",
        clinical_example="The goal of this behavioral clinical trial is to compare two"
        " different ways of becoming less sedentary and more active in 60 older adults"
        " at elevated risk of becoming frail.",
        plain_example="We want to learn which is easier for people 65 and older who"
        " are not very active: one 30-minute walk a day, or three 10-minute walks.",
        why_it_matters="In interviews, many older adults in England did not want to"
        " see themselves as frail. Some who were called 'old and frail' by others"
        " pulled back from social and physical activity. This study hopes to get"
        " inactive adults 65 and older walking more, so a flyer that leads with"
        " 'frail' could work against its own goal.",
        source_name="ClinicalTrials.gov",
        nct_number="NCT06023680",
        study_title="The Sedentary to Active Rising to Thrive (START) Trial",
    ),
    Puzzle(
        puzzle_date=date(2026, 10, 23),
        secret="viral",
        is_jargon=True,
        counterpart="the amount of HIV in your blood, as in 'viral load'",
        clinical_example='A viral load that measures as "undetectable" (i.e., fewer'
        " than 200 copies of HIV per millilitre of blood) will represent virologic"
        " suppression, which is a positive indication of HIV health.",
        plain_example="If you just learned you have HIV and are starting care for the"
        " first time, this study tests a short program to help you keep going to your"
        " clinic visits.",
        why_it_matters="In a study of people living with HIV, those with lower health"
        " literacy were less likely to know their viral load. Those who did know the"
        " number were less likely to understand what it meant. This trial enrolls"
        " people entering HIV care for the first time, when 'viral load' and 'virologic"
        " suppression' may be new words.",
        source_name="ClinicalTrials.gov",
        nct_number="NCT04201288",
        study_title="Brief Acceptance-Based Retention Intervention for Newly"
        " Diagnosed HIV Patients",
    ),
    Puzzle(
        puzzle_date=date(2026, 10, 24),
        secret="sugar",
        is_jargon=False,
        counterpart="glycemic control; blood glucose; HbA1c",
        clinical_example="Glycated hemoglobin (HbA1c) is the average blood glucose"
        " levels in past 3 months (HbA1c); higher percentages reflect higher levels of"
        " blood glucose (worse blood glucose management).",
        plain_example="In this program, promotores (community health workers) call"
        " Hispanic and Latino adults with type 2 diabetes to help them manage their"
        " blood sugar.",
        why_it_matters="Among 408 English- and Spanish-speaking adults with type 2"
        " diabetes at a public hospital, those with inadequate health literacy were"
        " about twice as likely to have poor glycemic control. This study is run in"
        " English and Spanish by community health workers. 'Blood sugar' is a term"
        " people already use at home, so they can act on it.",
        source_name="ClinicalTrials.gov",
        nct_number="NCT06445725",
        study_title="Acceptance Based Coping Skills for Diabetes Delivered By"
        " Promotores",
    ),
    Puzzle(
        puzzle_date=date(2026, 10, 25),
        secret="fecal",
        is_jargon=True,
        counterpart="stool (poop)",
        clinical_example="Eligible patients will be mailed a fecal immunochemical test"
        " (FIT).",
        plain_example="Some patients will get a colon cancer test in the mail. You"
        " take a small sample of your poop at home and mail it back.",
        why_it_matters="At a Latino-serving health center, patients preferred FIT"
        " instructions with almost no words over a 415-word version. In another trial,"
        " low-literacy instructions and reminder calls cut mishandled samples. Rural"
        " Medicaid patients in this study do the test alone at home, so each step has"
        " to make sense without a nurse in the room.",
        source_name="ClinicalTrials.gov",
        nct_number="NCT04890054",
        study_title="Screening More Patients for Colorectal Cancer Through Adapting"
        " and Refining Targeted Evidence-Based Interventions in Rural Settings,"
        " SMARTER CRC",
    ),
    Puzzle(
        puzzle_date=date(2026, 10, 26),
        secret="flare",
        is_jargon=False,
        counterpart="exacerbation; a period of increased disease activity",
        clinical_example="The purpose of this study is to evaluate the efficacy,"
        " safety, and tolerability of belimumab in adult patients of black race with"
        " systemic lupus erythematosus (SLE; lupus).",
        plain_example="Researchers will track how long it takes before a person has a"
        " bad lupus flare, a time when symptoms like joint pain, tiredness, or rashes"
        " get worse.",
        why_it_matters="One review found Black patients make up 43% of people with"
        " lupus but 14% of lupus trial enrollees. This trial enrolled only Black"
        " adults. 'Flare' is the patients' own word, but in interviews patients"
        " described flares by symptoms, while doctors meant measured disease activity."
        " Materials should say which meaning they use.",
        source_name="ClinicalTrials.gov",
        nct_number="NCT01632241",
        study_title="Efficacy and Safety of Belimumab in Black Race Patients With"
        " Systemic Lupus Erythematosus (SLE)",
    ),
    Puzzle(
        puzzle_date=date(2026, 10, 27),
        secret="taper",
        is_jargon=True,
        counterpart="slowly lower a medicine dose over time",
        clinical_example="The pharmacist will then follow-up with the participant by"
        " phone each week until surgery to assess progress and adjust the taper as"
        " necessary.",
        plain_example="If you take opioid pain medicine and plan to have a knee or hip"
        " replacement, a pharmacist can help you slowly lower your dose before surgery.",
        why_it_matters="In interviews with 21 adults reducing long-term opioids, pain"
        " and the need for medicine changed from day to day. Patients talked about the"
        " work of tapering with clinicians briefly, if at all. The authors urged"
        " clinicians to address fears and make plans that can change. Saying 'slowly"
        " lower your dose' tells people the plan is gradual.",
        source_name="ClinicalTrials.gov",
        nct_number="NCT05788016",
        study_title="Developing an Opioid Taper Intervention Before Total Joint"
        " Arthroplasty",
    ),
]

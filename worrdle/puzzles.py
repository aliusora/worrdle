"""The list of Worrdle puzzles, one per date."""

from datetime import date

from worrdle.game import Puzzle

PUZZLES: list[Puzzle] = [
    Puzzle(
        puzzle_date=date(2026, 10, 17),
        secret="acute",
        is_jargon=True,
        counterpart="sudden start, short term, quick",
        clinical_example="In this randomized clinical trial, a 'Kidney Action Team'"
        " will provide timely, personalized recommendations for the diagnosis and"
        " initial treatment of hospitalized patients with Acute Kidney Injury.",
        plain_example="This study tests whether a specialized team of doctors can"
        " improve early care for patients who suddenly develop kidney problems.",
        why_it_matters="Using plain language in this specific situation matters because"
        " acute kidney injury (AKI) is an unexpected, fast-moving medical emergency"
        " that often happens to patients who are already very sick with other"
        " conditions. When studies use complicated medical terms, it creates severe"
        " barriers to recruitment.",
        source_name="ClinicalTrials.gov",
        nct_number="NCT04040296",
        study_title="Personalized Recommendations for Acute Kidney Injury (AKI) Care",
    ),
]

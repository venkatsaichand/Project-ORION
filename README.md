# Project ORION
## Six Sigma & Business Analytics | Independent E-Commerce Delivery Reliability Case Study

Project ORION is an independent, end-to-end Six Sigma and Business Analytics case study applying the **DMAIC (Define, Measure, Analyze, Improve, Control)** methodology to historical Brazilian e-commerce delivery data. It investigates delivery reliability, establishes a data-validated baseline, examines process-stage and customer-experience patterns, develops evidence-qualified improvement hypotheses, and translates the analysis into a proposed pilot and control strategy.

The project demonstrates how structured process-improvement methods and reproducible data analysis can move from an operational problem statement to measurable performance evidence and actionable improvement design.

> **Independence and project status:** This is an independent portfolio study based on a public historical dataset. It was not commissioned by, conducted for, or implemented at Olist. Findings describe the supplied historical data, not Olist's current operations. Proposed interventions, owners, pilots, targets and controls are recommendations—not implemented changes or verified operational results.

---

## Project at a Glance

| Area | Description |
|---|---|
| Project | Project ORION |
| Disciplines | Six Sigma, Operational Excellence and Business Analytics |
| Framework | DMAIC |
| Business problem | Delivery reliability in a Brazilian e-commerce marketplace dataset |
| Primary CTQ | Late delivery, measured by comparing actual and estimated delivery calendar dates |
| Analytical cohort | 96,203 eligible delivered orders |
| Historical purchase period | 1 January 2017 – 31 August 2018 |
| Primary baseline | 6.79% late deliveries |
| Analysis | Data validation, descriptive analysis, statistical inference, process variation and segment analysis |
| Status | Historical analysis and improvement design completed; no operational intervention implemented |
| Main technologies | Python, Pandas, NumPy and SciPy |

## Executive Summary

The analysis establishes a reconciled baseline of **6,531 late deliveries among 96,203 eligible delivered orders**, equivalent to a calendar-date late-delivery rate of **6.79%**. The conventional 95% Wilson confidence interval is **6.63%–6.95%**.

A key data-quality finding materially affects the measurement definition: **all 96,203 estimated-delivery timestamps are recorded at midnight**. The primary CTQ therefore uses calendar dates rather than treating the estimated timestamp as a precise time-of-day commitment. A timestamp-based sensitivity definition produces a higher late rate of 8.13%, illustrating why operational definitions and source-data precision must be validated before performance is reported.

The analysis also examines elapsed-time proxies between order approval, carrier handoff and customer delivery; weekly process variation; destination geography; product categories; seller-related indicators; and customer reviews. Late orders have substantially lower latest review scores on average, but these observed relationships are associations and do not establish causation.

The project concludes with evidence-qualified root-cause hypotheses, a prioritized countermeasure portfolio, an illustrative controlled-pilot design, proposed KPIs and a control strategy. These are recommendations requiring current operational data, process-owner validation and a properly governed pilot before implementation or impact claims can be made.

## DMAIC Approach

### 1. Define
- Frame delivery reliability as the business problem.
- Define the primary Critical-to-Quality (CTQ) measure and eligible measurement cohort.
- Establish project scope, assumptions, stakeholders and analytical boundaries.
- Map the high-level order-to-delivery process and identify information needed to investigate performance.

### 2. Measure
- Load and integrate the nine supplied source tables.
- Assess data completeness, timestamp precision, key integrity and join behavior.
- Build a reproducible order-level analytical dataset.
- Establish the calendar-date late-delivery baseline and confidence interval.
- Reconcile counts and validate key analytical outputs.

### 3. Analyze
- Examine delivery performance across time, process-stage proxies and destination segments.
- Use descriptive and inferential statistics to compare observed groups.
- Apply a Laney p′ control chart to assess weekly variation.
- Examine customer-review patterns and item-level category summaries.
- Develop root-cause hypotheses while distinguishing evidence from assumptions.

### 4. Improve
- Identify and prioritize potential countermeasures against observed patterns and evidence gaps.
- Develop an illustrative controlled-pilot framework, including sample-size considerations and operational guardrails.
- Define additional event-level data required to validate hypotheses and evaluate interventions.

### 5. Control
- Propose a KPI and monitoring framework.
- Define control-plan elements, escalation logic and ownership requirements.
- Specify the evidence and governance needed to sustain any future improvement.
- Separate proposed controls from controls that have actually been deployed.

## Key Findings

| Measure | Result |
|---|---:|
| Eligible delivered orders | 96,203 |
| Calendar-date late deliveries | 6,531 |
| Calendar-date late-delivery rate | **6.79%** |
| Conventional 95% Wilson confidence interval | 6.63%–6.95% |
| Timestamp-based late-delivery rate (sensitivity) | 8.13% |
| Estimated-delivery timestamps recorded at midnight | 100.00% |
| Orders with a latest scored review | 95,560 (99.33%) |
| Mean latest review score — on-time group | 4.291 |
| Mean latest review score — late group | 2.271 |

These results relate to the historical dataset and its measurement rules. They are not current marketplace performance, causal estimates, or proof of responsibility by a particular seller, carrier or process stage.

## Skills Demonstrated

### Six Sigma & Operational Excellence
- DMAIC methodology and project charter development
- Critical-to-Quality (CTQ) identification and operationalization
- High-level process mapping and stakeholder requirements analysis
- Process performance measurement and Statistical Process Control (SPC)
- Control-plan and operational-monitoring design

### Data Analytics & Data Management
- Data cleaning, transformation, quality assessment and validation
- Data reconciliation, integrity checks and multi-table integration
- Order-level and item-level analytical data modeling
- Reproducible analytical pipeline development
- Segment analysis across time, geography, categories and customer reviews

### Statistical Analysis
- Descriptive and inferential statistics
- Mann–Whitney U test and Welch's two-sample t-test
- Wilson score confidence intervals
- Effect-size interpretation, including rank-biserial correlation
- Laney p′ control-chart analysis
- Defects per Million Opportunities (DPMO) and descriptive sigma-level calculation
- Pilot sample-size estimation and interpretation of statistical limitations

### Business Analysis & Improvement Design
- Process-stage and delivery-performance analysis
- Customer-experience and review analysis
- Fishbone/Ishikawa analysis and exploratory 5 Whys
- Evidence-qualified root-cause hypothesis development
- Countermeasure identification and prioritization
- Controlled-pilot design and Intention-to-Treat (ITT) framework
- KPI development, operational guardrails and control-strategy design

### Communication & Decision Support
- Executive reporting and evidence-based recommendations
- Interpretation of statistical results in an operational context
- Communication of assumptions, limitations and uncertainty
- Distinguishing association from causation and recommendations from implemented outcomes

## Tools & Technologies

| Tool / Technology | Role in the project |
|---|---|
| Python | Analytical programming and reproducible workflows |
| Pandas | Data preparation, transformation, joining and aggregation |
| NumPy | Numerical computation |
| SciPy | Statistical calculations and inference |
| Statsmodels | Statistical analysis in the broader report environment |
| Matplotlib | Data visualization in the broader report environment |
| GitHub | Source-code and project publication |

The repository pipeline's direct Python dependencies are listed in `requirements.txt`. Statsmodels and Matplotlib are included in the broader analytical environment documented in the report; they should not be interpreted as required imports for every pipeline script.

## Repository Structure

```text
Project-ORION/
├── README.md
├── requirements.txt
├── config.json
├── run_all.py
├── src/
│   └── orion_pipeline.py
├── data/
│   ├── raw/                 # Local source CSV files; not committed
│   └── processed/           # Generated analytical tables; not committed
├── outputs/                 # Generated summaries and validation outputs
├── tests/
│   └── test_helpers.py
├── docs/                    # Supporting methodology and project notes
└── deliverables/
    ├── Executive_Overview.pdf
    ├── Project_Brief.pdf
    └── Final_Project_Report.pdf
```

The exact contents of supporting folders may evolve as the repository is updated. Raw source data and locally generated intermediate files are intentionally excluded from version control.

## Reproducing the Pipeline

### Requirements
- Python 3.10 or later (use a version compatible with the installed dependencies)
- The nine source CSV files from the public Brazilian E-Commerce dataset used in this study
- Packages listed in `requirements.txt`

### Setup

Clone the repository and move into the project directory:

```bash
git clone https://github.com/venkatsaichand/Project-ORION.git
cd Project-ORION
```

Create and activate a virtual environment.

**Windows PowerShell**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the pipeline dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Add the Source Data

Download the public Olist Brazilian E-Commerce dataset from Kaggle and place the nine required CSV files in `data/raw/`, using the filenames expected by the pipeline.

Raw data is not included in this repository. Keep the files local; do not commit the original CSVs or generated intermediate datasets.

### Run

From the repository root:

```bash
python run_all.py
```

The pipeline reads the configured source data, performs analytical preparation and validation, and writes generated summaries and validation outputs to the project output folders. Review the console validation results and generated files before using any output in a report or downstream analysis.

## Project Deliverables

The `deliverables/` directory contains:
- **Executive Overview** — concise summary of the problem, baseline, findings and recommendations.
- **Project Brief** — condensed account of the DMAIC work, conclusions and next steps.
- **Final Project Report** — full technical report with detailed analysis, statistical methods, limitations, references and appendices.

The repository also contains analytical code and supporting project materials. An interactive Power BI dashboard is a separate supplementary deliverable and is not represented here as a completed output.

## Data, Methodological Boundaries & Limitations

This project uses the public historical Brazilian E-Commerce dataset commonly known as the Olist Brazilian E-Commerce Public Dataset. The analysis is limited to the fields and records supplied in that dataset.

- The cohort and baseline are historical; they are not a current operational benchmark.
- All estimated-delivery timestamps in the eligible cohort are recorded at midnight, which is why the calendar-date definition is used as the primary CTQ.
- Stage durations are timestamp-derived proxies. They do not provide complete warehouse, seller, carrier or last-mile event histories.
- Stage comparisons share the delivery endpoint with the late-delivery outcome and are mathematically coupled; they are not independent proof of root cause.
- Review comparisons are observational and may be affected by selection and other biases.
- Category summaries are based on item-level records and should not be interpreted as order-level category performance.
- The available data does not establish that a specific seller, carrier, geography or process stage caused late delivery.
- The dataset does not provide intervention assignments, finance-approved cost inputs or implementation records needed to verify causal impact, realized savings or ROI.
- Proposed pilots, countermeasures, owners, KPIs and controls are recommendations requiring operational validation and approval.

These limitations keep conclusions proportionate to the evidence and identify the additional data needed for a real operational deployment.

## Data Source & References

**Dataset:** Olist Brazilian E-Commerce Public Dataset, published on Kaggle.

The dataset is used for independent educational and portfolio analysis. This repository is not an official Olist product, publication or operational project.

The full report provides detailed references and methodological sources used in the study, including references for the statistical and process-control methods.

---

## Author

**Project ORION**  
Independent Six Sigma, Operational Excellence and Business Analytics portfolio case study.

For questions, feedback or discussion about the analytical approach, please use the repository's GitHub Issues or Discussions.

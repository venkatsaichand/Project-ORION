PROJECT ORION

Six Sigma & Business Analytics | DMAIC Case Study

Applying Six Sigma methodology and business analytics to investigate delivery reliability, identify improvement opportunities, and design a measurable control framework.

Project ORION is an independent end-to-end Six Sigma and Business Analytics case study using the public Olist Brazilian e-commerce dataset.

The project demonstrates how a structured DMAIC (Define, Measure, Analyze, Improve, Control) approach can turn operational data into a measurable business problem, a defensible performance baseline, evidence-led investigation, prioritized improvement proposals, and a proposed control plan.

This is an independent portfolio study. It was not commissioned by, affiliated with, or implemented at Olist.

Project at a Glance

Area

Application

Business problem

Delivery reliability and missed customer delivery commitments

Methodology

Six Sigma DMAIC

Analytical focus

Operational performance, process variation, customer experience, and improvement opportunities

Dataset

Public Brazilian Olist e-commerce dataset

Tools

Python, Pandas, NumPy, SciPy, Excel, and Power BI (dashboard planned)

Deliverable

Business case study, statistical analysis, improvement design, and control framework

Applying the DMAIC Framework

1. Define — Establish the business problem

Translated the customer expectation of receiving an order by its promised date into a measurable Critical-to-Quality (CTQ).

Developed the problem statement, project charter, scope, stakeholder considerations, and high-level process map.

Defined the unit of analysis and operational measure for delivery reliability.

2. Measure — Establish a defensible baseline

Assessed data quality, completeness, key integrity, duplicates, and relationships across nine source datasets.

Reconciled the eligible delivered-order cohort.

Defined the primary performance measure and quantified historical delivery performance.

Used statistical estimation to communicate baseline uncertainty.

3. Analyze — Investigate process performance

Applied statistical process monitoring using a Laney p′ chart to examine weekly variation.

Investigated delivery performance across process stages, destination states, sellers, product categories, and customer reviews.

Used statistical comparisons and effect measures to distinguish observed patterns from unsupported causal claims.

Identified areas requiring better operational data before root causes can be confirmed.

4. Improve — Develop evidence-led countermeasures

Developed and prioritized proposed interventions based on the observed process gaps.

Designed illustrative pilot scenarios and sample-size calculations.

Defined experimental principles, outcome measures, and operational guardrails to evaluate whether proposed changes work.

5. Control — Design a sustainable monitoring framework

Proposed performance indicators, monitoring triggers, escalation principles, ownership considerations, and review cadence.

Designed a control approach to monitor delivery reliability and sustain improvements after a successful pilot.

Distinguished proposed controls from changes actually implemented in an operating organization.

Business Analytics and Six Sigma Techniques

The project brings together:

CTQ definition and operationalization

Project charter and process mapping

Data-quality assessment and cohort reconciliation

Order-level data modeling and aggregation

Descriptive and inferential statistics

Confidence intervals and effect-size interpretation

Statistical process control (SPC) using a Laney p′ chart

Process-stage and customer-experience analysis

Countermeasure prioritization

Pilot design and sample-size estimation

KPI design and control planning

Project Deliverables

The repository contains the analytical pipeline, supporting documentation, validation evidence, and reproducible summary outputs.

The accompanying project documents provide the business-facing explanation and detailed evidence:

Executive Overview — concise presentation of the business problem, key findings, DMAIC application, and recommended direction.

Project Brief — project charter, phase-by-phase summary, analytical findings, improvement portfolio, and control design.

Final Project Report — detailed methodology, analysis, statistical evidence, recommendations, limitations, and appendices.

See the deliverables/ folder.

Tools and Implementation

Python: analytical pipeline and reproducible data preparation

Pandas and NumPy: data manipulation and numerical analysis

SciPy: statistical calculations

Power BI: planned supplementary interactive dashboard

The pipeline can be run from the project root after obtaining and placing the original source CSV files in data/raw/. Setup instructions and analytical definitions are provided in docs/.

Evidence and Limitations

The analysis uses historical observational data. Statistical associations and process-monitoring signals help identify where further investigation is warranted; they do not independently establish root causes or assign responsibility.

The proposed countermeasures and control framework are recommendations, not implemented operational changes. The available dataset does not support claims of realized savings, verified ROI, or current Olist performance.

Repository Structure

Project-ORION/
├── data/              # Source-data location and generated analytical data
├── docs/              # Methodology, data dictionary, and technical guidance
├── deliverables/      # Executive overview, project brief, and final report
├── outputs/            # Validated analytical summaries and evidence
├── src/                # Python analytical pipeline
├── tests/              # Helper tests
├── README.md
├── config.json
├── requirements.txt
└── run_all.py

Project ORION — Independent Six Sigma & Business Analytics Case Study

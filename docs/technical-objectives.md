# Technical Objectives

The technical objectives of the Adaptive Model Risk project are intended to translate the research questions into measurable and reproducible analyses.

## Objective 1 — Measure Data Distribution Shift

Implement and compare methods for detecting changes in model-input distributions over time.

Potential methods include:

- Population Stability Index;
- Kolmogorov-Smirnov statistics;
- Wasserstein distance;
- Jensen-Shannon divergence;
- multivariate drift detection;
- classifier-based drift detection.

The final set of methods will be determined through literature review and empirical evaluation.

## Objective 2 — Monitor Model Outputs and Performance

Develop methods for tracking changes in:

- predicted probability distributions;
- classification performance;
- ranking or discrimination;
- calibration;
- prediction error;
- observed outcome rates.

Metrics will depend on the specific modeling task and dataset.

## Objective 3 — Identify Changes in Predictor–Outcome Relationships

Investigate whether changes in the relationship between predictors and outcomes can be detected independently of simple changes in predictor distributions.

This component will focus on forms of concept drift or conditional-distribution change that may materially affect model reliability.

## Objective 4 — Develop Model-Aware Drift Measures

Investigate methods for weighting observed distribution changes according to their relevance to model behavior.

Potential approaches may consider:

- feature importance;
- model sensitivity;
- partial dependence;
- local or global explanations;
- interaction effects;
- changes in predictive contribution.

The goal is to distinguish statistically observable drift from drift that materially affects predictions.

## Objective 5 — Evaluate Models Across Economic Regimes

Compare model performance and monitoring indicators across different historical economic conditions.

Potential regime definitions may incorporate variables such as:

- unemployment;
- interest rates;
- inflation;
- credit conditions;
- housing-market conditions;
- delinquency or default environments.

## Objective 6 — Conduct Controlled Stress Experiments

Create controlled changes in data distributions or predictor–outcome relationships in order to measure model sensitivity.

These experiments may help establish links between:

\[
\text{environmental change}
\rightarrow
\text{model response}
\rightarrow
\text{performance degradation}
\]

## Objective 7 — Develop Diagnostic Signals

Investigate whether multiple monitoring indicators can be combined to identify:

- the likely source of model deterioration;
- the severity of deterioration;
- whether deterioration appears temporary or structural.

## Objective 8 — Evaluate Potential Remediation Strategies

Where feasible, compare different responses to model deterioration, including:

- continued monitoring;
- recalibration;
- threshold adjustment;
- retraining;
- model redevelopment.

The project will evaluate these approaches empirically rather than prescribe institution-specific governance decisions.

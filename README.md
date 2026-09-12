# Adaptive Model Risk

**Adaptive Model Risk** is an open-source research project focused on detecting and diagnosing deterioration in predictive models when the economic environment, population, or underlying relationships in the data change over time.

## Baseline Model Experiment

The first reproducible experiment is now available.

The baseline notebook creates a controlled synthetic credit-risk environment, generates borrower default outcomes from a known probability-of-default process, trains a logistic regression model, and establishes reference performance metrics for later model-deterioration experiments.

**Baseline test performance**

| Metric                    |  Value |
| ------------------------- | -----: |
| ROC AUC                   |  0.839 |
| Brier Score               | 0.0683 |
| Log Loss                  | 0.2368 |
| Calibration Error         | 0.0042 |
| MAE vs. Synthetic True PD | 0.0028 |

These results represent a deliberately healthy baseline model. Subsequent experiments keep the trained model fixed while changing the operating environment to study covariate drift, concept drift, calibration deterioration, and model-performance degradation.


[View the baseline notebook](notebooks/01_baseline_model.ipynb)

### Baseline Calibration

![Baseline model calibration](figures/baseline_calibration.png)

> **Note:** The current experiment uses synthetic data and an intentionally controlled data-generating process. It is designed to study model-risk mechanisms and should not be interpreted as a production credit-risk model or as representative of any financial institution.

## Controlled Model Deterioration Experiments

The second reproducible experiment keeps the trained baseline model fixed and evaluates it under controlled future environments.

The experiments independently manipulate:

$$
P(X)
$$

and:

$$
P(Y \mid X)
$$

to distinguish input-distribution drift from deterioration in the relationship between model inputs and outcomes.

Four controlled environments form a $2 \times 2$ experimental design:

| Scenario        | $P(X)$ | $P(Y \mid X)$ |
| --------------- | -------- | --------------- |
| Stable          | Baseline | Baseline        |
| Covariate Drift | Changed  | Baseline        |
| Concept Drift   | Baseline | Changed         |
| Combined Drift  | Changed  | Changed         |

A separate economic-shock experiment also changes both the unemployment distribution and the true sensitivity of default risk to unemployment.

### Key Experimental Results

| Scenario        | Max PSI | ROC AUC | Calibration Error | MAE vs. Synthetic True PD |
| --------------- | ------: | ------: | ----------------: | ------------------------: |
| Stable          |  0.0000 |  0.8383 |            0.0019 |                    0.0023 |
| Covariate Drift |  0.1204 |  0.8300 |            0.0043 |                    0.0029 |
| Concept Drift   |  0.0000 |  0.8316 |            0.0511 |                    0.0505 |
| Combined Drift  |  0.1204 |  0.8237 |            0.0673 |                    0.0665 |
| Economic Shock  | 10.0183 |  0.8241 |            0.0793 |                    0.0792 |

The controlled results illustrate two central findings:

* detectable input drift does not necessarily imply substantial model deterioration;
* substantial model deterioration can occur even when monitored input distributions remain unchanged.

In particular, the Concept Drift experiment uses exactly the same model-input observations as the Stable environment. Input-drift statistics are therefore zero, while calibration error and error relative to the known synthetic true probability increase materially.

The progressive-deterioration experiment further shows that probability accuracy can worsen gradually while input drift remains zero and ROC AUC remains relatively stable.

[View the model deterioration notebook](notebooks/02_model_deterioration.ipynb)

### Input Drift vs. Model Deterioration

![Input drift versus model deterioration](figures/drift_vs_model_deterioration.png)

### Progressive Concept Drift

![Progressive concept drift](figures/progressive_concept_drift_pd.png)

> **Note:** These experiments use synthetic controlled environments designed to isolate model-risk mechanisms. Scenario magnitudes, including the severe economic-shock PSI, are experimental stress settings and should not be interpreted as universal production monitoring thresholds.

## Motivation

Financial institutions increasingly rely on statistical and machine-learning models for credit risk, forecasting, fraud detection, customer analytics, and other decision-making processes.

These models are generally developed using historical relationships between predictors and outcomes. However, economic conditions, customer populations, market behavior, and relationships among variables can change.

As a result, a model that performed well when it was developed may remain operational while becoming progressively less reliable.

This project investigates methods for identifying these changes, measuring their effect on predictive models, diagnosing the causes of deterioration, and evaluating possible responses.

## Research Focus

The project will investigate several related forms of model instability, including:

- data distribution shift;
- prediction drift;
- model performance degradation;
- calibration deterioration;
- changes in relationships between predictors and outcomes;
- model sensitivity to changing economic regimes.

A central objective is to distinguish between **changes in data that are statistically observable** and **changes that materially affect model reliability**.

## Initial Research Questions

The project currently focuses on questions including:

1. How early can changes in data distributions indicate deterioration in financial predictive models?
2. Which types of distribution shift are most strongly associated with deterioration in predictive performance or calibration?
3. Can model-aware drift measures distinguish consequential model changes from benign population changes?
4. Can controlled stress scenarios identify conditions under which a previously validated model becomes unreliable?
5. How can multiple monitoring signals inform decisions to continue monitoring, investigate, recalibrate, retrain, or redevelop a model?

## Planned Project Components

The project is expected to include:

- public financial datasets;
- baseline predictive models;
- temporal model validation;
- drift-detection methods;
- model-performance monitoring;
- calibration monitoring;
- economic-regime comparisons;
- controlled stress experiments;
- diagnostic methods;
- reproducible Python implementations and notebooks.

## Current Status

The project has progressed from initial research design through baseline model development and controlled model-deterioration experiments.

Completed work currently includes:

* a reproducible synthetic credit-risk data-generating process;
* a frozen baseline logistic regression pipeline;
* held-out discrimination and calibration evaluation;
* comparison of model-predicted risk with known synthetic true risk;
* controlled Stable, Covariate Drift, Concept Drift, and Combined Drift environments;
* a \(2 \times 2\) experimental design separating changes in \(P(X)\) from changes in \(P(Y \mid X)\);
* PSI, KS, and Wasserstein input-drift monitoring;
* progressive concept-drift experiments across multiple monitoring periods;
* an economic regime-change stress experiment;
* reusable drift-detection utilities;
* reproducible figures and monitoring summaries.

The controlled experiments demonstrate that observable input drift and deterioration in model validity are related but distinct phenomena. In particular, the project shows both that substantial input drift can occur without substantial probability error and that material calibration deterioration can occur while monitored input distributions remain unchanged.

Current development will build on these controlled experiments toward broader monitoring and diagnostic methods for identifying when a previously valid model may require investigation, recalibration, retraining, or redevelopment.


## Documentation

Project documentation will be maintained in the [`docs`](docs/) directory.

## Data

Only public, appropriately licensed, or independently generated data will be used.

See [`data/README.md`](data/README.md) for data-management principles.

## Disclaimer

This is an independent research project and does not represent the views or practices of any current or former employer or other organization.

See [`DISCLAIMER.md`](DISCLAIMER.md) for the full disclaimer.

## License

This project is licensed under the Apache License 2.0.

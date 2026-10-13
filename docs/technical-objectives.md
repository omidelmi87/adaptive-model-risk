# Technical Objectives

The technical objectives of the Adaptive Model Risk project translate the research questions into measurable and reproducible analyses.

The project is designed as an evolving experimental framework. Some objectives have already been implemented in the current synthetic experiments, while others remain areas for future development.

## Objective 1 — Measure Data Distribution Shift

Implement and compare methods for detecting changes in model-input distributions over time.

The current framework includes:

* Population Stability Index;
* Kolmogorov-Smirnov statistics;
* Wasserstein distance;
* feature-level mean shifts;
* calendar-aware empirical normalization of drift statistics.

The project also evaluates how ordinary recurring variation, such as seasonality, affects raw drift measures so that expected changes are not automatically treated as abnormal deterioration.

Future extensions may include:

* Jensen-Shannon divergence;
* multivariate drift detection;
* classifier-based drift detection;
* dependence-aware drift measures.

## Objective 2 — Monitor Model Outputs and Performance

Develop methods for tracking whether model predictions remain reliable as the operating environment changes.

The current framework evaluates:

* predicted probabilities;
* observed outcome rates;
* prediction-versus-observed outcome gaps;
* calibration error;
* Brier score;
* ROC AUC;
* prediction error relative to known synthetic true probabilities.

The project distinguishes between metrics used directly for alert generation and metrics retained for diagnostic interpretation.

For example, ROC AUC and Brier score are currently treated as diagnostic measures rather than primary alert components.

## Objective 3 — Identify Changes in Predictor–Outcome Relationships

Investigate whether changes in the relationship between predictors and outcomes can be detected independently of changes in predictor distributions.

Controlled experiments currently include concept-deterioration scenarios in which:

* the distribution of model inputs remains unchanged;
* the frozen model produces the same predictions;
* the true relationship between predictors and outcomes changes;
* calibration and prediction reliability deteriorate.

These experiments provide a controlled setting for separating changes in `P(X)` from changes in `P(Y | X)`.

Future work may extend this analysis to additional forms of conditional-distribution change and additional model classes.

## Objective 4 — Develop Model-Aware Drift Measures

Investigate whether observed distribution changes can be weighted or interpreted according to their relevance to model behavior.

Potential approaches include:

* feature importance;
* model sensitivity;
* partial dependence;
* local or global explanations;
* interaction effects;
* changes in predictive contribution;
* deterioration concentrated in decision-relevant regions.

This objective remains an area for future development.

The current framework intentionally begins by separating input-distribution evidence from outcome-based evidence before introducing more model-specific drift measures.

## Objective 5 — Evaluate Models Across Economic Regimes

Evaluate model behavior under changing economic environments and identify conditions under which a previously validated model becomes unreliable.

The current synthetic framework includes an abrupt economic regime-shock experiment involving:

* a substantial increase in unemployment;
* a simultaneous change in the relationship between unemployment and default risk;
* sustained post-shock conditions.

This controlled experiment provides an initial regime-analysis capability.

Future work may extend this objective to:

* historical economic periods;
* recession and expansion regimes;
* interest-rate environments;
* inflation regimes;
* credit-market conditions;
* housing-market conditions;
* observed delinquency or default environments.

## Objective 6 — Conduct Controlled Stress Experiments

Create controlled changes in model-input distributions and predictor-outcome relationships in order to measure model sensitivity and deterioration.

The current framework includes:

* a stable seasonal environment;
* gradual covariate shift;
* gradual concept deterioration;
* gradual combined deterioration;
* an abrupt economic regime shock.

These experiments establish controlled links among:

`environmental change -> monitoring evidence -> model-reliability consequences`

Because the synthetic data-generating process is known, the experiments can distinguish true structural change from random sampling variation.

## Objective 7 — Develop Sequential Diagnostic Signals

Develop monitoring signals that identify not only whether abnormal evidence exists, but also what type of change may be occurring.

The current framework includes separate:

* input-monitoring signals;
* outcome-monitoring signals;
* exponentially weighted moving-average evidence;
* system-level monitoring scores;
* empirically calibrated alert thresholds;
* persistence rules for confirmed alerts.

Healthy-null simulations are used to estimate expected monitoring behavior under normal conditions.

The framework also measures:

* first confirmed alert period;
* detection delay;
* change magnitude at detection;
* input-channel detection;
* outcome-channel detection;
* false alerts;
* missed detections.

This structure allows monitored scenarios to be characterized as input-driven, outcome-driven, or supported by both forms of evidence.

Future work may investigate richer diagnostic classifications and uncertainty around these diagnoses.

## Objective 8 — Evaluate Potential Remediation Strategies

Evaluate possible responses after deterioration has been detected and diagnosed.

Potential responses include:

* continued monitoring;
* investigation;
* recalibration;
* threshold adjustment;
* partial retraining;
* full retraining;
* model redevelopment.

This objective remains future work.

The current project focuses first on building a defensible detection and diagnosis framework before evaluating intervention strategies.

Future experiments may examine whether the appropriate response depends on:

* the source of deterioration;
* severity;
* persistence;
* detection confidence;
* whether the change appears temporary or structural.

The project will evaluate these approaches empirically rather than prescribe institution-specific model-governance decisions.

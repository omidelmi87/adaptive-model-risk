# Research Questions

The Adaptive Model Risk project investigates how predictive models behave when the environment in which they operate changes and how monitoring evidence can distinguish expected variation from meaningful deterioration.

The research agenda is organized around five primary questions.

## RQ1 — Early Detection

**How early can monitoring evidence identify meaningful changes in a model's operating environment or reliability?**

This question examines the timing of different types of monitoring evidence.

Changes in model inputs may be observable immediately, while evidence of deterioration in the relationship between predictors and outcomes may not become available until realized outcomes are observed.

The project therefore considers:

* contemporaneous input-distribution evidence;
* delayed outcome-based evidence;
* the statistical latency required for persistent evidence to accumulate;
* the total delay between the onset of deterioration and a confirmed monitoring alert.

A key issue is whether meaningful deterioration can be identified early without assuming that abnormal input drift must always occur first.

## RQ2 — Consequential vs. Benign Change

**Which observed changes represent normal or benign variation, and which are materially associated with deterioration in model reliability?**

Not every statistically significant change in the model-input population creates meaningful model risk.

Conversely, deterioration in the relationship between predictors and outcomes may occur even when monitored input distributions remain comparatively stable.

This research question examines how monitoring can distinguish among:

* expected recurring variation such as seasonality;
* population or covariate shift;
* deterioration in predictor-outcome relationships;
* combined changes;
* abrupt regime changes.

The objective is to separate observable change in `P(X)` from evidence that `P(Y | X)` has changed in a way that affects model reliability.

## RQ3 — Model-Aware Monitoring

**Can monitoring methods that incorporate model sensitivity, feature importance, or model structure better identify consequential changes than distribution-based measures alone?**

Distribution-based monitoring measures treat changes in observed variables primarily as statistical changes in the input population.

However, equal-sized changes in different variables may have very different consequences for a predictive model.

This question explores whether monitoring can incorporate information such as:

* feature importance;
* local or global model sensitivity;
* variable interactions;
* model-specific response functions;
* changes concentrated in high-risk or decision-relevant regions.

This remains an area for future development beyond the current input- and outcome-channel monitoring framework.

## RQ4 — Regime and Stress Analysis

**Can controlled stress scenarios or historical economic regimes identify conditions under which a previously validated model becomes unreliable?**

The project uses controlled synthetic scenarios to isolate different forms of change and examine how a frozen model responds.

Current experiments include gradual population shift, gradual relationship deterioration, combined deterioration, and an abrupt economic regime shock.

Future work may extend this analysis to historical economic periods, alternative datasets, and additional stress configurations.

The objective is to identify not only whether model performance changes, but also which types of environmental change create the greatest risk to model reliability.

## RQ5 — Monitoring Evidence and Model Intervention

**How can multiple monitoring signals be combined to support model-management responses?**

The current framework combines input- and outcome-based monitoring evidence into a sequential alert system while preserving the diagnostic distinction between the two channels.

Potential model-management responses may include:

* continued monitoring;
* investigation;
* recalibration;
* threshold adjustment;
* partial retraining;
* full retraining;
* model redevelopment.

The current project focuses primarily on detection and diagnosis rather than automating these interventions.

Future work will investigate whether the type, severity, persistence, and timing of monitoring evidence can help determine which response is most appropriate.

The objective is not to automate institutional model-governance decisions, but to develop evidence that can support more informative diagnosis and decision-making.

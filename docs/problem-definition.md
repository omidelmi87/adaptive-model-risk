# Problem Definition

## Background

Predictive models used in financial decision-making are developed using historical observations of relationships among customer characteristics, economic variables, behavioral indicators, and future outcomes.

Model development and validation generally evaluate whether these relationships are sufficiently stable and predictive for the intended use of the model.

However, the environment in which a model operates can change after deployment.

Examples may include:

- changes in macroeconomic conditions;
- interest-rate changes;
- labor-market disruptions;
- shifts in borrower or customer populations;
- changes in consumer behavior;
- changes in product composition;
- structural changes in financial markets;
- unexpected economic shocks.

These changes may alter either the distribution of model inputs or the relationships between predictors and outcomes.

## Core Problem

A predictive model may remain technically operational even after the assumptions and relationships supporting its historical performance begin to weaken.

Traditional model-monitoring approaches often measure changes in model inputs, outputs, or performance independently.

However, not every observable distribution shift creates meaningful model risk.

At the same time, important deterioration may occur even when simple distribution-shift indicators remain relatively stable.

The central problem addressed by this project is therefore:

> **How can changes in the operating environment of a financial predictive model be detected, evaluated, and connected to changes in model reliability?**

## Distinguishing Statistical Change from Model-Relevant Change

Consider a model developed at time $t_0$.

The distribution of predictors may change over time:

$$
P_t(X) \neq P_{t_0}(X)
$$

This type of change may be observable through conventional drift metrics.

However, distribution change alone does not necessarily imply that the model has become unreliable.

A more consequential change may occur when the relationship between predictors and outcomes changes:

$$
P_t(Y \mid X) \neq P_{t_0}(Y \mid X)
$$


In such situations, relationships learned from historical observations may no longer accurately describe the environment in which the model is currently operating.

## Research Challenge

The project investigates monitoring approaches that move beyond simply detecting whether data have changed.

The broader challenge is to determine:

1. whether an observed change is unusual relative to normal operating variation;
2. whether the change reflects a shift in the model-input population, deterioration in the relationship between predictors and outcomes, or both;
3. whether predicted probabilities remain reliable after the environment changes;
4. how quickly meaningful deterioration can be identified when outcome labels are delayed;
5. how persistent monitoring evidence should be before an alert is treated as meaningful;
6. what type of model-management response may ultimately be appropriate.

A central part of this challenge is separating **observable input change** from **evidence that the model itself has become unreliable**.

The project therefore evaluates input-distribution evidence and outcome-based evidence separately before combining them within a sequential monitoring framework.

Normal recurring variation, such as calendar seasonality, must also be distinguished from abnormal change so that expected fluctuations do not generate unnecessary alerts.

## Intended Outcome

The intended outcome is an open and reproducible framework for studying, detecting, and diagnosing model deterioration under changing financial and economic conditions.

The framework is designed to support experiments involving:

* stable but seasonally changing environments;
* gradual shifts in model-input populations;
* gradual deterioration in predictor-outcome relationships;
* combined population and relationship changes;
* abrupt economic regime changes;
* delayed availability of realized outcomes;
* sequential accumulation of monitoring evidence;
* measurement of detection delay, missed detection, and false-alert behavior.

The framework is intended to help distinguish **what has changed**, **whether model reliability has changed**, and **which monitoring evidence supports that conclusion**.

It is intended to support research and model-risk analysis rather than replace institution-specific model validation, governance, or regulatory judgment.

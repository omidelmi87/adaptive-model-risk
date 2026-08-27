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

The project aims to investigate monitoring approaches that move beyond simply detecting whether data have changed.

The broader objective is to determine:

1. whether meaningful change has occurred;
2. whether the change affects model performance;
3. which variables or relationships are contributing to deterioration;
4. how severe the deterioration is;
5. what type of model-management response may be appropriate.

## Intended Outcome

The intended outcome is an open and reproducible framework for studying and diagnosing model degradation under changing financial and economic conditions.

The framework is intended to support research and model-risk analysis rather than replace institution-specific model validation, governance, or regulatory judgment.

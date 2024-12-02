# Intro

This repository contains implementation of Automated Market Maker (AMM) using Fixed Product (FPMM), inspired from Polymarket formula.

See this [page](https://help.polkamarkets.com/how-polkamarkets-works/automated-market-maker-(amm)) or this [one](https://help.polkamarkets.com/how-polkamarkets-works/trading-and-price-calculation) for more details on Polymarket formula.

### Main difference with Polymarket formula

Here, we have an implementation where we can create a market with inequality of the outcomes. This is not possible with Polymarket formula.

But you can check in this [script]() that this is equivalent to creating a market with equally weighted outcomes and then buying shares to the targeted outcome.

# Maths

## Fundamentals

Definitions:
- $s_i$ is the amount of shares $i$ in the pool
- $p_i$ is the price of share $i$
- $w_i$ is outcome price weight $i$
- $N$ is the number of outcomes
- $\text{liquidity}$ is the total liquidity in the pool

Here are the fundamentals of the AMM:
```math
\prod s_i = \text{liquidity}^N
```
```math
w_k = \sum_{i \neq k} s_i
```
```math
p_k = \frac{w_k}{\sum_{i \neq k} w_i}
```
```math
\sum p_i = 1
```

In practice, we will know the following data: $(p_i)$, $N$, and $\text{liquidity}$.

## Shares relation

Using the fundamentals, we can express the relationship between shares and prices:

```math
w_k = \sum_{i \neq k} s_i = \frac{\text{liquidity}^N}{s_k}
```

Then:
```math
\sum_{i \neq k} w_k = \sum_{i \neq k} \frac{\text{liquidity}^N}{s_i} = \text{liquidity}^N \cdot \sum_{i \neq k} \frac{1}{s_i}
```

From the price equation:
```math
p_k = \frac{w_k}{\sum_{i \neq k} w_i} = \frac{\frac{1}{s_k}}{\sum_{i \neq k} \frac{1}{s_i}}
```

Thus:
```math
s_k = \frac{1}{p_k} \cdot \frac{1}{\sum_{i \neq k} \frac{1}{s_i}}
```

### Iterative shares calculation

We consider that $s_1$ is known or at least arbitrarily fixed.

Start with $s_1$:
```math
s_1 = \frac{1}{p_1} \cdot \frac{1}{\sum_{i \neq 1} \frac{1}{s_i}}
```
Which implies:
```math
\sum_{i \neq 1} \frac{1}{s_i} = \frac{1}{p_1 \cdot s_1}
```

For $s_k$:
```math
s_k = \frac{1}{p_k} \cdot \frac{1}{\sum_{i \neq k} \frac{1}{s_i}}
```
Rearranging:
```math
\sum_{i \neq k} \frac{1}{s_i} = \frac{1}{p_k \cdot s_k}
```

Breaking down $\sum_{i \neq k} \frac{1}{s_i}$:
```math
\sum_{i \neq k} \frac{1}{s_i} = \sum_{i \neq 1} \frac{1}{s_i} + \frac{1}{s_1} - \frac{1}{s_k}
```
Substituting:
```math
\frac{1}{p_k \cdot s_k} = \frac{1}{p_1 \cdot s_1} + \frac{1}{s_1} - \frac{1}{s_k}
```

Simplify to compute $s_k$:
```math
\frac{1}{p_k \cdot s_k} + \frac{1}{s_k} = \frac{1}{p_1 \cdot s_1} + \frac{1}{s_1}
```
Factorize:
```math
\frac{1 + p_k}{p_k \cdot s_k} = \frac{1}{p_1 \cdot s_1} + \frac{1}{s_1}
```

Finally:
```math
s_k = \frac{1 + p_k}{p_k \cdot \left( \frac{1}{p_1 \cdot s_1} + \frac{1}{s_1} \right)}
```

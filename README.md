# Kaggle project: Best Frameglass Order

## Introduction

We have 2 types of paintings: landscape and portrait. Each frameglass is able to hold 1 landscape painting or 2 portrait paintings. Each painting has a set of tags. The goal is to find the best order of frameglasses to maximize Global Robotic Satisfaction score.

Global Robotic Satisfaction score is a sum of Local Robotic Satisfaction. Local Robotic Satisfaction is calculated as a minimum of these 3 values:

- The number of common tags between two neighboring frameglasses

- The number of tags in the first painting but not in the second painting

- The number of tags in the second painting but not in the first painting

## Approach

We have 2 problems here:

1. How to divide the paintings into groups of 1 landscape painting and 2 portrait paintings

2. How to order the paintings in each group to maximize the Global Robotic Satisfaction score

These 2 problems can't be solved independently. We need to solve them together. We can use dynamic programming to solve this problem.

To maximize the Global Robotic Satisfaction score, we need to maximize the Local Robotic Satisfaction score between each pair of neighboring paintings. We can use dynamic programming to calculate the Local Robotic Satisfaction score between each pair of neighboring frameglasses.

Also, to maximize LRS score, we have to use frameglasses that have a half of the same tags, because the LRS score is $n/2$ at the best where $n$ is $min(tags1, tags2)$. It also means that it is better to assemble frameglasses with the most different tags.

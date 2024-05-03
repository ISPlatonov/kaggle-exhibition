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

Globally,to maximize the Global Robotic Satisfaction score, we need to maximize the Local Robotic Satisfaction score between each pair of neighboring paintings. To do that, we need to maximize the number of tags for each frameglass.

Also, to maximize LRS score, we have to use frameglasses that have a half of the same tags, because the LRS score is $n/2$ at the best where $n$ is $min(tags1, tags2)$. It also means that it is better to assemble frameglasses with the most different tags.

### 1. (L | P) -> Frameglass

For landscape paintings, we can use them as they are. For portrait paintings, we need to maximize the number of tags for each frameglass. To do that, we can use the following approach:

- Sort the portrait paintings by the number of tags in descending order

- Traverse the list of portrait paintings and group them with the most different and numerous tags (greedy approach, check on union of tags)

To speed up the process, we can break traversing each time we find already have a frameglass with number of tags more than half of the tags of the current painting.

### 2. Order the frameglasses, $GRS -> max$

To maximize the Global Robotic Satisfaction score, we need to maximize the Local Robotic Satisfaction score between each pair of neighboring paintings. To do that, we need to sort the frameglasses in such a way that the number of common tags between each pair of neighboring frameglasses is maximized.

To better understand the problem, we can represent it as a Euler Rounds: $\overline{A \cap B}$. The best situation is when the number of tags in the intersection of two neighboring frameglasses is a half of the number of tags in each frameglass. It means that we have a formula for the Local Robotic Satisfaction score: $LRS = min(min(tags1, tags2) - A \cap B, A \cap B)$.

To maximize the LRS score, we need to maximize LRS for each pair of neighboring frameglasses. To do that, we can use the following approach:

- Sort the frameglasses by the number of tags in descending order

- Traverse the list of frameglasses and group them in such a way that LRS is maximized

To speed up the process, we can break traversing each time number of tags in frameglass is less than two times the number of tags in the local maximum of LRS.

## Conclusion

The problem can be solved by using a greedy approach. We need to maximize the number of tags for each frameglass and maximize the Local Robotic Satisfaction score between each pair of neighboring paintings. To speed up the process, we can break traversing each time new iteration does not improve the result.

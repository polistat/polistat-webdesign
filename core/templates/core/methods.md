# Overview

The ORACLE (Overall Results of an Analytical Consideration of the Looming Elections) of Blair is a senior class project at Montgomery Blair High School under the supervision of Mr. David Stein. We created this election model during the fall semester to predict the upcoming 2020 Presidential Election. This is the third iteration of election modeling at Blair; the Oracle successfully forecasted the 2018 Congressional Elections, and we also created a model for the 2016 battleground states. Our forecast is probabilistic, meaning we *favor* a candidate’s win based on the number of times that candidate wins in our simulations. All decisions in creating this model were made by students in the class. We take full responsibility for the methods used in the model, as well as the predictions made by the model. 
​

All calculations are based on the two-party vote (Democratic and Republican parties), so any votes for a third-party or independent candidate do not count toward our model. **Positive** margins favor Republican incumbent Donald Trump, while **negative** margins favor Democratic challenger Joe Biden. 
​

Furthermore, since Maine and Nebraska uniquely distribute their electoral votes by congressional district, Maine CD-2 and Nebraska CD-2 were considered “states” since they tend to vote less consistently with the state as a whole. Therefore, our model has 53 “states”: the fifty states, the District of Columbia, Maine CD-2, and Nebraska CD-2.
​

Our model uses four factors to arrive at its predictions: Priors, Polls, Correlation, and Simulation. In **Priors**, we combined a partisan lean index, which we have termed Blair Partisan Index (BPI), and predictive demographics for each state. With **Polls**, we averaged polls through a novel z-test method and determined variance using sampling variation, days before the election, and voting difficulty in each state. With **Correlation**, our model then correlated each state through the Oracle State Correlations and Relationships (OSCAR) method. During **Simulation**, we combined the various components and simulated the election one million times, picking random starting points for each state, and seeing how each state affects the other using OSCAR. 
​

# Priors

## Blair Partisan Index (BPI)

Understanding how Democratic or Republican each state has voted historically helps us predict how they’ll vote in the future. We found the Republican two-party vote percentage for each state in five previous elections: the 2008, 2012, and 2016 Presidential elections, and the 2014 and 2018 US House elections. For each election, we found the difference between the national two-party percentage and the state two-party percentage (i.e. how partisan the state was compared to the nation as a whole). We took a weighted average of these differences based on how representative we thought each election was using the following equation:
​

> BPI = 0.5 &times; (2016 presidential difference) + 0.2 &times; (2012 presidential difference) + 0.2 &times; (2018 midterm difference) + 0.05 &times; (2014 midterm difference) + 0.05 &times; (2008 presidential difference)
​

This weighted average is our Blair Partisan Index (BPI), representing the bias toward Republicans in that state compared to their national standing. For example, if a state has a +5 BPI, then (disregarding polls, demographics, etc.) Republicans historically outperformed their national total by around 5% and Democrats underperformed their national total vote by around 5%. The resulting margin is actually double the BPI (e.g. if one candidate gets 5% more than the national average and the other gets 5% less, the margin between them is 10%).
​

## Demographics
Understanding how different demographics have voted in the past also helps us predict how they’ll vote in the future. We decided on the four most informative demographics:
​

1. the percentage of non-Hispanic white residents

2. the percentage of nonreligious residents

3. the urbanicity of the state[^1]

4. the percentage of residents that have a college degree[^2]

​
We took a linear regression between these statistics and the results of the 2016 Presidential Election and predicted the vote percentage of each state with the following equation:
​

> Expected Trump Percentage Vote = 2.72 &times; (White Non-Hispanic) - 4.320 &times; (Non-Religious) - 4.47 &times; (College Degree) - 3.69 &times; (Urbanicity) + 48.261
​

For each state, we obtained demographic data from the 2010 Census and plugged that into the equation. The resulting expected Trump vote is what we call the "demographic prior".
​

## Combining BPI and Demographics
To find the overall prior prediction, we combine the BPI and demographic analyses by taking a simple average of the two. For example, if the national vote percentage was 50% for Trump, and a state has a BPI of +5% and a demographic prior of 51%, then the overall prior prediction would be 53%.
​

# Polls
## Averaging Polls: Z-Test Method
We introduced a new method for averaging polls, which accounts for how volatile each state’s population is, dubbed the “z-test method”. For each day we ran the model, we gathered polls for each state from FiveThirtyEight starting from Aug. 12 and divided the polls into ten-day blocks. We divided these blocks by counting backwards in ten-day steps from the current day until all polls in that state were encompassed by a block. For example, if we ran the model on Sept. 10 for a state with its earliest poll on Aug. 15, there would be three blocks of ten days: Sept. 10 to Sept. 1, Aug. 31 to Aug. 22, Aug. 21 to Aug. 12. 
​

Based on the number of polls in a block, we calculated the mean in three different ways:

1. If the block had only one poll, the mean of the block would be the result of that poll.

2. If the block had more than one poll, we conducted a meta-analysis[^3] on the polls to determine the mean.

3. If the block had no polls, all the polls in the past two blocks were considered to be a single block.
​

Rather than using the margin of error provided by the pollster, we calculated the variance for each poll by combining the sampling variation with the percentage of voters who indicated they weren’t affiliated with either candidate:
​
$$varianceCombined = \frac{pq}{n} + (\frac{1}{30} * (1 - (\%Trump + \%Biden)))^2$$

Using the mean and combined variance for each block, starting with the earliest block, we conducted z-tests between consecutive blocks, with a significance level of \\(\alpha = 0.05\\). A significant difference between two consecutive blocks indicates a significant shift in the voting intentions of the population, in which case polls from previous blocks would be discarded from the model. Otherwise, the two consecutive blocks would be combined. Therefore, the final block used for prediction would include all polls after the last significant population shift.
​

For example, if block one (Aug. 21 to Aug. 12; with three polls) and block two (Aug. 31 to Aug 22; with five polls) were not significantly different according to our z-test, then all the polls from both blocks would be combined, with eight polls now in block two. Then, if block two and block three were significantly different, then we would not consider any of the polls in block two and only use block three.
​

By the end of this process, we’ll have one final block to use for prediction, for which we calculate the mean and variance using the methods described above.
​

## Additional Variance
Once we determine the mean and variance for each state based on polls alone, we add more variance based on how easy it is to vote in that state and how close our predictions are to election day. We do this by adding a multiple of the Cost of Voting Index[^4] to each of the states as well as a multiple of the amount of days until election day, using the following equations:
​

$$\frac{0.6(CoVI +2.06)}{400}$$

$$\frac{1}{1600} \sqrt{\frac{electionDate-currentDate}{7}}$$ 
​

## Combining Polls with BPI (Finding State Lean)
We combined the means from the priors and the means from the polls using a weighted average. Depending on how many polls were used in the final block of the z-test method, the weight for the mean of the polls in each state was calculated using the following equation:

$$\frac{1.92}{\pi}\arctan{(0.65 \times numPolls)}$$
​
The weight for the mean of the priors would be the complement[^5] of this equation. We will call this weighted average the state’s lean.
​

# Correlation
## Oracle State Correlations and Relationships (OSCAR) 
Since we expect demographically similar states to vote similarly, it’s important to consider how they might influence one another in their state elections. For example, if one state were to lean heavily toward Trump, we would need to take that into account and shift all other states that are correlated with it accordingly. 
​

We decided on seven informative demographics: 

1. the percentage of non-hispanic white residents

2. the percentage of black residents

3. the percentage of hispanic residents

4. the percentage of nonreligious residents

5. the urbanicity of the state

6. the median age of the state

7. the percentage of residents that have a college degree
​

For each state, we ran a regression against all other states with the seven demographics as predictors and stored the outputs in a square matrix, the Oracle State Correlations and Relationships (OSCAR).
​

## Correlation Scheme
Our Correlation Scheme, which is used during simulations, calculates a net effect posed by each state onto every other state based on their demographic similarity. Given demographically similar state A and state B, if we predict a Trump win by 2% more than the state lean in state A, then we can expect a similar win for state B. Given state C, which is nothing like state A, we can expect very little impact on state C from state A.
​

Each time we run our model, we choose a random number for each state according to the normal distribution of that state’s lean. We then take the difference of those random numbers from the state’s leanings, and take the dot product of those differences with OSCAR. Then, we divide that product by the sum of that state’s row in OSCAR. This value is the net effect of other states, which we add to the random number.
​

For example, consider states A, B and C, with the following hypotheticals:
​

State A:

- Predicted 2% more than its lean

- Correlated 0.8 with state B

- Correlated 0.1 with state C

​
State B:

- Predicted -3% more than its lean

- Correlated 0.8 with state A

- Correlated 0.5 with state C

​
State C:

- Predicted 4% more than its lean

- Correlated 0.1 with state A

- Correlated 0.5 with state B

​
The net effect of these states on each other would be:
​

> For State A: (-0.03 &times; 0.8 - 0.04 &times; 0.1)/(0.8 + 0.1)

> For State B: (0.02 &times; 0.8 + 0.04 &times; 0.5)/(0.8 + 0.5)

> For State C: (0.02 &times; 0.1 - 0.03 &times; 0.5)/(0.1 + 0.5)
​

The correlation scheme for the entire model would be similar, using 53 states instead of only three states.
​

# Simulation
## Putting it all together 
In order to calculate how likely a candidate is to win the national election, we need to simulate how well each candidate will do in each state. After we find each state’s lean and combined variance, we create a normal distribution for each state, centered at the state’s lean and standard deviation[^6]. Each time we run our model, a random number is chosen for each state according to their normal distribution. Depending on how much greater that random number is than the state’s lean, a net effect is applied onto each state based on the Correlation Scheme.
​

Once the net effect is added to the state’s random number, a candidate will win that state’s electoral votes based on who the state is in favor of. After all the electoral votes are tallied up, the candidate with 270 or more electoral votes will have won that one simulation.
​

Each run of the model simulates the election one million times. The results for each state and for the whole country are recorded and displayed in the national predictions as well as the individual state forecasts.
​

[^1]: Urbanicity is defined as the logarithm of the population living within 5 miles of a large city; obtained from [The Economist.](https://github.com/TheEconomist/us-potus-model/blob/master/data/urbanicity_index.csv)
[^2]: Defined as having a Bachelor's Degree or higher.
[^3]: A statistical procedure that combines the results of multiple independent studies, using the **metafor** package in R
[^4]: Obtained from [Election Law Journal: Rules, Politics, and Policy.](https://www.liebertpub.com/doi/full/10.1089/elj.2017.0478)
[^5]: As in \\(1 - \frac{1.92}{\pi} \cdot \arctan{(0.65 \cdot numPolls)}\\)
[^6]: Defined as the square root of the combined variance.

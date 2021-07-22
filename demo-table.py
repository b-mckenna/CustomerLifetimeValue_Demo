## Customer Analytics: Lifetime Value


#
# With a dataset of customer transactions, you can predict (i) the probability that a customer with a given transaction history is still “alive”, and (ii)
# the expected number of future transactions for a randomly-chosen customer, conditional on their transaction history

## Concrete Examples
# * Predicting how often a visitor will return to your website. (Alive = visiting. Die = decided the website wasn’t for them)
# * Understanding how frequently a patient may return to a hospital. (Alive = visiting. Die = maybe the patient moved to a new city, or became deceased.)
# * Predicting individuals who have churned from an app using only their usage history. (Alive = logins. Die = removed the app)
# * Predicting repeat purchases from a customer. (Alive = actively purchasing. Die = became disinterested with your product)
# * Predicting the lifetime values of your customers


from lifetimes.datasets import load_cdnow_summary
data = load_cdnow_summary(index_col=[0])

print(data.head())

## The shape of your data
# For all models, the following nomenclature is used:
# * **_frequency_** represents the number of repeat purchases the customer has made. This means that it’s one less than the total number of purchases. This is actually slightly wrong. It’s the count of time periods the customer had a purchase in. So if using days as units, then it’s the count of days the customer had a purchase on.
# * **_T_** represents the age of the customer in whatever time units chosen (weekly, in the above dataset). This is equal to the duration between a customer’s first purchase and the end of the period under study.
# * **_recency_** represents the age of the customer when they made their most recent purchases. This is equal to the duration between a customer’s first purchase and their latest purchase. (Thus if they have made only 1 purchase, the recency is 0.)


## Basic Frequency/Recency analysis using the BG/NBD model
# We’ll use the BG/NBD model first. There are other models which we will explore in these docs, but this is the simplest to start with.

from lifetimes import BetaGeoFitter

# similar API to scikit-learn and lifelines.
bgf = BetaGeoFitter(penalizer_coef=0.0)
bgf.fit(data['frequency'], data['recency'], data['T'])
print(bgf)

# After fitting, we have lots of nice methods and properties attached to the fitter object.
# For small samples sizes, the parameters can get implausibly large, so by adding an l2 penalty the likelihood, we can control how large these parameters can be. This is implemented as setting as positive penalizer_coef in the initialization of the model. In typical applications, penalizers on the order of 0.001 to 0.1 are effective.


## Visualizing our Frequency/Recency Matrix
# Consider: a customer bought from you every day for three weeks straight, and we haven’t heard from them in months. What are the chances they are still “alive”? Pretty small. On the other hand, a customer who historically buys from you once a quarter, and bought last quarter, is likely still alive. We can visualize this relationship using the Frequency/Recency matrix, which computes the expected number of transactions a artificial customer is to make in the next time period, given his or her recency (age at last purchase) and frequency (the number of repeat transactions he or she has made).

from lifetimes.plotting import plot_frequency_recency_matrix

plot_frequency_recency_matrix(bgf)


# We can see that if a customer has bought 25 times from you, and their latest purchase was when they were 35 weeks old (given the individual is 35 weeks old), then they are your best customer (bottom-right). Your coldest customers are those that are in the top-right corner: they bought a lot quickly, and we haven’t seen them in weeks.
# There’s also that beautiful “tail” around (5,25). That represents the customer who buys infrequently, but we’ve seen him or her recently, so they might buy again - we’re not sure if they are dead or just between purchases.
# Another interesting matrix to look at is the probability of still being alive:

from lifetimes.plotting import plot_probability_alive_matrix

plot_probability_alive_matrix(bgf)

## Ranking customers from best to worst
# Let’s return to our customers and rank them from “highest expected purchases in the next period” to lowest. Models expose a method that will predict a customer’s expected purchases in the next period using their history.

t = 1
data['predicted_purchases'] = bgf.conditional_expected_number_of_purchases_up_to_time(t, data['frequency'], data['recency'], data['T'])
data.sort_values(by='predicted_purchases').tail(5)

# Great, we can see that the customer who has made 26 purchases, and bought very recently from us, is probably going to buy again in the next period.

## Assessing model fit
# Ok, we can predict and we can visualize our customers’ behaviour, but is our model correct? There are a few ways to assess the model’s correctness. The first is to compare your data versus artificial data simulated with your fitted model’s parameters.

from lifetimes.plotting import plot_period_transactions
plot_period_transactions(bgf)


# We can see that our actual data and our simulated data line up well. This proves that our model doesn’t suck.

## Example using transactional datasets
# Most often, the dataset you have at hand will be at the transaction level. Lifetimes has some utility functions to transform that transactional data (one row per purchase) into summary data (a frequency, recency and age dataset). 

from lifetimes.datasets import load_transaction_data_from_table
from lifetimes.utils import summary_data_from_transaction_data

transaction_data = load_transaction_data_from_table().toPandas()
print(type(transaction_data))
print(transaction_data.head())


summary = summary_data_from_transaction_data(transaction_data, 'id', 'date', observation_period_end='2018-12-31')
print(summary.head())


bgf.fit(summary['frequency'], summary['recency'], summary['T'])

## More model fitting
# With transactional data, we can partition the dataset into a calibration period dataset and a holdout dataset. This is important as we want to test how our model performs on data not yet seen (think cross-validation in standard machine learning literature). Lifetimes has a function to partition our dataset like this:

from lifetimes.utils import calibration_and_holdout_data

summary_cal_holdout = calibration_and_holdout_data(transaction_data, 'id', 'date',
                                        calibration_period_end='2014-06-01',
                                        observation_period_end='2014-12-31' )   
print(summary_cal_holdout.head())


# With this dataset, we can perform fitting on the _cal columns, and test on the _holdout columns:


from lifetimes.plotting import plot_calibration_purchases_vs_holdout_purchases

bgf.fit(summary_cal_holdout['frequency_cal'], summary_cal_holdout['recency_cal'], summary_cal_holdout['T_cal'])
plot_calibration_purchases_vs_holdout_purchases(bgf, summary_cal_holdout)

## Customer Predictions
# Based on customer history, we can predict what an individuals future purchases might look like:

t = 10 #predict purchases in 10 periods
individual = summary.iloc[20]

# The below function is an alias to `bfg.conditional_expected_number_of_purchases_up_to_time`
bgf.predict(t, individual['frequency'], individual['recency'], individual['T'])


## Customer Probability Histories
# Given a customer transaction history, we can calculate their historical probability of being alive, according to our trained model. For example:
from lifetimes.plotting import plot_history_alive

id = 35
days_since_birth = 200
sp_trans = transaction_data.loc[transaction_data['id'] == id]
plot_history_alive(bgf, days_since_birth, sp_trans, 'date')


## Fit model 

from lifetimes import BetaGeoFitter
from lifetimes.datasets import load_cdnow_summary

data = load_cdnow_summary(index_col=[0])
bgf = BetaGeoFitter()
bgf.fit(data['frequency'], data['recency'], data['T'])
bgf

## Save model

bgf.save_model('bgf.pkl')


#Your model has been saved and is ready to deploy. Go to **Models** and select the **predict** function from the **predictCLV.py** script.
### Introduction

This demo is based on the Lifetimes library. See the [official documentation](http://lifetimes.readthedocs.io/en/latest/) for more information. 

Lifetimes can be used to analyze your users based on a few assumption:

1. Users interact with you when they are "alive".
2. Users under study may "die" after some period of time.

I've quoted "alive" and "die" as these are the most abstract terms: feel free to use your own definition of "alive" and "die" (they are used similarly to "birth" and "death" in survival analysis). Whenever we have individuals repeating occurrences, we can use Lifetimes to help understand user behaviour.

### Applications

If this is too abstract, consider these applications:

 - Predicting how often a visitor will return to your website. (Alive = visiting. Die = decided the website wasn't for them)
 - Understanding how frequently a patient may return to a hospital. (Alive = visiting. Die = maybe the patient moved to a new city, or became deceased.)
 - Predicting individuals who have churned from an app using only their usage history. (Alive = logins. Die = removed the app)
 - Predicting repeat purchases from a customer. (Alive = actively purchasing. Die = became disinterested with your product)
 - Predicting the lifetime values of your customers

### Specific Application: Customer Lifetime Value
As emphasized by P. Fader and B. Hardie, understanding and acting on customer lifetime value (CLV) is the most important part of your business's sales efforts. [And (apparently) everyone is doing it wrong](https://www.youtube.com/watch?v=guj2gVEEx4s). *Lifetimes* is a Python library to calculate CLV for you.


## BYOD (Bring my Own Data)

**CSV**

In the **/lifetimes** directory, edit MYDATA.txt with the full path and filename to the dataset you want to use. It _must_ be a .csv with two columns id and date. 
For example, format a dataset like (2018-08-08 12:40:10,0) and write it to HDFS. Then add the path (/user/joe/retail_dataset.csv) to MYDATA.txt. 

**Impala/Hive Table**

In the **/lifetimes** directory, edit MYTABLE.txt with the full path and filename to the dataset you want to use. It _must_ be a two column table with id and date. 
For example, format a dataset like (2018-08-08 12:40:10,0) and write it to HDFS. Then add the path (/user/hive/warehouse/my_table) to MYDATA.txt. 


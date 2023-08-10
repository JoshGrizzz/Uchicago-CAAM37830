# Section 1: Introduction of SIR model and used notation
SIR model is a classical model to predict the number of infected people by utilizing three major different states of a person:
1. Susceptible: the individual who has not caught the disease but they can be infected. Actaully they are the only source in this model to 
get infected.
2. Infectious: an individual has already been caught the disease and can spread the disease to susceptible individuals. They are the only source to spread the disease.
3. Removed: the people who were previously infectious but now either can't be infected or infect others.

We use the recommened model parameters b and k listed in the SIR.md in our script to simulate, where b represents the number of interactions each day that could spread the disease (per individual) and k represents the fraction of the infectious population which recovers each day. We will introduce the specific notations we used for simulation in part 3.

Note that to make the results easier to interpret, in the continuous model we divide the group of removed into two groups of recovered and dead.

# Section 2: Description of package *SIR*
## Description for the class "Person"
First of all we constructed a class "Person" where we can update states of the person for the agent-based model. Besides the given states: S, I and R, we also consider the conditions which induce great effect on the infection trend that happen in our real life: whether people wear masks and whether people follow the advice to be quarantined. To initiate the class, we set self.susceptible be true and other attributes to be false since except for the given number of infected people, people are set default to be susceptible. Then we define some functions to represent transitions such as got_infected and got_removed by changing states of the booleans. We also include a transition_to_removed function to take the authorized 14 - days quarantine period into consideration.
## Decription of the file ODE_SIR.py
We first set up some parameters, such as p, q, r, k, d, b to represent mask effectiveness; proportion of people who wear masks; quarantine level; recover fraction; death fraction and number of contacts of an infected individual respectively.
Then we set up a vector consisting of 4 elements and get their derivatives respectively. Then we put them into the lambda function and get the right side of the differential equation. Finally we set up the function to solve the equation using "solve_ivp". We also set up events such that the susceptible people amount to be nearly 0.
## Description of the functions used in simulation
We also write some methods to faciliate the simulation. "count_infected" is used for counting infected people by summing the is_infected in class. When we add is_removed to is_infected we get "count_total", which is the idea for "count_total". Exactly the same idea for "count_removed" and "count_susceptible". We also wrote a method "run_simulation" to show how the total percentage of the population infected at some point in the simulation depend on k, b and T given b_quarantined(will introduce in part 3) = 5, N(population size) = 5000 and n(innitial infected size) = 5.

# Section 3: Preliminary investigations 
## Using agent-based models
### Preparation
 1.We draw a population size at N = 5000; set the probability that a close contact is infected as p = 0.037; set the probability of not being infected through wearing masks as 0.6 and set the probability a person is quarantined after being infected be 0.5.
 2. We then constructed two sets for the two most important parameters of this model. We set the possible values for k to be [0.01, 0.05, 0.1]. For parameter b, we consider two situations since conditions are quite different in these two situaions. The one is the number of interactions each day that could spread the disease per infectious individual if not quaratined; the other is the number of interactions each day that could spread the disease per infectious individual if quaratined. We choose the possible values for b when people are not quarantined to be 30, 45 and 60, and we set b to be 5 when the individual is quarantined.
Then we begin to simulate SIR over time(T = 80 days) respectively:
### Simulation
#### k = 0.01, b = 30:
<div style="text-align: center;">

![k = 0.01, b = 30](https://github.com/caam37830/project-group-3/blob/main/pictures/agent-based/T%3D80%20b_exposed%3D30%2C45%2C60/0.01%2C%2030.png#pic_center)
</div>

#### k = 0.01, b = 45:
![k = 0.01, b = 30](https://github.com/caam37830/project-group-3/blob/main/pictures/agent-based/T%3D80%20b_exposed%3D30%2C45%2C60/0.01%2C%2045.png#pic_center)

#### k = 0.01, b = 60:
![k = 0.01, b = 30](https://github.com/caam37830/project-group-3/blob/main/pictures/agent-based/T%3D80%20b_exposed%3D30%2C45%2C60/0.01%2C%2060.png#pic_center)

#### k = 0.05, b = 30:
![k = 0.05, b = 60](https://github.com/caam37830/project-group-3/blob/main/pictures/agent-based/T%3D80%20b_exposed%3D30%2C45%2C60/0.05%2C%2030.png#pic_center)

#### k = 0.05, b = 45:
![k = 0.05, b = 45](https://github.com/caam37830/project-group-3/blob/main/pictures/agent-based/T%3D80%20b_exposed%3D30%2C45%2C60/0.05%2C%2045.png#pic_center)


#### k = 0.05, b = 60:
![k = 0.05, b = 60](https://github.com/caam37830/project-group-3/blob/main/pictures/agent-based/T%3D80%20b_exposed%3D30%2C45%2C60/0.05%2C%2060.png#pic_center)


#### k = 0.1, b = 30:
![k = 0.1, b = 30](https://github.com/caam37830/project-group-3/blob/main/pictures/agent-based/T%3D80%20b_exposed%3D30%2C45%2C60/0.1%2C%2030.png#pic_center)


#### k = 0.1, b = 45:
![k = 0.1, b = 45](https://github.com/caam37830/project-group-3/blob/main/pictures/agent-based/T%3D80%20b_exposed%3D30%2C45%2C60/0.1%2C%2045.png#pic_center)


#### k = 0.1, b = 60:
![k = 0.1, b = 60](https://github.com/caam37830/project-group-3/blob/main/pictures/agent-based/T%3D80%20b_exposed%3D30%2C45%2C60/0.1%2C%2060.png#pic_center#pic_center)

### To get a more comprehensive and dynamic overview of the effect of changing k and b, we also plot the total percentage of the population infected at T = 20 and T = 30.
#### Different combinations of k and b at T = 20:
![T = 20](https://github.com/caam37830/project-group-3/blob/main/pictures/agent-based/Phase%20Diagram/T%3D20.png#pic_center)

#### Different combinations of k and b at T =  30:
![T = 30](https://github.com/caam37830/project-group-3/blob/main/pictures/agent-based/Phase%20Diagram/T%3D30.png#pic_center)

### Analysis
#### In terms of choice of k through T = 80 days
By choosing different k values we find that the larger k, which means the larger portion of infected people will be recovered, the smaller of the maximum value of the infected people. Also, when we set k = 0.1, there is no cross point bewteen susceptible line and infected line, which means as long as we take action to hospitalize infected people quick enough and hold other variables the same, it's possible the infected amount will never exceed the susceptible amount; however, the date for the maximum value of infected people to come doesn't not change much along the variation of k values. 

#### In terms of choice of b through T = 80 days 
By choosing different b values we find that the larger b, which means the larger the number of interactions each day that could spread the disease, the earlier the day for the maximum of infected people happens comes. This dependent varibale doesn't change apparently when we alter the values of k, which we mentioned above. Also, it takes shorter time for each amount to be stable.

#### Common effects for both changes
From both logic and the observation of simulations, we know the larger k has similar effect as the smaller b, which are both beneficial to mitigate the disease disperse. So it's reasonable to observe that there are several common effects result from enlarging k and reducing b. Such as the maximum value of infected people will reduce, the speed of increment of removed people and decrease of susceptible & infected people will reduce. It may be confusing why the speed of increasing of removed line happens when the direction goes toward good. It's because the number of infected and removed are somewhat progress behind the suscetible amount. We can see that in each graph the turning point of number of susceptible people happens earlier than the counterparts of other two lines. Since susceptible people are the "source" of infected people, which means susceptible people can become infected people, but infected people cannot turn to susceptible people again.    



## Using continuous models
 
### Simulation
1. Without mask or quarantine:
![](https://github.com/caam37830/project-group-3/blob/main/pictures/ode_based/SIR_plain.png)

2. Without mask or quarantine showing the event:
![](https://github.com/caam37830/project-group-3/blob/main/pictures/ode_based/SIR_Plain_Event.png)

3. With mask and without quarantine:
![](https://github.com/caam37830/project-group-3/blob/main/pictures/ode_based/SIR_mask.png)

4. With mask and without quarantine showing the event:
![](https://github.com/caam37830/project-group-3/blob/main/pictures/ode_based/SIR_mask_event.png)

5. With mask and quarantine:
![](https://github.com/caam37830/project-group-3/blob/main/pictures/ode_based/SIR_mq.png)

6. With mask and quarantine showing the event:
![](https://github.com/caam37830/project-group-3/blob/main/pictures/ode_based/SIR_mq_event.png)

7. With lockdown(quarantine level at 0.95) and mandatory masks in 150 days:
![](https://github.com/caam37830/project-group-3/blob/main/pictures/ode_based/SIR_hp_150.png)

8. With lockdown(quarantine level at 0.95) and mandatory masks in 300 days:
![](https://github.com/caam37830/project-group-3/blob/main/pictures/ode_based/SIR_hp_300.png)

### Analysis
#### Comparison between plain model and the model with mask only:
From their corresponding graphs with events, we can see that it only takes about 5 or 6 days for the susceptible people to be nearly 0 if people neither wear masks nor be in quarantine, but takes about 16 days for the susceptible people to be nearly 0 if 76% people wear masks but not put the infected people in quarantine.

#### Comparison between plain model and the model with both mask and quarantine:
From the corresponding graphs with events, we can see that it takes about 40 days for the susceptible people to be nearly 0 if 76% people wear masks and quarantine let the infected people contact approximately 50% less people. Since it only takes about 16 days for the susceptible people to be nearly 0 if 76% people wear masks but not set the infected people in quarantine, we may draw a conclusion that quarantine for infected people is an effective approach to flatten the curve.

#### Comparison bewteen the model with moderate mask & quarantine ratio and the model with high mask & quarantine ratio:
Set t = 150 days and t = 300 days, we find it takes more than 150 days to get the susceptible and the removed & recovered crossed. Moreover, we find it is possible that it even takes more than 300 days for the susceptible amount to be stable. This progress is much prominant than the counterpart when we compare the plain model and the model with only masks, so maybe enhance the ratio of the current solutions to the disease is more effective than begining a new solution.


# Section 4
## Variation_1 The strength of enforcement of quarantine
#### Point_1:
I want to answer the question that how strength of quarantine will influence the effect of quarantine. I will get the conclusion by setting different values for prob_quarantined in simulation.
#### Point_2:
By setting different values for prob_quarantined in simulation there will be more loops based on the number of new values we want to include in our simulatiom.
#### Point_3: 
We don't use data for this variation.
#### Point_4:
This idea is drawn from our real life.

## Variation_2 The number of interactions each day and the infectivity of diseases
#### Point_1: 
I want to know how the randomness of interactions and the infectivity of the disease will affect the results. In the current model, we assumed that the number of interactions each day that could spread the disease is fixed. But it is not that reasonable according to our real life.
The process of spreading the disease to another one should have two steps: 1.intimate contact; 2.spread disease to him/her. Neither step can be represented with fixed number. So I want to set these 2 steps with randomness and probability respectively.
#### Point_2: 
In the first step, instead of a fixed number of interactions, we'll take an upper bound of interactions per individual per day. For instance, the upper bound of interacions per individual per day is 70, then we'll take a random number less than 70 as the number of intimate contacts.
In the step 2, we will need one more parameter, denoting the probabilty that one get infected under intimate contact with an infectious. It corresponds to the infectivity of a specific disease. 
#### Point_3: 
We don't use data for this variation.
#### Point_4:
This idea is drawn from our real life.

## Variation_3 A more robust and complete model: "SEIR" model with consideration of environmental factors, where E refers to exposure to the virus, through both "natural" contact to the virus and contact to the infected.
#### Point_1: 
The continuous model provides us some really useful information, but it does not consider exposure to the virus. Considering exposure, the model might have some really different features since those people who are exposed to the virus but not get infected may also spread the virus.
#### Point_2:
We may pull ourselves out from the "naive" set-ups with a samll group of people. Rather, we may consider a larger populaton. Also, after we get the data from our simulations, we may perform some inferences on the results, for example, perform some regression models on it. Additionally, we might compare our models to some previous records to testify our results.
#### Point_3:
We might use recorded data for this variation.
#### Point_4:
This idea is drawn from several documentations and papers that analyze Covid-19.

## References

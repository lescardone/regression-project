# Linear Regression and Webscraping Project: Predicting Loose Diamond Prices

## Question/Need:
*What is the framing question of your analysis, or the purpose of the model/system you plan to build?*
- How accurately can we predict the price of a diamond based on its given features (carot, cut, color, clarity, etc)?
- Does 'seller' affect the models' performance?
  - Ideally I'd like to build two models, one for a major retailer and one for a diamond wholesale site.

*Who benefits from exploring this question or building this model/system?*
- Individuals who want to understand which qualities have the most effect on diamond price
- Individuals looking to purchase diamonds for jewlery
- A diamond retailer who wants to have competetive pricing or build a tool for their website for users


## Data Description:
*What dataset(s) do you plan to use, and how will you obtain the data?*
These are the current options I am looking at for retailer/wholesaler
- Retailer: 
  - James Allen: https://www.jamesallen.com/loose-diamonds/all-diamonds/
   - Blue Nile: https://www.bluenile.com/diamond-search
- Wholesaler: 
  - Brilliance: https://www.brilliance.com/diamond-search
  - Firenzejewls http://www.firenzejewels.com/diamond-search.cfm

Data will be obtained by webscraping using BeautifulSoup and Selenium 

*What is an individual sample/unit of analysis in this project? What characteristics/features do you expect to work with?*
FEATURES:

1. Carat
    - Numerical/Continuous
    - .05 - 1.0

2. Cut
    - Categorical/Ordinal
    - Excellent, Very Good, Good, Poor

3. Color 
    - Categorical/Ordinal
    - D,E,F / G,H,I,J / K,L,M

4. Clarity
    - Categorical/Ordinal
    - IF/ VVS1,VVS2 / VS1,VS2 / SI1,SI2 / SI3 / I1,I2,I3

5. Shape
    - Categorical/Nominal

6. Polish
    - Categorical/Ordinal
    - Excellent, Very Good, Good

7. Report
    - Categorical/Nominal
    - GIA,IGI,AGS

8. Depth
    - Numerical/Discrete

9. Table
    - Numerical/Discrete

10. Flourescence
    - Categorical/Ordinal
    - None, Faint, Medium, Strong

11. Retailer/Wholesaler
    - Categorical/Nominal
  

TARGET: 

Price  
    - Numerical, Continuous

## Tools:
*How do you intend to meet the tools requirement of the project?*
- Building a linear regression in python
    - regularization and/or polynomial features and other feature engineering as appropriate
- Rigorous model selection and evaluation (i.e. proper validation and testing)

*Are you planning in advance to need or use additional tools beyond those required?*
- No, not at the moment.

## MVP Goal:
*What would a minimum viable product (MVP) look like for this project?*
- Data fully scraped from two websites and organized into a database
- Data cleaned (missing values, bad formatting, etc)
- Dummy variables created for categorical variables
- Pairplot and/or heatmap
- Initial Linear Regression Model for two DataFrames
- Basic Statistical Summary

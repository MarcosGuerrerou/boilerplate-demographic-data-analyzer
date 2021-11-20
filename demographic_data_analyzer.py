import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv(r"./adult.data.csv")
    df = df.rename(columns={
        "age":"age",
        "workclass":"workclass",
        "fnlwgt":"fnlwgt",
        "education":"education",
        "education-num":"educationnum",
        "marital-status":"maritalstatus",
        "occupation":"occupation",
        "relationship":"relationship",
        "race":"race",
        "sex":"sex",
        "capital-gain":"capitalgain",
        "capital-loss":"capitalloss",
        "hours-per-week":"hoursperweek",
        "native-country":"nativecountry",
        "salary":"salary"
    })

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.value_counts(subset='race')

    # What is the average age of men?
    average_age_men = df.groupby(["sex"])["age"].mean()["Male"]
    average_age_men = round(average_age_men, 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = (df.groupby(["education"]).count()['age'].loc['Bachelors'] / df.groupby(["education"]).count()['age'].sum())*100
    percentage_bachelors = round(percentage_bachelors, 1)
    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    high_ed = ['Bachelors','Masters','Doctorate']

    higher_education = 100* (df.query("education==@high_ed").education.count() / df.groupby(["education"]).count()['age'].sum())
    lower_education = 100 - higher_education

    higher_education = round(higher_education, 1)
    lower_education = round(lower_education,1)

    # percentage with salary >50K
    rich = df.query('salary == ">50K"')
    higher_education_rich = 100 * (rich.query("education==@high_ed").education.count() / df.query("education==@high_ed").education.count())
    lower_education_rich = 100 * (rich.query("education!=@high_ed").education.count() / df.query("education!=@high_ed").education.count())

    higher_education_rich = round(higher_education_rich, 1)
    lower_education_rich = round(lower_education_rich, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hoursperweek"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers_rich = rich[rich.hoursperweek == min_work_hours].count()[0]
    num_min_workers = df[df.hoursperweek == min_work_hours].count()[0]

    rich_percentage = 100 * (num_min_workers_rich / num_min_workers)

    # What country has the highest percentage of people that earn >50K?
    country_total = df.groupby(["nativecountry"]).count()
    country_total_rich = rich.groupby(["nativecountry"]).count()

    countries = country_total.index.values.tolist()

    countries_rich_percentages = pd.DataFrame()
    countries_rich_percentages['country'] = countries
    percentages = []

    for country in countries:
        try:
            rich_perc = 100 * (country_total_rich.loc[country][0] / country_total.loc[country][0])
        except KeyError:
            rich_perc = 0
        percentages.append(rich_perc)
    
    countries_rich_percentages['richpercentage'] = percentages

    highest_earning_country = countries_rich_percentages['country'][countries_rich_percentages['richpercentage'].idxmax()]
    highest_earning_country_percentage = countries_rich_percentages['richpercentage'].max()

    highest_earning_country_percentage = round(highest_earning_country_percentage, 1)

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = rich.query("nativecountry == 'India'").groupby(["occupation"]).count()['age'].idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

if __name__ == '__main__':
    calculate_demographic_data()
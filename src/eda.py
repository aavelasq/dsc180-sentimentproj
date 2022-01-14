import pandas as pd 
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import os

# CHANGE DATE DEPENDING ON INDIVIDUAL 
cancellation_date = datetime.datetime(2021, 10, 23)
target_indiv = "GISELLE"
outdir = ".//data/out/kpop_giselle"
tempdir = ".//data/temp"

def convert_dates(data):
    '''
    converts dates to datetime object
    '''
    # convert to datetime object
    data['created_at'] = pd.to_datetime(data['created_at']) 
    # don't localize time
    data['created_at'] = data['created_at'].dt.tz_localize(None) 

    # reset hour, min, sec to 0
    data['created_at'] = data['created_at'].apply(
        lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))

    return data

def count_days(date, cancel_date):
    '''
    helper function to count number of days since deplatform date
    '''
    return date - cancel_date

def user_activity_levels(data, cancel_date):
    '''
    measures posting activity levels by counting the number of tweets
    that occur per each time window (1 day)
    '''
    groupedUsers = data[['created_at', 'text']].groupby(by='created_at')

    num_tweets = groupedUsers.count()['text'] # number of tweets per time window

    df = num_tweets.reset_index().rename(
        columns={"created_at": "Date", "text": "# Tweets"})

    df['Date'] = df['Date'].apply(
        lambda x: count_days(x, cancel_date)).dt.days

    # convert df to csv
    out_path = os.path.join(tempdir, "GISELLE_userActivityLevels.csv")
    df.to_csv(out_path)

    return df

def create_userActivity_graph(df):
    '''
    creates graph for user activity
    '''
    sns.lineplot(data=df, x="Date", y="# Tweets")
    plt.xlabel('# Days Before and After Cancellation')
    plt.title("Volume of Tweets")

    out_path = os.path.join(outdir, "GISELLE_userActivityPlot.png")
    plt.savefig(out_path, bbox_inches='tight')

def numOfTweets(df, cancel_date):
    '''
    calculates number of tweets before and after date
    '''
    if cancel_date == 0:
        before_df = df[df['Date'] < cancel_date]
        on_date_df = df[df['Date'] == cancel_date]
        after_df = df[df['Date'] > cancel_date]
    else: 
        before_df = df[df['created_at'] < cancel_date]
        on_date_df = df[df['created_at'] == cancel_date]
        after_df = df[df['created_at'] > cancel_date]

    num_df = pd.DataFrame(data={"Before": [len(before_df)], "On Date": [len(on_date_df)],"After": [len(after_df)]})

    return num_df

def createToxicityLines(df, attribute_type):
    if attribute_type == 'toxicity': 
        toxicityLevels = df.mean()['toxicity'] # mean toxicity per time window
        toxicity_df = toxicityLevels.reset_index().rename(
            columns={"created_at": "Date", "toxicity": "Mean Toxicity"})

        sns.lineplot(data=toxicity_df, x="Date", y="Mean Toxicity")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Mean Toxicity Levels")

        file_name = target_indiv + "_toxicityPlot.png"
        out_path = os.path.join(outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'severe_toxicity': 
        severe_toxicityLevels = df.mean()['severe_toxicity'] # mean severe toxicty per time window
        severe_toxicity_df = severe_toxicityLevels.reset_index().rename(
            columns={"created_at": "Date", "severe_toxicity": "Mean Severe Toxicity"})

        sns.lineplot(data=severe_toxicity_df, x="Date", y="Mean Severe Toxicity")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Mean Severe Toxicity Levels")

        file_name = target_indiv + "_severeToxicityPlot.png"
        out_path = os.path.join(outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'insult': 
        insultLevels = df.mean()['insult'] # mean insult per time window
        insult_df = insultLevels.reset_index().rename(
            columns={"created_at": "Date", "insult": "Mean Insult Levels"})

        sns.lineplot(data=insult_df, x="Date", y="Mean Insult Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Mean Insult Levels")

        file_name = target_indiv + "_insultPlot.png"
        out_path = os.path.join(outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'profanity': 
        profanityLevels = df.mean()['profanity'] # mean profanity per time window
        profanity_df = profanityLevels.reset_index().rename(
            columns={"created_at": "Date", "profanity": "Mean Profanity Levels"})

        sns.lineplot(data=profanity_df, x="Date", y="Mean Profanity Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Mean Profanity Levels")

        file_name = target_indiv + "_profanityPlot.png"
        out_path = os.path.join(outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

def month_func(month_num):
    '''
    helper function to convert month numbers to actual names
    '''
    month_li = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    return month_li[month_num + 1]

def createToxicityBoxPlots(df, attribute_type):
    '''
    creates box plot graphs based on toxicity values 
    '''
    copy_df = df.copy()
    copy_df['Month'] = copy_df['created_at'].dt.month
    copy_df['Month'] = copy_df['Month'].apply(month_func)

    if attribute_type == 'toxicity': 
        copy_df = copy_df.rename(columns={"toxicity": "Toxicity Levels"})
        sns.boxplot(data=copy_df, x="Month", y="Toxicity Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Toxicity Levels")

        file_name = target_indiv + "_BoxToxicity.png"
        out_path = os.path.join(outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'severe_toxicity': 
        copy_df = copy_df.rename(columns={"severe_toxicity": "Severe Toxicity Levels"})
        sns.boxplot(data=copy_df, x="Month", y="Severe Toxicity Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Severe Toxicity Levels")

        file_name = target_indiv + "_BoxSevToxic.png"
        out_path = os.path.join(outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'insult': 
        copy_df = copy_df.rename(columns={"insult": "Insult Levels"})
        sns.boxplot(data=copy_df, x="Month", y="Insult Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Insult Levels")

        file_name = target_indiv + "_BoxInsult.png"
        out_path = os.path.join(outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'profanity': 
        copy_df = copy_df.rename(columns={"profanity": "Profanity Levels"})
        sns.boxplot(data=copy_df, x="Month", y="Profanity Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Profanity Levels")

        file_name = target_indiv + "_BoxProfanity.png"
        out_path = os.path.join(outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

def calcToxicityOverTime(file_path, cancel_date):
    '''
    creates box plots and line graphs showing how toxicity levels change over time

    '''
    data = pd.read_csv(file_path).rename(
        columns={"date": "created_at"})
    inital_df = convert_dates(data)

    # CLEAN DATAFRAME
    inital_df = inital_df[inital_df['toxicity'] != 1000] 
    inital_df = inital_df[inital_df['severe_toxicity'] != 1000]
    inital_df = inital_df[inital_df['insult'] != 1000]
    inital_df = inital_df[inital_df['profanity'] != 1000]

    # creates and saves box plots 
    createToxicityBoxPlots(inital_df, 'toxicity')
    plt.clf()
    createToxicityBoxPlots(inital_df, 'severe_toxicity')
    plt.clf()
    createToxicityBoxPlots(inital_df, 'insult')
    plt.clf()
    createToxicityBoxPlots(inital_df, 'profanity')

    line_df = inital_df.copy()
    line_df['created_at'] = line_df['created_at'].apply(
            lambda x: count_days(x, cancel_date)).dt.days
    groupedUsers = line_df[['created_at', 'toxicity']].groupby(by='created_at')

    # creates and saves line graphs 
    plt.clf()
    createToxicityLines(groupedUsers, 'toxicity')
    plt.clf()
    createToxicityLines(groupedUsers, 'severe_toxicity')
    plt.clf()
    createToxicityLines(groupedUsers, 'insult')
    plt.clf()
    createToxicityLines(groupedUsers, 'profanity')

def calculate_stats(data, test=False):
    df = convert_dates(data)

    if test == False:
        # create csvs out of data
        userActivity_df = user_activity_levels(df, cancellation_date)
        # counts number of tweets before and after deplatforming 
        totalTweets = numOfTweets(df, cancellation_date)

        out_path = os.path.join(outdir, "GISELLE_numOfTweetsBefAft.csv")
        totalTweets.to_csv(out_path)

        # create graphs + save as pngs
        create_userActivity_graph(userActivity_df)

        calcToxicityOverTime("./data/temp/GISELLE_toxicVals.csv", cancellation_date)
    else:
        # userActivity_df = user_activity_levels(df, test_date)
        # totalTweets = numOfTweets(df, test_date)
        print("test")
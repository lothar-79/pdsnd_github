import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    repeat_request = "Wrong user input. Please try again. "
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    user_city_request = "Please choose one of the cities: Chicago, New York City or Washington: "
    city_names = ['chicago', 'new york city', 'washington']

    while True:
        user_input_city = input(user_city_request).lower()
        if (user_input_city in city_names):
            city = user_input_city
            break
        else:
            print(repeat_request)
            continue

    # get user input for month (all, january, february, ... , june)
    user_month_request = "Please choose one of the months: January, February, March, April, May, June or say all: "

    while True:
        user_input_month = input(user_month_request).lower()
        if (user_input_month in months):
            month = user_input_month
            break
        elif user_input_month == 'all':
            month = user_input_month
            break
        else:
            print(repeat_request)


    # get user input for day of week (all, monday, tuesday, ... sunday)
    user_day_request = "Please choose one of the days: monday, tuesday, wednesday, thursday, friday, saturday, sunday or say all: "
    day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    while True:
        user_input_day = input(user_day_request).lower()
        if (user_input_day in day_names):
            day = user_input_day
            break
        else:
            print(repeat_request)

    print('-'*120)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start/End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour # returns table of integer

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) +1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    number_of_month = df['month'].value_counts().index[0]  # returns first integer item of a sorted list with counted max values
    max_value_month = df['month'].value_counts().max()  # max value
    name_of_month = months[number_of_month - 1]  # returns month name fron month as integer
    print("The most common month is {} and {} times where bikes used this month.".format(name_of_month, max_value_month))

    # display the most common day of week
    name_of_day = df['day_of_week'].value_counts().index[0]  # returns first integer item of a sorted list with counted max values
    max_value_days = df['day_of_week'].value_counts().max()  # max value
    print("The most common day is {} and {} times where bikes used this day.".format(name_of_day, max_value_days))

    # display the most common start hour
    most_common_hour = df['hour'].value_counts().index[0]  # returns first integer item of a sorted list with counted max values
    max_count_most_common_hour = df['hour'].value_counts().max()  # max value
    print("The most common hour is {} o'clock and bikes were used {} times this hour.".format(most_common_hour, max_count_most_common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_stat = df['Start Station'].value_counts().index[0]  # returns first element of a sorted list with the name of the counted max value
    max_count_most_start_stat = df['Start Station'].value_counts().max()  # max value
    print("The most common start station is {} and bikes were used {} times from this station.".format(most_common_start_stat, max_count_most_start_stat))

    # display most commonly used end station
    most_common_end_stat = df['End Station'].value_counts().index[0]  # returns first element of a sorted list with the name of the counted max value
    max_count_most_end_stat = df['End Station'].value_counts().max()  # max value
    print("The most common end station is {} and bikes were used {} times from this station.".format(most_common_end_stat, max_count_most_end_stat))


    # display most frequent combination of start station and end station trip

    # returns first element of the first column of a sorted array with the name of the counted max value
    most_frequent_start = df.groupby(['Start Station'])['End Station'].value_counts().index[0][0]

    # returns first element of the second column of a sorted array with the name of the counted max value
    most_frequent_end = df.groupby(['Start Station'])['End Station'].value_counts().index[0][1]

    count_most_frequent_start_end = df.groupby(['Start Station'])['End Station'].value_counts().max()  # max value
    print("The most frequent start / end stations are: {} / {}. This combination appeared {} times.".format(most_frequent_start, most_frequent_end, count_most_frequent_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['total trip duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    total_trip_duration = df['total trip duration'].sum()
    total_trip_duration = total_trip_duration.round('S')
    print("The total sum of all trip durations is: {}.".format(total_trip_duration))

    # display mean travel time
    mean_total_trip_duration = df['total trip duration'].mean()
    mean_total_trip_duration = mean_total_trip_duration.round('S')
    print("The mean of all trip durations is: {}.".format(mean_total_trip_duration))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    counts_user_types = df['User Type'].value_counts()
    print("The counts of the user types are:")
    print(counts_user_types)
    print()

    if city == 'washington':
        print("Sorry! For Washington there is no data of Gender and Birth Year available.")
    else:
        # Display counts of gender
        counts_gender = df.groupby(['User Type'])['Gender'].value_counts()
        print("The counts of genders are:")
        print(counts_gender)
        print()

        # Display earliest year of birth
        earliest_birth_year = df['Birth Year'].min()
        print("The earliest year of birth of our subscribers is: {}".format(int(earliest_birth_year)))
        print()

        #Display most recent year of birth
        latest_birth_year = df['Birth Year'].max()
        print("The latest year of birth of our subscribers is: {}".format(int(latest_birth_year)))
        print()

        # Display most common year of birth
        count_most_common_birth_year = df['Birth Year'].value_counts().max()
        print("The count of the most common year of birth of our subscribers is: {}".format(int(count_most_common_birth_year)))
        print()

        most_common_birth_year = df['Birth Year'].value_counts().index[0]
        print("The most common year of birth of our subscribers is: {}".format(int(most_common_birth_year)))
        print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)



def raw_data(df):
    """Displays raw data to the user.
        Starts with five rows and adds five rows if requested till the end of the table"""

    start_time = time.time()

    row_count = 5
    # start with five rows
    while True:
        if row_count == 5:
            # first request
            raw_data_request = input("Would you like to see a table with five lines of raw data? Then enter yes, otherwise no: ")
            print()
        else:
            # all additional requests
            raw_data_request = input("Would you like to see a table with five more lines of raw data? Then enter yes, otherwise no: ")
            print()

        if raw_data_request.lower() == "yes":
            # printing rows and add five more rows for next request
            print(df.head(row_count))
            row_count += 5

            if row_count >= df.shape[0]:
                # proofs if end of table is reached and exits
                print("End of table !")
                break

        elif raw_data_request.lower() == "no":
            # exit if user wants to
            print("OK")
            break
        else:
            # repeats loop if input is wrong
            print("Wrong input. Please repeat your decision: ")
            continue

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*120)
    print('-'*120)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)


        restart = input('\nWould you like to restart? Then enter yes. Otherwise enter anything else.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()

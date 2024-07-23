import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to get basic data exploration.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to analyze data for Chicago, New York City, or Washington? ').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('Invalid city. Please try again.')

    # get user input for month (all, january, february,..., june)
    while True:
        month = input('Which month would you like to analyze? '
                      'Type "all" for all months or type any month between january to june. ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid month. Please try again.')

    # get user input for day of week (all, monday, tuesday,..., sunday)
    while True:
        day = input('Which day of the week would you like to analyze? '
                    'Type "all" for all days or Type a day of the week. ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid day. Please try again.')

    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_int = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month_int]

    # filter by day if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]
    print('The most common month is:', popular_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of the week is:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour is:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Start-End Station'] = df['Start Station'] + '-' + df['End Station']
    popular_combination = df['Start-End Station'].mode()[0]
    print('The most frequent combination of start station and end station trip is:', popular_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Type Counts:')
    print(user_types)

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print('Gender Counts:')
        print(gender_counts)
    except KeyError:
        print('Gender data not available.')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('Earliest Birth Year:', earliest_birth_year)
        print('Most Recent Birth Year:', most_recent_birth_year)
        print('Most Common Birth Year:', most_common_birth_year)
    except KeyError:
        print('Birth Year data not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

"""
    Runs a loop that allows the user to specify a city, month, and day to get basic data exploration.
    Loads data for the specified city and filters by month and day if applicable.
    Displays statistics on time, station usage, trip duration, and user statistics.
    Allows the user to restart the loop or exit.
    Parameters:
    None
    Returns:
    None
    """
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
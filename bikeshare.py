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
    # Welcome message
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city
    while True:
        city = input('Would you like to analyze bike share data for Chicago, New York City, or Washington? ').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('Invalid city. Please try again.')

    # Get user input for month
    while True:
        month = input('Which month would you like to analyze? '
                      'Type "all" for all months or type any month between january to june. ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid month. Please try again.')

    # Get user input for day of week
    while True:
        day = input('Which day of the week would you like to analyze? '
                    'Type "all" for all days or Type a day of the week. ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid day. Please try again.')

    # Print separator line
    print('-' * 40)

    # Return city, month, and day
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
    """
    Displays statistics on the most frequent times of travel.

    This function calculates and displays the most common month, day of the week,
    and start hour of travel. It uses the 'Start Time' column of the dataframe to
    extract the month, day of the week, and hour, and then finds the mode of each
    to determine the most common values.

    Args:
        df (pandas.DataFrame): The dataframe containing bikeshare data.
    """
    # Print a message indicating that the program is calculating the most frequent times of travel
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Extract the month from the 'Start Time' column and find the mode
    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]
    print('The most common month is:', popular_month)

    # Extract the day of week from the 'Start Time' column and find the mode
    df['day_of_week'] = df['Start Time'].dt.day_name()
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of the week is:', popular_day)

    # Extract the hour from the 'Start Time' column and find the mode
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour is:', popular_hour)

    # Print the time taken and a separator line
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df (pandas.DataFrame): The dataframe containing bikeshare data.
    """

    # Print message indicating the calculation of the most popular stations and trip
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display the most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:', popular_start_station)

    # Display the most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is:', popular_end_station)

    # Display the most frequent combination of start station and end station trip
    df['Start-End Station'] = df['Start Station'] + '-' + df['End Station']
    popular_combination = df['Start-End Station'].mode()[0]
    print('The most frequent combination of start station and end station trip is:', popular_combination)

    # Print the time taken and a separator line
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df (pandas.DataFrame): The dataframe containing bikeshare data.

    Returns:
        None
    """
    # Start the timer
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate the total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is:', total_travel_time)

    # Calculate the mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is:', mean_travel_time)

    # Print the time taken and a separator line
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """
    Displays statistics on bikeshare users.

    This function calculates and displays various statistics about bikeshare users,
    including the counts of different user types, gender counts, and the earliest,
    most recent, and most common year of birth.

    Args:
        df (pandas.DataFrame): The dataframe containing bikeshare data.
    """
    # Start the timer
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Type Counts:')
    print(user_types)

    # Display counts of gender
    try:
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print('Gender Counts:')
        print(gender_counts)
    except KeyError:
        print('Gender data not available.')

    # Display earliest, most recent, and most common year of birth
    try:
        # Get earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])

        # Display the results
        print('Earliest Birth Year:', earliest_birth_year)
        print('Most Recent Birth Year:', most_recent_birth_year)
        print('Most Common Birth Year:', most_common_birth_year)
    except KeyError:
        print('Birth Year data not available.')

    # Print the time taken and a separator line
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
    """
    Main function to run the program.

    This function repeatedly asks for user input for city, month, and day,
    loads the corresponding data, and displays statistics. The program ends
    when the user enters 'no' to restart.
    """

    while True:
        # Ask for user input for city, month, and day
        city, month, day = get_filters()

        # Load the corresponding data
        df = load_data(city, month, day)

        # Display time statistics
        time_stats(df)

        # Display station statistics
        station_stats(df)

        # Display trip duration statistics
        trip_duration_stats(df)

        # Display user statistics
        user_stats(df)

        # Ask user if they want to restart
        restart = input('\nWould you like to restart? Enter yes or no.\n')

        # If user enters 'no', exit the loop
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
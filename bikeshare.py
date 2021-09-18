import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def display_data(pd_series):
    """
    Display data from a Panda Series in chunks of chosen size.
    """
    view_data = 'Y'
    chunk_size = -1

    while chunk_size < 0:
        try:
            chunk_size = int(input('\nHow many rows would you like to see each time? ').lower())
        except:
            print('You must input an integer number greater than or equal to zero!')

    if chunk_size == 0:
        view_data = 'No'

    chunk_size += 1
    start_loc = 0

    while view_data in ('y','Y','Yes','YES','yes'):
        display = pd_series[start_loc:start_loc+chunk_size]
        start_loc += chunk_size
        print(display)
        view_data = input("Do you wish to continue? ").lower()

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bike-share data!')

    #Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Enter the desired city: (Chicago/New York City/Whashington) ').lower()

    if city == 'new york':
        city = 'new york city'

    while city not in CITY_DATA:
        city = input('Please, choose one of these cities: Chicago, New York City or Whashington. ').lower()
        if city == 'new york':
            city = 'new york city'

    #Get user input for month (all, january, february, ... , june)
    month = input('''Enter the desired month: (January, February, ..., June, or "all") ''').lower()

    if month in ('\"all\"', '\'all\''):
        month = 'all'

    while month != 'all' and month not in MONTHS:
        month = input('''Please, choose one month from January to June or "all".''').lower()

    #Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('''Enter the desired day of week: (Sunday, Monday, ..., Saturday, or "all") ''').lower()

    if day in ('\"all\"', '\'all\''):
        day = 'all'

    while day != 'all' and day not in DAYS:
        day = input('''Please, choose one day of week from Sunday to Saturday or "all". ''').lower()

    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    #Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    #Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    dfst = df['Start Time']

    #Extract month and day of week from Start Time to create new columns
    df['month'] = dfst.dt.month
    df['day_of_week'] = dfst.dt.dayofweek


    #Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        month = MONTHS.index(month) +1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

    #Filter by day of week if applicable    
    if day != 'all':
        #Filter by day of week to create the new dataframe
        day = DAYS.index(day)
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month
    print('Most common month:', MONTHS[df['month'].mode()[0] - 1].capitalize())

    #Display the most common day of week
    print('Most common day of week:', DAYS[df['day_of_week'].mode()[0]].capitalize())

    #Display the most common start hour
    print('Most common start hour: ', df['Start Time'].dt.hour.mode()[0],':00 ', sep='')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    print('Most commonly used start station:', df['Start Station'].mode()[0])

    #Display most commonly used end station
    print('Most commonly used end station:', df['End Station'].mode()[0])

    #Display most frequent combination of start station and end station trip
    print('Most frequent combination of start station and end station trip:\n')
    display_data(df.groupby(['Start Station', 'End Station'])['Start Time'].size().sort_values(ascending=False))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    total_tt = pd.to_timedelta(df['End Time'].dt.strftime('%H:%M:%S')) - pd.to_timedelta(df['Start Time'].dt.strftime('%H:%M:%S'))
    print('Total travel time:\n')
    display_data(total_tt)

    #Display mean travel time
    mean_tt = total_tt.mean()
    print('Average duration of all travel times:', mean_tt)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, washington=False):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print('Quantity of user types:\n', df['User Type'].value_counts())

    if washington:
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    else:
        #Display counts of gender
        print('\nQuantity of genders:\n', df['Gender'].value_counts())

        #Display earliest, most recent, and most common year of birth
        print('\nEarliest birth year:', df['Birth Year'].dropna(axis=0).astype(dtype='int64').min())
        print('Most recent birth year:', df['Birth Year'].dropna(axis=0).astype(dtype='int64').max())
        print('Most common birth year:', df['Birth Year'].dropna(axis=0).astype(dtype='int64').mode()[0])
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)

        if city == 'washington': #check if city is Washington, as it doesn't have 'Gender' nor 'Birth Year' columns
            user_stats(df, True)
        else:
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ('y','Y','Yes','YES','yes'):
            break

if __name__ == "__main__":
	main()

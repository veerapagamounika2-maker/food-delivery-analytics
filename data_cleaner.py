import pandas as pd

def load_and_clean():
    # Load data
    df = pd.read_csv("Food_Delivery_Times.csv")

    print("Original shape:", df.shape)
    print("Missing values:\n", df.isnull().sum())

    # Drop duplicates
    df = df.drop_duplicates()

    # Drop missing values
    df = df.dropna()

    # Rename columns for easy use
    df.columns = [
        'order_id', 'distance_km', 'weather',
        'traffic_level', 'time_of_day', 'vehicle_type',
        'preparation_time', 'courier_experience',
        'delivery_time_min'
    ]

    # Fix data types
    df['distance_km'] = df['distance_km'].astype(float)
    df['preparation_time'] = df['preparation_time'].astype(int)
    df['courier_experience'] = df['courier_experience'].astype(int)
    df['delivery_time_min'] = df['delivery_time_min'].astype(int)

    # Add new useful columns
    df['total_time'] = df['preparation_time'] + df['delivery_time_min']
    df['is_delayed'] = df['delivery_time_min'].apply(
        lambda x: 'Delayed' if x > 60 else 'On Time'
    )

    print("\nCleaned shape:", df.shape)
    print("\nSample data:")
    print(df.head(3))

    return df

if __name__ == "__main__":
    df = load_and_clean()
    # Save cleaned data

    df.to_csv("cleaned_data.csv", index=False)
    print("\n✅ Cleaned data saved!")
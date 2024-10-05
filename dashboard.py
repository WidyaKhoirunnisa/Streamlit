import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')

#load dataset
@st.cache_data  
def load_data():
    return pd.read_csv("https://raw.githubusercontent.com/WidyaKhoirunnisa/Bike-Sharing-Dataset/main/day.csv")

def main():
    st.title("Analisis Penyewaan Sepeda")
    
    #load data
    day_df = load_data()
    st.write("Data Penyewaan Sepeda:")
    st.dataframe(day_df)

    #data assessing
    st.subheader("Data Assessing")
    duplicates = day_df.duplicated().sum()
    missing_values = day_df.isnull().sum()
    st.write(f"Jumlah duplikasi: {duplicates}")
    st.write("Nilai yang hilang:")
    st.write(missing_values)

    #data cleaning, dteday dikonversi ke format datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    st.write("Format tanggal telah diperbarui.")
    
    #exploratory data analysis (EDA)
    st.header("Pengaruh Cuaca (Kelembapan dan Suhu) terhadap Jumlah Penyewaan Sepeda")

    #pengaruh cuaca terhadap jumlah penyewaan sepeda
    weather_effects = day_df.groupby(['temp', 'hum']).agg({
        'cnt': ['sum', 'max', 'min', 'mean', 'std']
    }).reset_index()
    st.write("Pengaruh kelembapan dan suhu terhadap jumlah penyewaan sepeda:")
    st.dataframe(weather_effects.head())

    st.header("Tren Bulanan dan Musiman terhadap Jumlah Penyewaan Sepeda")
    
    #tren bulanan terhadap jumlah penyewaan sepeda
    monthly_stats = day_df.groupby('mnth').agg({
        'cnt': ['sum', 'max', 'min', 'mean', 'std']
    }).reset_index()
    st.write("Tren bulanan terhadap jumlah penyewaan sepeda:")
    st.dataframe(monthly_stats)

    #tren musimam terhadap jumlah penyewaan sepeda
    seasonal_stats = day_df.groupby('season').agg({
        'cnt': ['sum', 'max', 'min', 'mean', 'std']
    }).reset_index()
    st.write("Tren musiman terhadap jumlah penyewaan sepeda:")
    st.dataframe(seasonal_stats)

    st.header("Visualisasi")

    #scatter plot untuk suhu
    st.subheader("Hubungan Suhu dengan Jumlah Penyewaan Sepeda")
    fig_temp, ax_temp = plt.subplots(figsize=(12, 8))
    sns.scatterplot(data=day_df, x='temp', y='cnt', hue='season', palette='coolwarm', alpha=0.7, ax=ax_temp)
    ax_temp.set_title('Hubungan Suhu dengan Jumlah Penyewaan Sepeda')
    ax_temp.set_xlabel('Suhu')
    ax_temp.set_ylabel('Jumlah Penyewaan Sepeda')
    ax_temp.legend(title='Musim')
    st.pyplot(fig_temp)

    #scatter plot untuk kelembapan
    st.subheader("Hubungan Kelembaban dengan Jumlah Penyewaan Sepeda")
    fig_hum, ax_hum = plt.subplots(figsize=(12, 8))
    sns.scatterplot(data=day_df, x='hum', y='cnt', hue='season', palette='coolwarm', alpha=0.7, ax=ax_hum)
    ax_hum.set_title('Hubungan Kelembaban dengan Jumlah Penyewaan Sepeda')
    ax_hum.set_xlabel('Kelembaban')
    ax_hum.set_ylabel('Jumlah Penyewaan Sepeda')
    ax_hum.legend(title='Musim')
    st.pyplot(fig_hum)

    #hubungan antara faktor cuaca dan jumlah penyewa sepeda
    st.subheader("Hubungan antara Faktor Cuaca dan Jumlah Penyewaan Sepeda")
    fig_corr, ax_corr = plt.subplots(figsize=(12, 8))
    sns.heatmap(day_df[['temp', 'hum', 'cnt']].corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=.5, ax=ax_corr)
    ax_corr.set_title('Korelasi antara Faktor Cuaca dan Jumlah Penyewaan Sepeda')
    st.pyplot(fig_corr)

    #visualisasi tren bulanan penyewaan sepeda
    month_map = {1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April', 5: 'Mei', 
                 6: 'Juni', 7: 'Juli', 8: 'Agustus', 9: 'September', 10: 'Oktober', 
                 11: 'November', 12: 'Desember'}
    day_df['mnth'] = day_df['mnth'].map(month_map)

    st.subheader("Tren Bulanan Penyewaan Sepeda")
    fig_month, ax_month = plt.subplots(figsize=(10, 6))
    sns.barplot(x='mnth', y='cnt', data=day_df, estimator='mean', ci=None, palette='Spectral', ax=ax_month)
    ax_month.set_title('Tren Bulanan Penyewaan Sepeda')
    ax_month.set_xlabel('Bulan')
    ax_month.set_ylabel('Rata-rata Penyewaan Sepeda')
    ax_month.set_xticklabels(ax_month.get_xticklabels(), rotation=45)
    st.pyplot(fig_month)

    #visualisasi tren musiman penyewaan sepeda
    season_map = {1: 'Dingin', 2: 'Semi', 3: 'Panas', 4: 'Gugur'}
    day_df['season'] = day_df['season'].map(season_map)

    st.subheader("Tren Musiman Penyewaan Sepeda")
    fig_season, ax_season = plt.subplots(figsize=(8, 5))
    sns.barplot(x='season', y='cnt', data=day_df, estimator='mean', ci=None, palette='coolwarm', ax=ax_season)
    ax_season.set_title('Tren Musiman Penyewaan Sepeda')
    ax_season.set_xlabel('Musim')
    ax_season.set_ylabel('Rata-rata Penyewaan Sepeda')
    st.pyplot(fig_season)

if __name__ == "__main__":
    main()

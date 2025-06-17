import pandas as pd
import matplotlib.pyplot as plt
import kagglehub

# 1. Shkarkoni versionin më të fundit të dataset-it nga KaggleHub
path = kagglehub.dataset_download("risakashiwabara/tokyo-weatherdata")

# 2. Shfaqni rrugën ku është ruajtur dataset-i
print("Rruga e dataset-it:", path)

# 3. Ngarkoni skedarin CSV nga rruga që është krijuar
df = pd.read_csv(f"{path}/weather_tokyo_data.csv")

# 4. Pastrimi i të dhënave:
# Sigurohuni që kolonat 'year' dhe 'day' janë të plota për krijimin e datës
df['Date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['day'], format='%Y-%m/%d')  # Bashkoni 'year' dhe 'day' për të krijuar datën

# Pastroni emrat e kolonave dhe sigurohuni që 'temperature' është i saktë
df.columns = [item.strip() for item in df.columns]  # Pastrimi i hapësirave në fund dhe para të emrave të kolonave

# Sigurohuni që temperaturat negative janë të trajtuara
df['temperature'] = df['temperature'].apply(lambda x: float(x.replace('(', '-').replace(')', '')))  # Ndrysho temperaturat me kllapa për të shënuar temperaturat negative

# 5. Temperaturat mujore: Llogaritni temperaturën mesatare për çdo muaj
df['Month'] = df['Date'].dt.month  # Nxirrni muajin nga kolona 'Date'
monthly_avg_temp = df.groupby('Month')['temperature'].mean()

# Vizualizoni temperaturën mesatare mujore
plt.figure(figsize=(10, 6))
monthly_avg_temp.plot(kind='bar', color='skyblue')
plt.title('Temperatura mesatare mujore në Tokio')
plt.xlabel('Muaji')
plt.ylabel('Temperatura mesatare (°C)')
plt.xticks(ticks=range(12), labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
plt.tight_layout()
plt.show()

# 6. Trendet e Temperaturës: Vizualizimi i temperaturave për kohë
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['temperature'], color='orange', linewidth=1)
plt.title('Trendet e Temperaturës në Tokio')
plt.xlabel('Data')
plt.ylabel('Temperatura (°C)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 7. Përmbledhje e Temperaturës: Llogaritni temperaturën mesatare për të gjithë datasetin dhe e formatoni në 2 decimal points
avg_temperature = df['temperature'].mean()
print(f"\nTemperatura mesatare për të gjithë datasetin: {avg_temperature:.2f}°C")

# 8. Ditët më të nxehta dhe më të ftohta: Gjeni ditën më të nxehtë dhe më të ftohtë dhe shfaqni të dhënat përkatëse
hottest_day = df.loc[df['temperature'].idxmax()]
coldest_day = df.loc[df['temperature'].idxmin()]

print("\nDita më e nxehtë:")
print(hottest_day)
print("\nDita më e ftohtë:")
print(coldest_day)

# 9. Temperatura mesatare për çdo sezon (Pranverë, Verë, Vjeshtë, Dimër)
seasons = {
    'Pranvera': [3, 4, 5],
    'Vera': [6, 7, 8],
    'Vjeshta': [9, 10, 11],
    'Dimri': [12, 1, 2]
}

# Llogaritni temperaturën mesatare për çdo sezon
seasonal_avg_temp = {}
for season, months in seasons.items():
    seasonal_data = df[df['Month'].isin(months)]
    seasonal_avg_temp[season] = seasonal_data['temperature'].mean()

print("\nTemperaturat mesatare për çdo sezon:")
for season, temp in seasonal_avg_temp.items():
    print(f"{season}: {temp:.2f}°C")

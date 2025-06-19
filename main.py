import pandas as pd; import matplotlib.pyplot as plt; import kagglehub

# Shkarkimi i të dhënave
dataset_path = kagglehub.dataset_download("risakashiwabara/tokyo-weatherdata")
print("Rruga e dataset-it:", dataset_path)

# Leximi i të dhënave
df = pd.read_csv(f"{dataset_path}/weather_tokyo_data.csv")

# Konvertimi i datës dhe pastrimi i kolonave
df.columns = [col.strip() for col in df.columns]
df["Date"] = pd.to_datetime(df["year"].astype(str) + "-" + df["day"], format="%Y-%m/%d")
df["temperature"] = df["temperature"].map(lambda val: float(val.replace("(", "-").replace(")", "")))

# Mesatarja mujore
df["Month"] = df["Date"].dt.month
avg_temp_monthly = df.groupby("Month")["temperature"].mean()

# Grafiku i mesatares mujore
plt.figure(figsize=(10, 6)); avg_temp_monthly.plot(kind="bar", color="skyblue")
plt.title("Temperatura mesatare mujore në Tokio")
plt.xlabel("Muaji"); plt.ylabel("Temperatura mesatare (°C)")
plt.xticks(ticks=range(12), labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
plt.tight_layout(); plt.show()

# Grafiku i trendit ditor
plt.figure(figsize=(12, 6))
plt.plot(df["Date"], df["temperature"], color="orange", linewidth=1)
plt.title("Trendet e Temperaturës në Tokio")
plt.xlabel("Data"); plt.ylabel("Temperatura (°C)")
plt.xticks(rotation=45); plt.tight_layout(); plt.show()

# Temperatura mesatare totale
mesatarja = df["temperature"].mean()
print(f"\nTemperatura mesatare për të gjithë datasetin: {mesatarja:.2f}°C")

# Ditët ekstreme
max_dita = df.loc[df["temperature"].idxmax()]
min_dita = df.loc[df["temperature"].idxmin()]
print("\nDita më e nxehtë:"); print(max_dita)
print("\nDita më e ftohtë:"); print(min_dita)

# Mesataret sezonale
sezonet = {"Pranvera": [3, 4, 5], "Vera": [6, 7, 8], "Vjeshta": [9, 10, 11], "Dimri": [12, 1, 2]}
mesataret_sezonale = {sezon: df[df["Month"].isin(muajt)]["temperature"].mean() for sezon, muajt in sezonet.items()}

print("\nTemperaturat mesatare për çdo sezon:")
for sez, temp in mesataret_sezonale.items():
    print(f"{sez}: {temp:.2f}°C")

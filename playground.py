import numpy as np
from scipy.stats import poisson, kstest

# Ihre beobachteten Messwerte
beobachtete_werte = np.array([36382,23382,33300,33098,39325])
#beobachtete_werte = np.array([8.6, 7.6, 8.1, 8.0, 9.1, 8.7, 8.3])
i = 0
p = []
while i < 10000:
    # Lambda-Wert für die Poisson-Verteilung
    lambda_value = 33000

    # Generiere 7 zufällige Werte aus der Poisson-Verteilung
    poisson_values = np.random.poisson(lambda_value, size=7)
    beobachtete_werte = poisson_values
    # Mittelwert der beobachteten Werte
    mittelwert = np.mean(beobachtete_werte)

    # Berechnen der erwarteten Häufigkeiten basierend auf der Poisson-Verteilung
    erwartete_haeufigkeiten = poisson.pmf(beobachtete_werte, mu=mittelwert) * len(beobachtete_werte)

    # Durchführung des Kolmogorov-Smirnov-Tests für Anpassung
    ks_statistic, p_value = kstest(beobachtete_werte, 'poisson', args=(mittelwert,))
    p.append(p_value)
    i += 1
p_mean = np.mean(p)
p_min = np.min(p)
# Ausgabe der Ergebnisse
print("Mittelwert:", mittelwert)
print("Erwartete Häufigkeiten:", erwartete_haeufigkeiten)
print("KS-Statistik:", ks_statistic)
print("P-Wert:", p_value)

# Überprüfen der Nullhypothese basierend auf dem P-Wert und einem Signifikanzniveau von 0.05
if p_value > 1-0.05:
    print("Die Daten stammen wahrscheinlich aus einer Poisson-Verteilung.")
else:
    print("Die Daten stammen wahrscheinlich nicht aus einer Poisson-Verteilung.")

print("Generierte Werte aus der Poisson-Verteilung:", poisson_values)

print(p_mean, p_min)
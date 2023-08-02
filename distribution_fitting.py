from fitter import Fitter
import numpy as np
from scipy.stats import poisson

# Beispiel-Daten als Liste
your_data = [33047, 32975, 33260, 33202, 33248 ,33042 ,32600]

# Erstelle eine Fitter-Instanz und passe deine Daten an die fit()-Methode an
f = Fitter(your_data)
f.fit()

# Schätze die Parameter der Poisson-Verteilung
lambda_param = np.mean(your_data)

# Teste die Poisson-Verteilung manuell mit dem Chi-Quadrat-Test
expected_counts = poisson.pmf(your_data, lambda_param) * np.sum(your_data)
chi2_statistic = np.sum((your_data - expected_counts)**2 / expected_counts)
p_value = 1 - poisson.cdf(chi2_statistic, len(your_data) - 1)

# Vergleiche die Passgenauigkeit der Poisson-Verteilung mit anderen Verteilungen
best_fit = 'poisson' if p_value > 0.05 else f.df_errors['sumsquare_error'].idxmin()

# Gib eine Zusammenfassung der Ergebnisse aus
print("Beste Passende Verteilung:", best_fit)
print(f.df_errors)
print(f.fitted_param[best_fit])

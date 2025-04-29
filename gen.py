import requests
import numpy as np
from scipy.integrate import solve_ivp

KEY = ""
URL = "https://api.sncf.com/v1/coverage/sncf/traffic_reports"

def requeteTrains(key=KEY, url=URL):
    headers = {
        "Authorization": key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        reports = response.json().get('traffic_reports', [])
    
        trains_supprimes = 0
        trains_retard = 0
    
        for report in reports:
            effect = report.get('impact', {}).get('effect', '')
        
            if effect == "NO_SERVICE":
                trains_supprimes += 1
            elif effect in ("REDUCED_SERVICE", "MODIFIED_SERVICE"):
                trains_retard += 1
        return trains_supprimes, trains_retard
    else:
        raise RuntimeError(f"Erreur HTTP {response.status_code} lors de la requête SNCF.")

def double_pendule_etat(t, y0, l1=1.0, l2=1.0, m1=1.0, m2=1.0, g=9.81):
    """
    Renvoie l'état (angles et vitesses) d'un double pendule après un temps t.
    
    Args:
        t : durée en secondes
        y0 : conditions initiales [theta1, omega1, theta2, omega2]
        l1, l2 : longueurs des pendules
        m1, m2 : masses des pendules
        g : gravité
    
    Returns:
        Etat final [theta1, omega1, theta2, omega2] au temps t
    """
    
    def equations(t, y):
        theta1, omega1, theta2, omega2 = y
        
        delta = theta2 - theta1
        
        den1 = (m1 + m2) * l1 - m2 * l1 * np.cos(delta) ** 2
        den2 = (l2 / l1) * den1
        
        dtheta1_dt = omega1
        dtheta2_dt = omega2
        
        domega1_dt = (m2 * l1 * omega1**2 * np.sin(delta) * np.cos(delta) +
                      m2 * g * np.sin(theta2) * np.cos(delta) +
                      m2 * l2 * omega2**2 * np.sin(delta) -
                      (m1 + m2) * g * np.sin(theta1)) / den1
        
        domega2_dt = (-m2 * l2 * omega2**2 * np.sin(delta) * np.cos(delta) +
                      (m1 + m2) * g * np.sin(theta1) * np.cos(delta) -
                      (m1 + m2) * l1 * omega1**2 * np.sin(delta) -
                      (m1 + m2) * g * np.sin(theta2)) / den2
        
        return [dtheta1_dt, domega1_dt, dtheta2_dt, domega2_dt]
    
    sol = solve_ivp(equations, [0, t], y0, t_eval=[t], method='RK45')
    print(sol)
    if sol.success:
        return sol.y[:, 0]  # Correction ici : sol.y[:, 0] (pas -1)
    else:
        raise RuntimeError("Erreur d'intégration du double pendule.")

def generateur_pseudo_aleatoire():
    t = 42
    trains_supprimes, trains_retard = requeteTrains()  # Appeler vraiment l'API ici
    print(trains_retard, trains_supprimes)
    # Encodage des données dans le double pendule

    theta1 = (trains_retard % 360) * np.pi / 180  # convertir degrés -> radians
    omega1 = (trains_supprimes + trains_retard) % 5  # vitesse limitée à ±10 rad/s
    theta2 = (trains_supprimes % 360) * np.pi / 180
    omega2 = (trains_supprimes - trains_retard) % 5

    sol_pendules = double_pendule_etat(
        t,
        [theta1, omega1, theta2, omega2]
    )
    return float(np.sum(sol_pendules))  # S'assurer que c'est un float au retour

def main():
    print("Valeur générée :", generateur_pseudo_aleatoire())

if __name__ == "__main__":
    main()

"""
Reproduction fidèle de la vulnérabilité SQL Injection réelle de OWASP Juice Shop
(routes/login.ts) et de sa correction, à des fins de vérification.
"""
import sqlite3
import hashlib

def setup_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("""CREATE TABLE Users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        deletedAt TEXT
    )""")
    admin_hash = hashlib.md5("admin123".encode()).hexdigest()
    conn.execute("INSERT INTO Users (id, email, password, deletedAt) VALUES (1, 'admin@juice-sh.op', ?, NULL)", (admin_hash,))
    conn.commit()
    return conn

def security_hash(password):
    return hashlib.md5(password.encode()).hexdigest()

# ============================================================
# CODE VULNERABLE (identique à routes/login.ts de Juice Shop)
# ============================================================
def login_VULNERABLE(conn, email, password):
    query = f"SELECT * FROM Users WHERE email = '{email}' AND password = '{security_hash(password)}' AND deletedAt IS NULL"
    print(f"  Requête SQL exécutée : {query}")
    cur = conn.execute(query)
    return cur.fetchone()

# ============================================================
# CODE CORRIGE (requête paramétrée)
# ============================================================
def login_CORRIGE(conn, email, password):
    query = "SELECT * FROM Users WHERE email = ? AND password = ? AND deletedAt IS NULL"
    print(f"  Requête SQL exécutée : {query}  |  paramètres = ('{email}', '<hash>')")
    cur = conn.execute(query, (email, security_hash(password)))
    return cur.fetchone()

payload_email = "' OR 1=1--"
payload_password = "n_importe_quoi"

print("="*70)
print("AVANT CORRECTION — test du payload d'injection SQL")
print("="*70)
conn = setup_db()
result = login_VULNERABLE(conn, payload_email, payload_password)
if result:
    print(f"  RESULTAT : Connexion REUSSIE sans mot de passe valide -> {result}")
    print("  ==> VULNERABLE : authentification contournée")
else:
    print("  RESULTAT : Connexion refusée")
conn.close()

print()
print("="*70)
print("APRES CORRECTION — même payload, sur le code corrigé")
print("="*70)
conn = setup_db()
result = login_CORRIGE(conn, payload_email, payload_password)
if result:
    print(f"  RESULTAT : Connexion réussie -> {result}")
    print("  ==> TOUJOURS VULNERABLE")
else:
    print("  RESULTAT : Connexion refusée (aucune ligne ne correspond)")
    print("  ==> CORRIGE : l'injection ne fonctionne plus")
conn.close()

print()
print("="*70)
print("VERIFICATION COMPLEMENTAIRE — un vrai identifiant fonctionne toujours")
print("="*70)
conn = setup_db()
result = login_CORRIGE(conn, "admin@juice-sh.op", "admin123")
if result:
    print(f"  RESULTAT : Connexion réussie avec les vrais identifiants -> {result}")
    print("  ==> La correction n'empêche pas les connexions légitimes")
conn.close()


import sqlite3
import json

def create_connection():
    conn = sqlite3.connect('cv_database.db')
    return conn

def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cvs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            analyzed BOOLEAN NOT NULL DEFAULT 0,
            full_name TEXT,
            email TEXT
        )
    ''')
    # Add columns if they don't exist (for existing databases)
    try:
        c.execute("ALTER TABLE cvs ADD COLUMN full_name TEXT")
    except sqlite3.OperationalError:
        pass # Column already exists
    try:
        c.execute("ALTER TABLE cvs ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        pass # Column already exists

    c.execute('''
        CREATE TABLE IF NOT EXISTS job_description (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL
        )
    ''')
    
    # Create new table for analysis results
    c.execute('''
        CREATE TABLE IF NOT EXISTS cv_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cv_name TEXT NOT NULL,
            nombre_candidato TEXT,
            email TEXT,
            puesto_solicitado TEXT,
            score_fit REAL,
            nivel_experiencia TEXT,
            tiempo_experiencia TEXT,
            habilidades_coincidentes TEXT,
            experiencia_coincidente TEXT,
            puntos_de_mejora TEXT,
            resumen_idoneidad TEXT,
            recomendacion TEXT,
            riesgos TEXT,
            fortalezas TEXT,
            analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cv_name) REFERENCES cvs (name)
        )
    ''')
    
    # Add new columns to existing cv_analysis table if they don't exist
    new_columns = [
        ("score_fit", "REAL"),
        ("nivel_experiencia", "TEXT"),
        ("tiempo_experiencia", "TEXT"),
        ("recomendacion", "TEXT"),
        ("riesgos", "TEXT"),
        ("fortalezas", "TEXT")
    ]
    
    for column_name, column_type in new_columns:
        try:
            c.execute(f"ALTER TABLE cv_analysis ADD COLUMN {column_name} {column_type}")
        except sqlite3.OperationalError:
            pass # Column already exists
    
    conn.commit()
    conn.close()

def update_cv_analysis(cv_name, full_name, email):
    conn = create_connection()
    c = conn.cursor()
    c.execute("UPDATE cvs SET analyzed = 1, full_name = ?, email = ? WHERE name = ?", (full_name, email, cv_name))
    conn.commit()
    conn.close()

def save_analysis_result(cv_name, analysis_data):
    """Save complete analysis result to database"""
    conn = create_connection()
    c = conn.cursor()
    
    # Extract data from analysis_data dictionary
    nombre_candidato = analysis_data.get("nombre_candidato", "N/A")
    email = analysis_data.get("email", "N/A")
    puesto_solicitado = analysis_data.get("puesto_solicitado", "N/A")
    score_fit = analysis_data.get("score_fit", 0.0)
    nivel_experiencia = analysis_data.get("nivel_experiencia", "N/A")
    tiempo_experiencia = analysis_data.get("tiempo_experiencia", "N/A")
    
    # Convert lists to JSON strings for storage
    habilidades_coincidentes = json.dumps(analysis_data.get("analisis_match", {}).get("habilidades_coincidentes", []), ensure_ascii=False)
    experiencia_coincidente = json.dumps(analysis_data.get("analisis_match", {}).get("experiencia_coincidente", []), ensure_ascii=False)
    puntos_de_mejora = json.dumps(analysis_data.get("puntos_de_mejora", []), ensure_ascii=False)
    riesgos = json.dumps(analysis_data.get("riesgos", []), ensure_ascii=False)
    fortalezas = json.dumps(analysis_data.get("fortalezas", []), ensure_ascii=False)
    
    resumen_idoneidad = analysis_data.get("resumen_idoneidad", "N/A")
    recomendacion = analysis_data.get("recomendacion", "N/A")
    
    # Insert or update analysis result
    c.execute('''
        INSERT OR REPLACE INTO cv_analysis 
        (cv_name, nombre_candidato, email, puesto_solicitado, score_fit, nivel_experiencia, 
         tiempo_experiencia, habilidades_coincidentes, experiencia_coincidente, 
         puntos_de_mejora, resumen_idoneidad, recomendacion, riesgos, fortalezas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (cv_name, nombre_candidato, email, puesto_solicitado, score_fit, nivel_experiencia, 
          tiempo_experiencia, habilidades_coincidentes, experiencia_coincidente, 
          puntos_de_mejora, resumen_idoneidad, recomendacion, riesgos, fortalezas))
    
    conn.commit()
    conn.close()

def get_analysis_result(cv_name):
    """Get analysis result for a specific CV"""
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM cv_analysis WHERE cv_name = ?", (cv_name,))
    result = c.fetchone()
    conn.close()
    
    if result:
        # Helper function to safely parse JSON
        def safe_json_loads(json_str, default=[]):
            if not json_str or json_str.strip() == '':
                return default
            try:
                return json.loads(json_str)
            except (json.JSONDecodeError, TypeError):
                return default
        
        # Convert JSON strings back to lists
        return {
            "cv_name": result[1],
            "nombre_candidato": result[2] or "",
            "email": result[3] or "",
            "puesto_solicitado": result[4] or "",
            "score_fit": result[5] or 0.0,
            "nivel_experiencia": result[6] or "",
            "tiempo_experiencia": result[7] or "",
            "habilidades_coincidentes": safe_json_loads(result[8]),
            "experiencia_coincidente": safe_json_loads(result[9]),
            "puntos_de_mejora": safe_json_loads(result[10]),
            "resumen_idoneidad": result[11] or "",
            "recomendacion": result[12] or "",
            "riesgos": safe_json_loads(result[13]),
            "fortalezas": safe_json_loads(result[14]),
            "analysis_date": result[15]
        }
    return None

def get_all_analysis_results():
    """Get all analysis results"""
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM cv_analysis ORDER BY analysis_date DESC")
    results = c.fetchall()
    conn.close()
    
    # Helper function to safely parse JSON
    def safe_json_loads(json_str, default=[]):
        if not json_str or json_str.strip() == '':
            return default
        try:
            return json.loads(json_str)
        except (json.JSONDecodeError, TypeError):
            return default
    
    analysis_list = []
    for result in results:
        analysis_list.append({
            "cv_name": result[1],
            "nombre_candidato": result[2] or "",
            "email": result[3] or "",
            "puesto_solicitado": result[4] or "",
            "score_fit": result[5] or 0.0,
            "nivel_experiencia": result[6] or "",
            "tiempo_experiencia": result[7] or "",
            "habilidades_coincidentes": safe_json_loads(result[8]),
            "experiencia_coincidente": safe_json_loads(result[9]),
            "puntos_de_mejora": safe_json_loads(result[10]),
            "resumen_idoneidad": result[11] or "",
            "recomendacion": result[12] or "",
            "riesgos": safe_json_loads(result[13]),
            "fortalezas": safe_json_loads(result[14]),
            "analysis_date": result[15]
        })
    return analysis_list

def save_job_description(description):
    conn = create_connection()
    c = conn.cursor()
    c.execute("DELETE FROM job_description") # Only keep one job description
    c.execute("INSERT INTO job_description (description) VALUES (?)", (description,))
    conn.commit()
    conn.close()

def get_job_description():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT description FROM job_description ORDER BY id DESC LIMIT 1")
    result = c.fetchone()
    conn.close()
    return result[0] if result else ""

def get_unanalyzed_cvs():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT name, path FROM cvs WHERE analyzed = 0")
    cvs = c.fetchall()
    conn.close()
    return cvs

def add_cv(name, path):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM cvs WHERE name = ?", (name,))
    exists = c.fetchone()
    if not exists:
        c.execute("INSERT INTO cvs (name, path) VALUES (?, ?)", (name, path))
    conn.commit()
    conn.close()

def get_all_cvs():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT name, analyzed, full_name, email FROM cvs")
    cvs = c.fetchall()
    conn.close()
    return cvs

def clear_database():
    conn = create_connection()
    c = conn.cursor()
    c.execute("DELETE FROM cvs")
    c.execute("DELETE FROM cv_analysis")
    conn.commit()
    conn.close()


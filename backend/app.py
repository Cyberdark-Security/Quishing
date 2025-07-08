# Backend Flask para recolectar estadísticas de la demo (OPCIONAL)

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS 
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Almacenamiento simple en archivo (para demo)
# CAMBIO: Usar /tmp para mayor compatibilidad con entornos de App Service
DATA_FILE = '/tmp/demo_analytics.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # Manejar caso de archivo JSON corrupto o vacío
                return {'visits': [], 'submissions': []}
    return {'visits': [], 'submissions': []}

def save_data(data):
    # Asegurarse de que el directorio /tmp exista (aunque suele existir)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# NUEVA RUTA: Endpoint para la URL raíz (/)
@app.route('/')
def home():
    """Endpoint para la raíz del sitio, útil para comprobaciones de estado."""
    return "Backend del laboratorio de QRphishing está funcionando correctamente."

@app.route('/api/track-visit', methods=['POST'])
def track_visit():
    """Endpoint para rastrear visitas a la página"""
    data = load_data()
    
    visit_info = {
        'timestamp': datetime.now().isoformat(),
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
        'referrer': request.headers.get('Referer'),
        'device_info': request.json
    }
    
    data['visits'].append(visit_info)
    save_data(data)
    
    return jsonify({'status': 'ok'})

@app.route('/api/track-submission', methods=['POST'])
def track_submission():
    """Endpoint para rastrear envíos de formulario"""
    data = load_data()
    
    submission_info = {
        'timestamp': datetime.now().isoformat(),
        'ip': request.remote_addr,
        'email': request.json.get('email', ''),
        'password_length': len(request.json.get('password', '')),
        'device_info': request.json.get('device_info', {})
    }
    
    data['submissions'].append(submission_info)
    save_data(data)
    
    return jsonify({'status': 'ok'})

@app.route('/admin/stats')
def show_stats():
    """Dashboard para ver estadísticas durante la presentación"""
    data = load_data()
    
    stats_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Demo Stats - Live</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .stat-box {{ 
                background: #f0f0f0; 
                padding: 20px; 
                margin: 10px 0; 
                border-radius: 5px; 
            }}
            .number {{ font-size: 2em; color: #e74c3c; font-weight: bold; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>🎯 Demo QRphishing - Estadísticas en Vivo</h1>
        
        <div class="stat-box">
            <h2>📊 Resumen</h2>
            <p>Visitantes totales: <span class="number">{len(data['visits'])}</span></p>
            <p>Formularios enviados: <span class="number">{len(data['submissions'])}</span></p>
            <p>Tasa de conversión: <span class="number">{(len(data['submissions'])/max(len(data['visits']),1)*100):.1f}%</span></p>
        </div>
        
        <div class="stat-box">
            <h2>📱 Últimas Víctimas</h2>
            <table>
                <tr>
                    <th>Hora</th>
                    <th>Email</th>
                    <th>Dispositivo</th>
                </tr>
    """
    
    # Mostrar últimas 10 submissions
    for submission in data['submissions'][-10:]:
        timestamp = datetime.fromisoformat(submission['timestamp']).strftime('%H:%M:%S')
        email = submission['email'][:20] + '...' if len(submission['email']) > 20 else submission['email']
        device = submission.get('device_info', {}).get('deviceType', 'Unknown')
        
        stats_html += f"""
                <tr>
                    <td>{timestamp}</td>
                    <td>{email}</td>
                    <td>{device}</td>
                </tr>
        """
    
    stats_html += """
            </table>
        </div>
        
        <p><em>Página se actualiza automáticamente cada 5 segundos</em></p>
    </body>
    </html>
    """
    
    return stats_html

if __name__ == '__main__':
    print("🚀 Iniciando servidor de analytics para demo...")
    print("📊 Stats disponibles en: http://localhost:5000/admin/stats")
    print("⚠️  Recuerda: Solo para fines educativos!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
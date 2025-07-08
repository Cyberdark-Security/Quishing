// Importa el conector de la base de datos
import { Pool } from 'pg';

// Crea una nueva instancia de conexión usando la variable de entorno que guardaste en Vercel
const pool = new Pool({
  connectionString: process.env.POSTGRES_URL,
  ssl: {
    rejectUnauthorized: false // Requerido para conexiones a Neon
  }
});

// Esta es la función principal que Vercel ejecutará
export default async function handler(request, response) {
  if (request.method !== 'POST') {
    return response.status(405).json({ message: 'Método no permitido' });
  }

  try {
    // Inserta un nuevo registro en la tabla de visitas
    await pool.query('INSERT INTO visits (visit_time) VALUES (NOW())');
    
    // Responde al frontend que todo salió bien
    response.status(200).json({ message: 'Visita registrada' });
  } catch (error) {
    console.error('Error en la base de datos:', error);
    response.status(500).json({ message: 'Error interno del servidor' });
  }
}
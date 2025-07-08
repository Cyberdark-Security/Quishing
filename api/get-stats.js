import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.POSTGRES_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

export default async function handler(request, response) {
  try {
    // Ejecuta todas las consultas a la vez para mayor eficiencia
    const [visitsResult, submissionsResult, latestSubmissionsResult] = await Promise.all([
      pool.query('SELECT COUNT(*) FROM visits'),
      pool.query('SELECT COUNT(*) FROM submissions'),
      pool.query('SELECT email, device_info, timestamp FROM submissions ORDER BY timestamp DESC LIMIT 10')
    ]);

    // Extrae los resultados
    const totalVisits = parseInt(visitsResult.rows[0].count, 10);
    const totalSubmissions = parseInt(submissionsResult.rows[0].count, 10);
    const latestSubmissions = latestSubmissionsResult.rows;

    // Construye el objeto JSON de respuesta
    const stats = {
      totalVisits,
      totalSubmissions,
      latestSubmissions
    };

    // Devuelve los datos en formato JSON
    response.status(200).json(stats);

  } catch (error) {
    console.error('Error al obtener estadísticas:', error);
    response.status(500).json({ message: 'Error al obtener estadísticas' });
  }
}
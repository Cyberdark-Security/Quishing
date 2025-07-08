import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.POSTGRES_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

export default async function handler(request, response) {
  try {
    const [visitsResult, submissionsResult, latestSubmissionsResult] = await Promise.all([
      pool.query('SELECT COUNT(*) FROM visits'),
      pool.query('SELECT COUNT(*) FROM submissions'),
      // --- CORRECCIÓN AQUÍ: Se eliminó "LIMIT 10" para obtener todos los registros ---
      pool.query('SELECT email, timestamp FROM submissions ORDER BY timestamp DESC')
    ]);

    const totalVisits = parseInt(visitsResult.rows[0].count, 10);
    const totalSubmissions = parseInt(submissionsResult.rows[0].count, 10);
    const latestSubmissions = latestSubmissionsResult.rows;

    const stats = {
      totalVisits,
      totalSubmissions,
      latestSubmissions
    };

    response.status(200).json(stats);

  } catch (error) {
    console.error('Error al obtener estadísticas:', error);
    response.status(500).json({ message: 'Error al obtener estadísticas' });
  }
}
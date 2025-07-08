import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.POSTGRES_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

export default async function handler(request, response) {
  if (request.method !== 'POST') {
    return response.status(405).json({ message: 'Método no permitido' });
  }

  // Aunque el frontend envíe más datos, solo extraemos los que necesitamos
  const { email, scenario } = request.body;

  try {
    // ---- CAMBIO IMPORTANTE ----
    // Se eliminan 'password' y 'device_info' de la consulta SQL.
    const query = 'INSERT INTO submissions (email, scenario) VALUES ($1, $2)';
    
    // ---- CAMBIO IMPORTANTE ----
    // El array de valores ahora solo contiene las dos variables que vamos a guardar.
    const values = [email, scenario];
    
    await pool.query(query, values);

    response.status(200).json({ message: 'Datos guardados correctamente' });
  } catch (error) {
    console.error('Error en la base de datos:', error);
    response.status(500).json({ message: 'Error interno del servidor' });
  }
}
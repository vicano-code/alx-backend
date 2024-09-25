import { createClient, print } from "redis";

const client = createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err}`))
  .on('connect', () => console.log('Redis client connected to the server'));

// Set a new value in Redis for a given school name
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, print);
}

// Get the value of a given school name from Redis and log it to the console
function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, value) => {
    if (err) {
      console.log(`Error getting value for ${schoolName}: ${err}`);
    } else {
      console.log(value); // Log the value retrieved from Redis
    }
  });
}

// Test the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

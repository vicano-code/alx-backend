import { createClient, print } from 'redis';

const client = createClient()
  .on('error', (err) => console.log(`Redis client not connected to the server: ${err}`))
  .on('connect', () => console.log('Redis client connected to the server'));

function setHolbertonSchools() {
  client.hset('HolbertonSchools', 'Portland', 50, print);
  client.hset('HolbertonSchools', 'Seattle', 80, print);
  client.hset('HolbertonSchools', 'New York', 20, print);
  client.hset('HolbertonSchools', 'Bogota', 20, print);
  client.hset('HolbertonSchools', 'Cali', 40, print);
  client.hset('HolbertonSchools', 'Paris', 2, print);
}

// get all values
function displayHolbertonSchools() {
  client.hgetall('HolbertonSchools', (err, result) => {
    if (err) {
      console.log(`Error retrieving HolbertonSchools: ${err}`);
    } else {
      console.log(result); // Log the entire hash object
    }
  });
}

// Set the HolbertonSchools hash values
setHolbertonSchools();

// Display the HolbertonSchools hash values
displayHolbertonSchools();

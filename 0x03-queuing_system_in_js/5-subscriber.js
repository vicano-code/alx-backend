import { createClient, print } from 'redis';

const client = createClient()
  .on('error', (err) => console.log(`Redis client not connected to the server: ${err}`))
  .on('connect', () => console.log('Redis client connected to the server'));

// Subscribe to the 'holberton school channel'
client.subscribe('holberton school channel');

// Set up a message event listener
client.on('message', (channel, message) => {
  console.log(`${message}`);

  if (message === 'KILL_SERVER') {
    client.unsubscribe('holberton school channel');
    client.quit();
  }
});

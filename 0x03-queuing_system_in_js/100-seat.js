import { createClient } from "redis";
import { promisify } from "util";
import kue from "kue";
const express = require('express');

// Create a client to connect to the Redis server
const client = createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err}`))
  .on('connect', () => console.log('Redis client connected to the server'));

// reserve seat(s)
function reserveSeat(number) {
  client.set(available_seats, number);
}

// Get the current available seats
async function getCurrentAvailableSeats() {
  const getAsync = promisify(client.get).bind(client);
  try {
    const value = await getAsync(available_seats);
    return value;
  } catch (err) {
    console.log(`Error getting value for ${available_seats}: ${err}`);
    return null;
  }
}

// Create a Kue queue
const queue = kue.createQueue();

// Create an express server listening on the port 1245.
const app = express();

// Route for returning the number of seat available
app.get('/available_seats', (req, res) => {
  res.json()
})
const { createClient, print } = require("redis");
const { promisify } = require("util");
const kue = require("kue");
const express = require('express');

// Create a client to connect to the Redis server
const client = createClient()
  .on('error', err => console.log(`Redis client not connected to the server: ${err}`))
  .on('connect', () => console.log('Redis client connected to the server'));

// Promisify Redis get operation
const getAsync = promisify(client.get).bind(client);

// Create a Kue queue
const queue = kue.createQueue();

// Initialize the number of available seats and reservationEnabled
let reservationEnabled = true;

// function to set number of available seats
function reserveSeat(number) {
  client.set('available_seats', number, print);
}

// Get the current available seats from Redis
async function getCurrentAvailableSeats() {
  try {
    const seats = await getAsync('available_seats');
    return seats ? parseInt(seats) : 0;
  } catch (err) {
    console.log(`Error fetching available seats: ${err}`);
    return 0;
  }
}

// Launch the application by setting available seats to 50
reserveSeat(50);

// Create an express server listening on the port 1245.
const app = express();
const PORT = 1245;

// Endpoint to return the number of available seats and whether reservation is enabled
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();

  res.json({
    numberOfAvailableSeats: availableSeats
  });
});

// Process the queue to reserve a seat asynchronously
queue.process('reserve_seat', async (job, done) => {
  const availableSeats = await getCurrentAvailableSeats();

  if (availableSeats <= 0) {
    reservationEnabled = false;
    return done(new Error('Not enough seats available'));
  }

  // Decrease available seats by 1 and update Redis
  reserveSeat(availableSeats - 1);

  if (availableSeats - 1 === 0) {
    reservationEnabled = false;
  }

  done();
});

// Endpoint to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({status: 'Reservation are blocked'});
  }

  // Create and queue a job
  const job = queue.create('reserve_seat')
    .save((err) => {
      if (err) {
        return res.json({status: 'Reservation failed'});
      }
      res.json({status: 'Reservation in process'});
    })
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errMessage}`)
  });
})

// Endpoint to process the reserve_seat queue
app.get('/process', async (req, res) => {
  app.get('/process', (req, res) => {
    res.json({ status: 'Queue processing' });
  
    // Process the queue for 'reserve_seat'
    queue.process('reserve_seat', async (job, done) => {
      const availableSeats = await getCurrentAvailableSeats();
  
      if (availableSeats <= 0) {
        reservationEnabled = false;
        return done(new Error('Not enough seats available'));
      }
  
      // Decrease available seats by 1 and update Redis
      reserveSeat(availableSeats - 1);
  
      if (availableSeats - 1 === 0) {
        reservationEnabled = false;
      }
  
      done();
    });
  });
})

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running and listening on port ${PORT}`);
});
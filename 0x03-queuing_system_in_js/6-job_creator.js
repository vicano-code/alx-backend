import kue from 'kue';

// create a Kue queue
const queue = kue.createQueue();

// Create an object containing the job data
const jobData = {
  phoneNumber: '4153518780',
  message: 'This is the code to verify your account',
}

// Create a queue
const job = queue.create('push_notification_code', jobData)
  .save((err) => {
    if (err) {
      console.error(`Notification job failed to create: ${err}`);
    } else {
      console.log(`Notification job created: ${job.id}`)
    }
  })

// Handle job completion
job.on('complete', () => {
  console.log('Notification job completed');
});

// Handle job failure
job.on('failed', () => {
  console.log('Notification job failed');
});

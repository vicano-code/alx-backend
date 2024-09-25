import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue();

function sendNotification(phoneNumber, message) {
  console.log(`sending notification to ${phoneNumber}, with message: ${message}`)
}

// Process function for the 'push_notification_code' queue
queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;

  // Call the sendNotification function with job data
  sendNotification(phoneNumber, message);

  // Indicate that the job is done
  done();
});

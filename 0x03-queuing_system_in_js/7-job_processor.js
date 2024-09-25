import kue from 'kue';

const blackListedNumbers = [4153518780, 4153518781];

const queue = kue.createQueue();

function sendNotification(phoneNumber, message, job, done) {
  // Track the progress
  job.progress(0, 100);

  if (blackListedNumbers.includes(phoneNumber)) {
    done(new Error(`Phone number ${phoneNumber} is blacklisted`));
  } else {
    // Track progress to 50%
    job.progress(50, 100)
    // Log the notification message to console
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    // Complete the job successfully
    done();
  }
}

// process job of the queue push_notification_code_2 with two jobs at a time
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  // Call the sendNotification function
  sendNotification(phoneNumber, message, job, done);
});

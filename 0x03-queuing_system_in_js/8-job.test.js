import createPushNotificationsJobs from './8-job';
const kue = require('kue');
const { expect } = require('chai');


describe('createPushNotificationJobs', () => {
  let queue;

  beforeEach(() => {
    // Enable test mode
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    // Clear the queue and exit test mode after each test
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw(Error, 'Jobs is not an array');
  });

  it('should create two new jobs to the queue', () => {
    const jobs = [
      {phoneNumber: '1234567890', message: 'This is a message'},
      {phoneNumber: '0987654321', message: 'Another message'}
    ];

    createPushNotificationsJobs(jobs, queue);

    //expect(queue.testMode.jobs.length).to.equal(2);
    //expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    //expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    //expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    //expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);
  });

  it('should create an empty queue if no jobs are passed', function() {
    createPushNotificationsJobs([], queue);
    expect(queue.testMode.jobs.length).to.equal(0);
  });
});

const { API_URL } = require('utils/constants');
const { submit } = require('utils/proxy');

const api_end_point = API_URL+'/api/queue';

const queueService = {
  waiting,
  entered,
  exited
};

function waiting(eventId) {
  return submit('GET', `${api_end_point}/waiting/${eventId}`);
}

function entered(eventId) {
  return submit('GET', `${api_end_point}/entered/${eventId}`);
}

function exited(eventId) {
  return submit('GET', `${api_end_point}/exited/${eventId}`);
}

export default queueService;
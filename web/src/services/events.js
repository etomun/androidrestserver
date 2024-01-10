import { API_URL } from 'utils/constants';
import { submit } from 'utils/proxy';

const api_end_point = API_URL+'/api/event';

const eventsService = {
  list,
};

function list() {
  return submit('GET', api_end_point);
}

export default eventsService;
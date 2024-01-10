import { faDoorOpen, faPersonBooth, faUserFriends } from '@fortawesome/free-solid-svg-icons';

export const API_URL = window.origin;
export const WS_URL = process.env.NODE_ENV === 'production' ? `${window.origin}` : 'http://192.168.18.12:8888';

export const eventStatus = {
  notStarted: 'NOT_STARTED',
  started: 'STARTED'
};

export const queueStatus = {
  waiting: {
    name: 'waiting',
    icon: faUserFriends
  },
  entered: {
    name: 'entered',
    icon: faPersonBooth
  },
  exited: {
    name: 'exited',
    icon: faDoorOpen
  }
};

export const img = {
  icMale: require('assets/img/ic_male.svg').default,
  icFemale: require('assets/img/ic_female.svg').default,
  icVerified: require('assets/img/ic_verified.svg').default
};
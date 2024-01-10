export const API_URL = window.origin;
export const WS_URL = process.env.NODE_ENV === 'production' ? `${window.origin}` : 'http://192.168.18.12:8888';

export const eventStatus = {
  notStarted: 'NOT_STARTED',
  started: 'STARTED'
};

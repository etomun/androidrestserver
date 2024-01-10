import { toast } from 'react-toastify';

export const submit = (requestType, url, data = {}, requestOptions = {}) => {
  return new Promise((resolve, reject) => {
    if (requestType === 'GET') {
      const newApiUrl = new URL(url);
      Object.keys(data).forEach(key => {
        newApiUrl.searchParams.append(key, data[key]);
      });
      fetch(newApiUrl, Object.assign({method: 'GET'}, requestOptions))
        .then(response => {
          if(response.status === 200){
            response.json().then(
              resp => {
                if (resp.status_code === 200) {
                  resolve(resp.data);
                } else {
                  if (resp.message) {
                    toast.error(resp.message);
                  }
                }
              }
            );
          }
          else {
            toast.error(response.statusText);
            // reject(response);
          }
        })
        .catch(error => console.log('error :>> ', error));
    }
  });
};

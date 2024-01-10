import { faClock, faIdCard } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import moment from 'moment';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { queueService } from 'services';
import { WS_URL, img, queueStatus } from 'utils/constants';
import { isMobile } from 'utils/utils';
import Line from './components/line';

const Queue = () => {
  const { id } = useParams();

  const [queueList, setQueueList] = useState([]);
  const [menu] = useState(queueStatus?.waiting?.name);

  useEffect(() => {
    getQueueList(2);
  }, [menu]);

  useEffect(() => {
    const ws = new WebSocket(`${WS_URL.replace('http', 'ws')}/api/queue/ws/${id}`);
    
    ws.onopen = () => {
      console.log('connection open');
      ws.addEventListener('message', ({data}) => {
        const res = JSON.parse(data);
        if(res?.event_id){
          getQueueList(res?.message_code);
        }
      });
    };

    ws.onclose = () => {
      ws.removeEventListener('message', () => {
        console.log('connection close :>> ');
      });
    };
    return () => {
      console.log('ws return :>> ', ws.readyState);
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close();
      }
    };
  }, [id]);

  const getQueueList = (status) => {
    if(menu){
      queueService[menu](id).then(
        resp => {
          if(status === 2){
            const firstQueue = document.querySelector('.animate:first-child');
            if(firstQueue){
              firstQueue.classList.add('animated-slide-gone');
            }
            const secondQueue = document.querySelector('.animate:nth-child(2)');
            if(secondQueue){
              secondQueue.classList.add('animated-fade-out');
            }

            setTimeout(() => {
              if(firstQueue){
                firstQueue.classList.remove('animated-slide-gone');
              }
              if(secondQueue){
                secondQueue.classList.remove('animated-fade-out');
              }

              setQueueList(resp ?? []);
    
              if(firstQueue){
                firstQueue.classList.add('animated-slide-up');
              }
              if(secondQueue){
                secondQueue.classList.add('animated-fade-in');
              }
            
              setTimeout(() => {
                if(firstQueue){
                  firstQueue.classList.remove('animated-slide-up');
                }
                if(secondQueue){
                  secondQueue.classList.remove('animated-fade-in');
                }
              }, 1000);
            }, 500);
          }else{
            setQueueList(resp ?? []);
          }
        }
      );
    }
  };

  const firstCard = ({ name, id, village, date_queued, gender }) => {
    return (
      <div className={`content ${isMobile() ? 'is-normal' : 'is-medium'}`}>
        <div style={{textAlign: 'center'}}>
          <div className='block-text'>
            <div style={{display: 'flex', alignItems: 'flex-start', justifyContent: 'center'}}>
              <h1 className='is-uppercase' style={{fontSize: isMobile() ? '2rem' : 70, color: 'white', lineHeight: 1}} >{name}</h1>
              <img alt="verified" src={img.icVerified} style={{width: isMobile() ? 15 : 30, marginLeft: 5}} />
              <img alt="gender" src={gender === 'male' ? img.icMale : img.icFemale} style={{width: isMobile() ? 14 : 28, backgroundColor: gender === 'male' ? '#BECBD4' : '#B794A8', borderRadius: '50%', marginLeft: 5}} />
            </div>
            <h3 style={{marginTop: 0, fontSize: isMobile() ? '1.25rem' : '3 rem', color: '#f5f5f5'}}>{village}</h3>
          </div>
          <div className='block-text'>
            <div>
              <Line color='#a9b9c5' />
            </div>
          </div>
          <div className='block-text' style={{display: 'flex', justifyContent: 'center', flexWrap: 'wrap'}}>
            <p style={{color: '#B9B3C7', marginRight: 20}}>
              <FontAwesomeIcon icon={faIdCard} style={{marginRight: 10}} />
              <span>{id}</span>
            </p>
            <p style={{color: '#B9B3C7'}}>
              <FontAwesomeIcon icon={faClock} style={{marginRight: 10}} />
              <span>{moment(date_queued).format('DD MMM YYYY (HH:mm)')}</span>
            </p>
          </div>
        </div>
      </div>
    );
  };
  
  const listCard = ({ name, id, village, gender }) => {
    return (
      <div className={`content ${isMobile() ? 'is-normal' : 'is-medium'}`}>
        <div style={{display: 'flex', color: 'black', textAlign: 'center', alignItems: 'center'}}>
          <div>
            <div className='block-text'>
              <h1 className='is-uppercase' style={{fontSize: isMobile() ? '1rem' : '1.5rem'}} >{`${name} - ${id}`}</h1>
            </div>
            <div className='block-text'>
              <p>{village}</p>
            </div>
          </div>
        </div>
      </div>
    );
  };
  
  
  return ( <div className='container is-fluid'>
    {queueList.length > 0 ? (
      queueList.map((item, index) => {
        const firstWaitingQueue = index === 0 && menu === queueStatus.waiting.name;
        const data = {
          name: item?.member?.name,
          id: item?.member?.unique_code,
          village: item?.member?.address?.village,
          date_queued: item?.date_queued,
          gender: item?.member?.gender
        };
        return (
          <div className="block animate" key={index}>
            <div className='card custom-shadow' style={{borderRadius: 16, backgroundImage: firstWaitingQueue ? 'linear-gradient(-225deg, #295270 0%, #524175 100%)' : ''}}>
              <div className='card-content' style={{minHeight: firstWaitingQueue ? '40vh' : 'auto', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: firstWaitingQueue ? '1rem' : '0.8rem'}}>
                {firstWaitingQueue ? firstCard(data) : listCard(data)}
              </div>
            </div>
          </div>
        );
      })
    ):(
      <div style={{display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center', padding: 20, textAlign: 'center'}}>
        <div className='is-size-1 is-bold is-italic has-text-danger-dark'>Belum ada antrian</div>
      </div>
    )}
  </div> );
};
 
export default Queue;
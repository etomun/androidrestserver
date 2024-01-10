import { faClock, faIdCard } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import moment from 'moment';
import { useEffect, useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import { queueService } from 'services';
import { WS_URL, img, queueStatus } from 'utils/constants';
import { isMobile } from 'utils/utils';
import Line from './components/line';
import SideMenu from './side_menu';

const FirstCard = ({ name, id, village, date_queued, gender }) => {
  return (
    <div className={`content ${isMobile() ? 'is-normal' : 'is-medium'}`}>
      <div style={{textAlign: 'center'}}>
        <div className='block-text'>
          <div style={{display: 'flex', alignItems: 'flex-start', justifyContent: 'center'}}>
            <h1 className='is-uppercase' style={{fontSize: isMobile() ? '2rem' : 70, color: 'white', lineHeight: 1}} >{name}</h1>
            <img alt="verified" src={img.icVerified} style={{width: isMobile() ? 15 : 30, marginLeft: 5}} />
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

export const ListCard = ({ name, id, village, status, index }) => {
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
          {status && (
            <div className='block-text'>
              <p style={{marginBottom: 0}}>Status : &nbsp;
                {status.toLowerCase() === queueStatus?.queued?.name && 'Dalam antrian'}
                {status.toLowerCase() === queueStatus?.entered?.name && 'Masuk'}
                {status.toLowerCase() === queueStatus?.exited?.name && 'Keluar'}
              </p>
              {index!== null && (
                <p className='has-text-danger is-bold'>
                  Menunggu {index}
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const Queue = () => {
  const { id } = useParams();
  const { state } = useLocation();

  const [queueList, setQueueList] = useState([]);
  const [menu, setMenu] = useState(queueStatus?.waiting?.name);

  useEffect(() => {
    getQueueList(null);
  }, [menu]);

  useEffect(() => {
    const ws = new WebSocket(`${WS_URL.replace('http', 'ws')}/api/queue/ws/${id}`);
    
    ws.onopen = () => {
      console.log('connection open');
      ws.addEventListener('message', ({data}) => {
        const res = JSON.parse(data);
        console.log('res ws message :>> ', res);
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
        resp => onSetAnimationData(status?.toLowerCase() === queueStatus?.entered?.name, resp)
      );
    }
  };

  const onSetAnimationData = (hasAnimate, data) => {
    if(hasAnimate){
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

        console.log('data true :>> ', data);
        setQueueList(data ?? []);

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
      console.log('data false :>> ', data);
      setQueueList(data ?? []);
    }
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
          <div className={`block animate ${menu !== queueStatus?.waiting?.name ? 'animated-fade-in' : ''}`} key={index}>
            <div className='card custom-shadow' style={{borderRadius: 16, backgroundImage: firstWaitingQueue ? 'linear-gradient(-225deg, #295270 0%, #524175 100%)' : ''}}>
              <div className='card-content' style={{minHeight: firstWaitingQueue ? '40vh' : 'auto', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: firstWaitingQueue ? '1rem' : '0.8rem'}}>
                {firstWaitingQueue ? <FirstCard {...data} /> : <ListCard {...data} />}
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
    <SideMenu  
      data={state?.event}
      menu={menu} 
      onClickMenu={setMenu}
    />
  </div> );
};
 
export default Queue;
import moment from 'moment';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Slider from 'react-slick';
import { eventsService } from 'services';
import { eventStatus } from 'utils/constants';
import { getRandomGradient } from 'utils/utils';
import Line from './components/line';

const settingSlider = {
  dots: true,
  infinite: true,
  speed: 500,
  slidesToShow: 1,
  slidesToScroll: 1,
  arrows: false
};

const Events = () => {
  const navigate = useNavigate();

  const [eventList, setEventList] = useState([]);
  const [detailEvent, setDetailEvent] = useState(null);

  useEffect(() => {
    eventsService.list().then((resp) => {
      setEventList(resp ?? []);
      if(resp.length > 0){
        setDetailEvent(resp[0]);
      }
    });
  }, []);

  return (
    <div className="container is-fullhd">
      <div className="block" style={{marginBottom: '2rem'}}>
        <Slider {...settingSlider}
          afterChange={(index) => setDetailEvent(eventList?.[index])}
        >
          {eventList.map((item, index) => (
            <div className='block' key={index}>
              <div className="card" style={{backgroundImage: getRandomGradient()}}>
                <div className="card-content" style={{ minHeight: 250, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <div className="content is-medium">
                    <h1>{item.name}</h1>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </Slider>
      </div>
      {detailEvent && (
        <div className='columns box-shadow' style={{height: 'calc(100vh - 250px)'}}>
          <div className='column is-7' style={{padding: '2rem'}}>
            <div className='block'>
              <div className='content'>
                {detailEvent?.has_queue && detailEvent?.status === eventStatus.started && (
                  <button className='button is-dark is-medium is-uppercase has-text-weight-bold	'
                    onClick={() => navigate(`/queue/${detailEvent?.id}`, {state: {event: detailEvent}})}
                  >Lihat antrian</button>
                )}
                <h1>Description</h1>
                <p>{detailEvent?.description}</p>
              </div>
            </div>
          </div>
          <div className='column is-5' style={{padding: '2rem', position: 'relative'}}>
            <Line coordinat='v' color='#dcdcdc' />
            <div className='block'>
              <div className='content'>
                {detailEvent?.status === eventStatus.notStarted && (
                  <h4 style={{backgroundColor: '#b93241', padding: 10, borderRadius: 5, color: 'white !important'}}>
                    Event will start {moment(detailEvent?.expected_start_date).startOf('day').fromNow()}
                  </h4>
                )}
                <br/>
                <h5>Start Date:</h5>
                <p>{moment(detailEvent?.expected_start_date).format('LLL') }</p>
                <h5>End Date:</h5>
                <p>{moment(detailEvent?.expected_end_date).format('LLL')}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Events;

import { useEffect, useRef, useState } from 'react';
import { useOutsideClick } from 'utils/hooks';
import { isMobile } from 'utils/utils';
import Line from './components/line';
import { queueStatus } from 'utils/constants';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBars, faClose, faSearch } from '@fortawesome/free-solid-svg-icons';
import { queueService } from 'services';
import { useParams } from 'react-router-dom';
import Modal from './components/modal';
import { ListCard } from './queue';

const SideMenu = ({ data, menu, onClickMenu }) => {
  const { id } = useParams();
  const sideRef = useRef(null);
  const [isShow, setIsShow] = useState(false);
  const [search, setSearch] = useState('');
  const [allQueue, setAllQueue] = useState([]);
  const [filterQueue, setFilterQueue] = useState([]);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    if(isShow){
      queueService.all(id).then(
        resp => setAllQueue(resp ?? [])
      );
    }
  }, [isShow]);

  useOutsideClick(sideRef, (e) => {
    if(!e.target.closest('button#menu-button') && !e.target.closest('div#modal')){
      setIsShow(false);
      setSearch('');
    }
  });

  const onSearch = (e) => {
    e.preventDefault();
    let result = allQueue.filter(x => x?.member?.name?.toLowerCase().includes(search?.toLowerCase()));
    result.forEach((item, index) => {
      const queueList = allQueue.filter(x => x?.last_status?.toLowerCase() === queueStatus?.queued?.name);
      result[index] = {
        ...item,
        index_queued: item.last_status?.toLowerCase() === queueStatus?.queued?.name ? queueList.map(x => x?.member?.unique_code).indexOf(item?.member?.unique_code) : null
      };
    });
    setFilterQueue(result);
    setShowModal(true);
  };
  
  return (
    <>
      <div style={{position: 'fixed', bottom: 30, right: 30, zIndex: 1}}>
        <button id="menu-button" className='button is-danger is-rounded has-shadow' style={{width: 50, height: 50}} 
          onClick={() => {
            if(isShow){
              setSearch('');
            }
            setIsShow(!isShow);
          }}
        >
          <FontAwesomeIcon icon={isShow ? faClose : faBars} style={{fontSize: 20}}/>
        </button>
      </div>
      <div ref={sideRef} className={`side-navbar-right ${isShow ? 'open' : ''}`}>
        <div className='block' style={{padding: '50px 20px 0px 20px'}}>
          <div className={`content ${isMobile() ? 'is-small' : 'is-normal'}`}>
            <h1 className='has-text-white'>{data?.name}</h1>
            <p>{data?.description}</p>
          </div>
        </div>
        <div style={{padding: '0px 10px'}}>
          <Line color='#404040' />
        </div>
        <div style={{padding: '20px 10px'}}>
          <form onSubmit={onSearch} >
            <div className='field'>
              <div className='control has-icons-left'>
                <input className='input dark-input' type="text" placeholder='Search name' 
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
                <FontAwesomeIcon className='icon is-small is-left dark-icon' icon={faSearch} size="2xs" style={{top: '7.5px', left: '7.5px', width: 20}} />
              </div>
            </div>
          </form>
        </div>
        <div style={{padding: '10px 10px'}}>
          <span>Menu</span>
        </div>
        <div className='block'>
          {Object.keys(queueStatus).map((item, index) => {
            if(item !== queueStatus?.queued?.name){
              return (
                <div className={`menu-list ${menu === queueStatus[item].name ? 'active' : '' }`} key={index} onClick={() => onClickMenu(queueStatus[item].name)}>
                  <div style={{marginRight: 20}}>
                    <FontAwesomeIcon icon={queueStatus[item].icon} />
                  </div>
                  <div style={{flex: 1}}>
                    <span className='is-capitalized'>{queueStatus[item].name}</span>
                  </div>
                </div>
              );
            }
            return null;
          })}
        </div>
      </div>
      <Modal 
        active={showModal}
        onClose={() => setShowModal(false)}
      >
        <div style={{position: 'absolute', right: 20, top: 20}} >
          <a onClick={() => setShowModal(false)}>
            <FontAwesomeIcon icon={faClose} />
          </a>
        </div>
        <div style={{marginTop: 25}}>
          {filterQueue.length > 0 ? (
            filterQueue.map((item, index) => (
              <div className='block animated-fade-in' key={index}>
                <div className='card custom-shadow'>
                  <div className='card-content' style={{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                    <ListCard 
                      name={item?.member?.name}
                      id={item?.member?.unique_code}
                      village={item?.member?.address?.village}
                      status={item?.last_status}
                      index={item?.index_queued}
                    />
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className='has-text-danger is-italic is-bold'>Data not found</div>
          )}
        </div>
      </Modal>
    </>
  );
};

export default SideMenu;
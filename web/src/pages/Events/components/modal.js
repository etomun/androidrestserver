const Modal = ({active, onClose, children, title}) => {
  return ( 
    <div id="modal" className={`modal ${active && 'is-active'}`}>
      <div className="modal-background" onClick={onClose}></div>
      <div className="modal-card">
        <section className="modal-card-body">
          {children}
        </section>
      </div>
    </div>
  );
};
 
export default Modal;
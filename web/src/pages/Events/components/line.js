const Line = ({ color, coordinat = 'h' }) => {
  let styles = {backgroundColor: color};
  if(coordinat === 'v'){
    styles = {...styles, position: 'absolute', top: 0, left: 0, height: '-webkit-fill-available', width: 1};
  }
  if(coordinat === 'h'){
    styles = {...styles, width: '100%', height: 1};
  }
  return ( 
    <hr style={styles} />
  );
};
 
export default Line;
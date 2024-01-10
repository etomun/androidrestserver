export const getRandomGradient = () => {
  const colorArr = [
    'linear-gradient(-225deg, #7de2fc 0%, #b9b6e5 100%)',
    'linear-gradient(-225deg, #FFC857 0%, #C11D38 100%)',
    'linear-gradient(-225deg, #D3D3D3 0%, #1DD1A1 100%)',
    'linear-gradient(-225deg, #66B5F6 0%, #BFE299 100%)',
    'linear-gradient(-225deg, #FFA69E  0%, #861657 100%)',
  ];

  return colorArr[Math.floor(Math.random() * colorArr.length)];
};

export const isMobile = () => {
  return window.innerWidth <= 768;
};
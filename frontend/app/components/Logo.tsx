import spyImage from './spy.png';

const Logo = () => {
  return (
    <div className="opacity-60 w-64 h-64">
      <img 
        src={spyImage.src} 
        alt="Spy Symbol" 
        className="w-full h-full object-contain"
      />
    </div>
  );
};

export default Logo;

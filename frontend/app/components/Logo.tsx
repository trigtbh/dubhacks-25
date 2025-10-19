import spyImage from './spy2.png';

const Logo = () => {
  return (
    <div className="brightness-200 w-64 h-64">
      <img 
        src={spyImage.src} 
        alt="Spy Symbol" 
        className="w-full h-full object-contain"
      />
    </div>
  );
};

export default Logo;

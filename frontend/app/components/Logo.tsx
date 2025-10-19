import spyImage from '../assets/spy2.png';

const Logo = () => {
  return (
    <div className="brightness-200 w-64 h-64" style={{
      filter: 'drop-shadow(0 0 20px rgba(51, 255, 102, 0.18)) drop-shadow(0 0 40px rgba(51, 255, 102, 0.09))'
    }}>
      <img 
        src={spyImage.src} 
        alt="Spy Symbol" 
        className="w-full h-full object-contain"
      />
    </div>
  );
};

export default Logo;

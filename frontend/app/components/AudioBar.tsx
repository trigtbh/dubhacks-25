import audioImage from '../assets/audio.png';

const AudioBar = () => {
  return (
    <div className="w-full h-128 flex items-center">
      <img 
        src={audioImage.src} 
        alt="Audio Bar" 
        className="w-full h-full object-contain"
      />
    </div>
  );
};

export default AudioBar;

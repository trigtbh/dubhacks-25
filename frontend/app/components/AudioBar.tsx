'use client';

import { useEffect, useRef, useState } from 'react';

interface AudioBarProps {
  audioFile?: string;
  shouldPlay?: boolean;
}

const AudioBar = ({ audioFile, shouldPlay = false }: AudioBarProps) => {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const animationRef = useRef<number | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const [hasPlayed, setHasPlayed] = useState(false);

  useEffect(() => {
    // Reset hasPlayed when audioFile changes
    setHasPlayed(false);
  }, [audioFile]);

  // Setup audio context and analyser
  useEffect(() => {
    if (audioRef.current && !audioContextRef.current) {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const analyser = audioContext.createAnalyser();
      const source = audioContext.createMediaElementSource(audioRef.current);
      
      analyser.fftSize = 256;
      source.connect(analyser);
      analyser.connect(audioContext.destination);
      
      audioContextRef.current = audioContext;
      analyserRef.current = analyser;
    }
  }, [audioFile]);

  // Visualizer animation
  useEffect(() => {
    const canvas = canvasRef.current;
    const analyser = analyserRef.current;
    
    if (!canvas || !analyser) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const draw = () => {
      animationRef.current = requestAnimationFrame(draw);
      
      analyser.getByteFrequencyData(dataArray);
      
      // Clear with transparent background
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const barWidth = (canvas.width / bufferLength) * 2.5;
      const centerY = canvas.height / 2;
      let barHeight;
      let x = 0;
      
      for (let i = 0; i < bufferLength; i++) {
        barHeight = (dataArray[i] / 255) * (canvas.height / 2) * 0.8;
        
        // Green gradient for top half
        const gradientTop = ctx.createLinearGradient(0, centerY - barHeight, 0, centerY);
        gradientTop.addColorStop(0, '#33ff66');
        gradientTop.addColorStop(1, 'rgba(51, 255, 102, 0.5)');
        
        // Draw top half (growing upward from center)
        ctx.fillStyle = gradientTop;
        ctx.fillRect(x, centerY - barHeight, barWidth, barHeight);
        
        // Green gradient for bottom half (mirrored)
        const gradientBottom = ctx.createLinearGradient(0, centerY, 0, centerY + barHeight);
        gradientBottom.addColorStop(0, 'rgba(51, 255, 102, 0.5)');
        gradientBottom.addColorStop(1, '#33ff66');
        
        // Draw bottom half (growing downward from center)
        ctx.fillStyle = gradientBottom;
        ctx.fillRect(x, centerY, barWidth, barHeight);
        
        x += barWidth + 1;
      }
    };

    draw();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [audioFile]);

  useEffect(() => {
    if (audioFile && shouldPlay && audioRef.current && !hasPlayed) {
      console.log('Attempting to play audio:', audioFile);
      
      // Resume audio context if suspended
      if (audioContextRef.current?.state === 'suspended') {
        audioContextRef.current.resume();
      }
      
      // Reset and play the audio
      audioRef.current.currentTime = 0;
      audioRef.current.play()
        .then(() => {
          console.log('Audio playing successfully:', audioFile);
          setHasPlayed(true);
        })
        .catch((error) => {
          console.error('Audio autoplay prevented:', error);
        });
    }
  }, [audioFile, shouldPlay, hasPlayed]);

  return (
    <div className="relative w-32 h-6 flex items-center justify-center">
      <audio ref={audioRef} src={audioFile || ''} preload="auto" />
      <canvas 
        ref={canvasRef}
        width={256}
        height={96}
        className="w-full h-full"
        style={{ 
          backgroundColor: 'transparent'
        }}
      />
    </div>
  );
};

export default AudioBar;

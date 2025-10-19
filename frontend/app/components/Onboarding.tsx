'use client';

import { useState, useEffect } from 'react';
import { ArrowRight } from 'lucide-react';
import Logo from './Logo';
import AudioBar from './AudioBar';

interface OnboardingProps {
  onComplete: () => void;
}

const Onboarding = ({ onComplete }: OnboardingProps) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [scrambledText, setScrambledText] = useState('');
  const [showUnfreeze, setShowUnfreeze] = useState(false);
  const [showSvg, setShowSvg] = useState(false);
  const [showAudioBar, setShowAudioBar] = useState(false);
  const [showSubtitle, setShowSubtitle] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    secretName: '',
    secondPage: ''
  });

  const targetText = 'U N F R E E Z E';
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()';

  // Scrambling effect
  useEffect(() => {
    if (currentStep === 0) {
      let scrambleCount = 0;
      const maxScrambles = 30; // 3 seconds at 100ms intervals
      
      const scrambleInterval = setInterval(() => {
        setScrambledText(prev => {
          scrambleCount++;
          
          if (scrambleCount >= maxScrambles) {
            clearInterval(scrambleInterval);
            setTimeout(() => {
              setShowUnfreeze(true);
              setTimeout(() => {
                setShowUnfreeze(false);
                setCurrentStep(1);
              }, 2000);
            }, 1000);
            return targetText;
          }
          
          return targetText.split('').map((char, index) => {
            // Gradually reveal more characters as we progress
            const revealThreshold = (scrambleCount / maxScrambles) * targetText.length;
            if (index < revealThreshold) {
              return char;
            }
            return characters[Math.floor(Math.random() * characters.length)];
          }).join('');
        });
      }, 100);

      return () => clearInterval(scrambleInterval);
    }
  }, [currentStep]);

  // SVG and audio bar sequence
  useEffect(() => {
    if (currentStep === 1) {
      setTimeout(() => setShowSvg(true), 500);
      setTimeout(() => setShowAudioBar(true), 1000);
      setTimeout(() => setShowSubtitle(true), 2000);
      setTimeout(() => {
        setShowSubtitle(false);
        setShowForm(true);
      }, 7000);
    }
  }, [currentStep]);

  // Second page sequence
  useEffect(() => {
    if (currentStep === 2) {
      setTimeout(() => setShowSubtitle(true), 500);
      setTimeout(() => {
        setShowSubtitle(false);
        setShowForm(true);
      }, 7000);
    }
  }, [currentStep]);

  // Final UNFREEZE sequence
  useEffect(() => {
    if (currentStep === 3) {
      setTimeout(() => {
        onComplete();
      }, 2000); // Show UNFREEZE for 2 seconds then go to main app
    }
  }, [currentStep]);

  const handleNext = () => {
    if (currentStep === 1) {
      setShowForm(false);
      setCurrentStep(2);
    } else if (currentStep === 2) {
      setShowForm(false);
      setCurrentStep(3);
    } else if (currentStep === 3) {
      onComplete();
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  if (currentStep === 0) {
    return (
      <div className="h-screen flex items-center justify-center px-4" style={{backgroundColor: '#0d0d0d'}}>
        <h1 className="text-4xl font-bold font-mono whitespace-nowrap neon-glow" style={{color: '#33ff66', letterSpacing: '0.1em'}}>
          {scrambledText || 'A B C D E F G H I'}
        </h1>
      </div>
    );
  }

  if (currentStep === 1) {
    return (
      <div className="h-screen relative" style={{backgroundColor: '#0d0d0d'}}>
        {/* Spy symbol at 30% from top */}
        {showSvg && (
          <div className="absolute top-1/3 left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
            <Logo />
          </div>
        )}

        {/* Audio bar on top of spy symbol */}
        {showAudioBar && (
          <div className="absolute top-1/3 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 fade-in">
            <AudioBar />
          </div>
        )}

        {/* Subtitle */}
        {showSubtitle && (
          <div className="absolute bottom-20 left-4 right-4 flex justify-center">
            <div className="typewriter text-lg font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>
              This is mission control.
            </div>
          </div>
        )}

        {/* Form at 30% from bottom */}
        {showForm && (
          <div className="absolute bottom-1/3 left-1/2 transform -translate-x-1/2 translate-y-1/2 fade-in">
            <div className="w-80 p-6 rounded-lg border neon-border" style={{backgroundColor: 'rgba(26, 26, 26, 0.8)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)'}}>
              <h2 className="text-2xl font-bold font-mono mb-4" style={{color: '#33ff66'}}>
                Secret Name:
              </h2>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={formData.secretName}
                  onChange={(e) => handleInputChange('secretName', e.target.value)}
                  className="flex-1 px-3 py-2 rounded border font-mono"
                  style={{backgroundColor: '#0d0d0d', borderColor: 'rgba(51, 255, 102, 0.4)', color: '#33ff66'}}
                  placeholder="Enter your name"
                />
                <button
                  onClick={handleNext}
                  disabled={!formData.secretName.trim()}
                  className="p-2 rounded disabled:opacity-50 transition-all hover:scale-105"
                  style={{backgroundColor: '#2CFF05', color: '#0a0a0a', boxShadow: '0 0 10px rgba(51, 255, 102, 0.4)'}}
                >
                  <ArrowRight size={20} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  if (currentStep === 2) {
    return (
      <div className="h-screen relative" style={{backgroundColor: '#0d0d0d'}}>
        {/* Spy symbol at 30% from top */}
        <div className="absolute top-1/3 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <Logo />
        </div>

        {/* Audio bar on top of spy symbol */}
        <div className="absolute top-1/3 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10">
          <AudioBar />
        </div>

        {/* Subtitle */}
        {showSubtitle && (
          <div className="absolute bottom-20 left-4 right-4 flex justify-center">
            <div className="typewriter text-lg font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>
              this is another page
            </div>
          </div>
        )}

        {/* Form at 30% from bottom */}
        {showForm && (
          <div className="absolute bottom-1/3 left-1/2 transform -translate-x-1/2 translate-y-1/2 fade-in">
            <div className="w-80 p-6 rounded-lg border neon-border" style={{backgroundColor: 'rgba(26, 26, 26, 0.8)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)'}}>
              <h2 className="text-2xl font-bold font-mono mb-4" style={{color: '#33ff66'}}>
                second page
              </h2>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={formData.secondPage}
                  onChange={(e) => handleInputChange('secondPage', e.target.value)}
                  className="flex-1 px-3 py-2 rounded border font-mono"
                  style={{backgroundColor: '#0d0d0d', borderColor: 'rgba(51, 255, 102, 0.4)', color: '#33ff66'}}
                  placeholder="Enter something"
                />
                <button
                  onClick={handleNext}
                  disabled={!formData.secondPage.trim()}
                  className="p-2 rounded disabled:opacity-50 transition-all hover:scale-105"
                  style={{backgroundColor: '#2CFF05', color: '#0a0a0a', boxShadow: '0 0 10px rgba(51, 255, 102, 0.4)'}}
                >
                  <ArrowRight size={20} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  if (currentStep === 3) {
    return (
      <div className="h-screen flex items-center justify-center px-4" style={{backgroundColor: '#0d0d0d'}}>
        <h1 className="text-4xl font-bold font-mono whitespace-nowrap neon-glow fade-in" style={{color: '#33ff66', letterSpacing: '0.1em'}}>
          U N F R E E Z E
        </h1>
      </div>
    );
  }

  return null;
};

export default Onboarding;

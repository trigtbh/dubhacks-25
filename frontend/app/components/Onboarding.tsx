'use client';

import { useState, useEffect } from 'react';
import { ArrowRight } from 'lucide-react';
import Logo from '../components/Logo';
import AudioBar from '../components/AudioBar';
import TypingText from "@/components/text/typing-text";
import Cookies from "js-cookie";

interface OnboardingProps {
  onComplete: () => void;
}

const Onboarding = ({ onComplete }: OnboardingProps) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [scrambledText, setScrambledText] = useState('');
  const [showUnfreeze, setShowUnfreeze] = useState(false);
  const [showSvg, setShowSvg] = useState(false);
  const [showAudioBar, setShowAudioBar] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [showContinue, setShowContinue] = useState(false);
  const [showName, setShowName] = useState(false);
  const [scrambledName, setScrambledName] = useState('');
  const [showTypingText, setShowTypingText] = useState(false);
  const [selectedSpecialty, setSelectedSpecialty] = useState('');
  const [showPoll, setShowPoll] = useState(false);
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
  const [showInterestsPoll, setShowInterestsPoll] = useState(false);
  const [dubhacksProject, setDubhacksProject] = useState('');
  const [showProjectInput, setShowProjectInput] = useState(false);
  const [hobbies, setHobbies] = useState('');
  const [showHobbiesInput, setShowHobbiesInput] = useState(false);
  const [selectedPersonality, setSelectedPersonality] = useState('');
  const [showPersonalityPoll, setShowPersonalityPoll] = useState(false);
  const [selectedRiskLevel, setSelectedRiskLevel] = useState('');
  const [showRiskPoll, setShowRiskPoll] = useState(false);
  const [contact, setContact] = useState('');
  const [showContactInput, setShowContactInput] = useState(false);
  const [showFinalMessage, setShowFinalMessage] = useState(false);
  const [showFinalSplash, setShowFinalSplash] = useState(false);

  const targetText = 'U N F R E E Z E';
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()';

  // Scrambling effect for the initial UNFREEZE splash
  useEffect(() => {
    if (currentStep === 0) {
      const t0 = setTimeout(() => {
        setScrambledText('#%8^@?3&!*$9!0&4@');

        let scrambleCount = 0;
        const maxScrambles = 30; // 3s at 100ms
        const scrambleInterval = setInterval(() => {
          scrambleCount++;

          if (scrambleCount >= maxScrambles) {
            clearInterval(scrambleInterval);
            setScrambledText(targetText);
            const t1 = setTimeout(() => {
              setShowUnfreeze(true);
              const t2 = setTimeout(() => {
                setShowUnfreeze(false);
                if (Cookies.get("userid")) {
                  setCurrentStep(1.6);
                } else {
                  setCurrentStep(1);
                }
              }, 1000);
            }, 500);
            return;
          }

          const revealThreshold = (scrambleCount / maxScrambles) * targetText.length;
          setScrambledText(
            targetText
              .split('')
              .map((char, index) =>
                index < revealThreshold
                  ? char
                  : characters[Math.floor(Math.random() * characters.length)]
              )
              .join('')
          );
        }, 100);

        // cleanup for this effect
        return () => clearInterval(scrambleInterval);
      }, 1000);

      return () => clearTimeout(t0);
    }
  }, [currentStep]);

  // Go to Google SSO
  useEffect(() => {
    if (currentStep === 1) {
      const t = setTimeout(() => setCurrentStep(1.5), 1000);
      return () => clearTimeout(t);
    }
  }, [currentStep]);

  // Show Google button
  useEffect(() => {
    if (currentStep === 1.5) {
      const t = setTimeout(() => setShowForm(true), 200);
      return () => clearTimeout(t);
    }
  }, [currentStep]);

  // After Google SSO click, proceed
  useEffect(() => {
    if (currentStep === 1.6) {
      if (!Cookies.get("userid")) {
        window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/auth/login`;
      }
      
      const t = setTimeout(() => setCurrentStep(2), 2000);
      return () => clearTimeout(t);
    }
  }, [currentStep]);

  // ZERO page sequence — REWIRED to fixed timers like the FIRST file
  useEffect(() => {
    if (currentStep !== 2) return;

    setShowSvg(true);
    setShowAudioBar(true);
    setShowTypingText(true); // purely visual; no longer gates the name scramble

    const timeouts: Array<ReturnType<typeof setTimeout>> = [];
    let interval: ReturnType<typeof setInterval> | null = null;

    // +1s: show original name
    timeouts.push(
      setTimeout(() => {
        setShowName(true);
        setScrambledName('Ishaan Awasthi');

        // +1s after name shows: start scramble to Agent Phoenix (100ms × 20)
        timeouts.push(
          setTimeout(() => {
            let scrambleCount = 0;
            const maxScrambles = 20;
            const targetName = 'Agent Phoenix';

            interval = setInterval(() => {
              scrambleCount++;
              setScrambledName(() => {
                if (scrambleCount >= maxScrambles) {
                  if (interval) clearInterval(interval);
                  return targetName;
                }
                const revealThreshold = (scrambleCount / maxScrambles) * targetName.length;
                return targetName
                  .split('')
                  .map((char, index) =>
                    index < revealThreshold
                      ? char
                      : characters[Math.floor(Math.random() * characters.length)]
                  )
                  .join('');
              });
            }, 100); // time to start scrambling

            // +3s from scramble start (2s scramble + 1s): show continue
            timeouts.push(
              setTimeout(() => setShowContinue(true), 3000) // time to show button
            );
          }, 1000)
        );
      }, 7000) // time to show name
    );

    // Cleanup on unmount/step change
    return () => {
      timeouts.forEach(clearTimeout);
      if (interval) clearInterval(interval);
    };
  }, [currentStep]);

  // Show typing text and poll for FIRST page
  useEffect(() => {
    if (currentStep === 3) {
      setShowTypingText(true);
      const t = setTimeout(() => setShowPoll(true), 7000); // time before showing poll
      return () => clearTimeout(t);
    }
  }, [currentStep]);

  // Show typing text and poll for SECOND page
  useEffect(() => {
    if (currentStep === 4) {
      setShowTypingText(true);
      const t = setTimeout(() => setShowInterestsPoll(true), 7000);
      return () => clearTimeout(t);
    }
  }, [currentStep]);

  // Show typing text and input for THIRD page
  useEffect(() => {
    if (currentStep === 5) {
      setShowTypingText(true);
      const t = setTimeout(() => setShowProjectInput(true), 7000);
      return () => clearTimeout(t);
    }
  }, [currentStep]);

  // Show typing text and input for FOURTH page
  useEffect(() => {
    if (currentStep === 6) {
      setShowTypingText(true);
      const t = setTimeout(() => setShowHobbiesInput(true), 7000);
      return () => clearTimeout(t);
    }
  }, [currentStep]);

  // Show typing text and poll for FIFTH page
  useEffect(() => {
    if (currentStep === 7) {
      setShowTypingText(true);
      const t = setTimeout(() => setShowPersonalityPoll(true), 6500);
      return () => clearTimeout(t);
    }
  }, [currentStep]);

  // Show typing text and poll for SIXTH page
  useEffect(() => {
    if (currentStep === 8) {
      setShowTypingText(true);
      const t = setTimeout(() => setShowRiskPoll(true), 5000);
      return () => clearTimeout(t);
    }
  }, [currentStep]);

  // Show typing text and input for SEVENTH page
  useEffect(() => {
    if (currentStep === 9) {
      setShowTypingText(true);
      const t = setTimeout(() => setShowContactInput(true), 8000);
      return () => clearTimeout(t);
    }
  }, [currentStep]);

  // Show final message and splash for EIGHTH page
  useEffect(() => {
    if (currentStep === 10) {
      const t1 = setTimeout(() => {
        setShowFinalMessage(true);
        const t2 = setTimeout(() => {
          setShowTypingText(true);
          const t3 = setTimeout(() => {
            setShowAudioBar(false); // Hide audio bar before splash
            setShowFinalSplash(true);
            const t4 = setTimeout(() => {
              onComplete();
            }, 3000);
            return () => clearTimeout(t4);
          }, 18000);
          return () => clearTimeout(t3);
        }, 1000);
        return () => clearTimeout(t2);
      }, 1000);
      return () => clearTimeout(t1);
    }
  }, [currentStep]);

  // Reset typing text when changing pages
  useEffect(() => {
    if (currentStep !== 2 && currentStep !== 3 && currentStep !== 4 && currentStep !== 5 && currentStep !== 6 && currentStep !== 7 && currentStep !== 8 && currentStep !== 9) {
      setShowTypingText(false);
    }
  }, [currentStep]);

  const handleNext = () => {
    if (currentStep === 1.6) {
      setCurrentStep(2);
    } else if (currentStep === 2) {
      setCurrentStep(3);
      setShowTypingText(false); // Reset typing text
    } else if (currentStep === 3) {
      setCurrentStep(4);
      setShowTypingText(false); // Reset typing text
    } else if (currentStep === 4) {
      setCurrentStep(5);
      setShowTypingText(false); // Reset typing text
    } else if (currentStep === 5) {
      setCurrentStep(6);
      setShowTypingText(false); // Reset typing text
    } else if (currentStep === 6) {
      setCurrentStep(7);
      setShowTypingText(false); // Reset typing text
    } else if (currentStep === 7) {
      setCurrentStep(8);
      setShowTypingText(false); // Reset typing text
    } else if (currentStep === 8) {
      setCurrentStep(9);
      setShowTypingText(false); // Reset typing text
    } else if (currentStep === 9) {
      setCurrentStep(10);
      setShowTypingText(false); // Reset typing text
    } else if (currentStep === 10) {
      onComplete();
    }
  };

  const handleSpecialtySelect = (specialty: string) => {
    setSelectedSpecialty(specialty);
  };

  const handleInterestSelect = (interest: string) => {
    setSelectedInterests(prev => 
      prev.includes(interest) 
        ? prev.filter(item => item !== interest)
        : [...prev, interest]
    );
  };

  const handleProjectChange = (value: string) => {
    setDubhacksProject(value);
  };

  const handleHobbiesChange = (value: string) => {
    setHobbies(value);
  };

  const handlePersonalitySelect = (personality: string) => {
    setSelectedPersonality(personality);
  };

  const handleRiskSelect = (riskLevel: string) => {
    setSelectedRiskLevel(riskLevel);
  };

  const handleContactChange = (value: string) => {
    setContact(value);
  };

  if (currentStep === 0) {
    return (
      <div className="h-screen flex items-center justify-center px-4" style={{ backgroundColor: '#0d0d0d' }}>
        {scrambledText && (
          <h1 className="text-4xl font-bold font-mono whitespace-nowrap neon-glow" style={{ color: '#33ff66', letterSpacing: '0.1em' }}>
            {scrambledText}
          </h1>
        )}
      </div>
    );
  }

  if (currentStep === 1.5) {
    return (
      <div className="h-screen flex items-center justify-center" style={{ backgroundColor: '#0d0d0d' }}>
        {showForm && (
          <button
            onClick={() => setCurrentStep(1.6)}
            className="px-8 py-4 rounded-lg border transition-all hover:scale-105 font-mono fade-in"
            style={{
              backgroundColor: 'rgba(26, 26, 26, 0.8)',
              borderColor: 'rgba(51, 255, 102, 0.4)',
              color: '#33ff66',
              backdropFilter: 'blur(10px)',
              boxShadow: '0 0 10px rgba(51, 255, 102, 0.4)'
            }}
          >
            Continue with Google
          </button>
        )}
      </div>
    );
  }

  if (currentStep === 1.6) {
    return (
      <div className="h-screen relative" style={{ backgroundColor: '#0d0d0d' }}>
        {/* intentionally empty (black) like your original second file */}
      </div>
    );
  }

  // ZERO - Welcome page
  if (currentStep === 2) {
    return (
      <div className="h-screen relative" style={{ backgroundColor: '#0d0d0d' }}>
        {showSvg && (
          <div className="absolute top-[40%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in transition-all duration-1000 ease-in-out">
            <Logo />
          </div>
        )}

        {showAudioBar && (
          <div className="absolute top-[40%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 fade-in transition-all duration-1000 ease-in-out">
            <AudioBar />
          </div>
        )}

        {/* Typing effect is visual-only; scramble is now timer-driven */}
        {showTypingText && (
          <div className="absolute bottom-24 left-4 right-4">
            <TypingText
              text={["> Welcome to the Syndicate, Ishaan. Let's encrypt that identity, shall we?"]}
              typingSpeed={30}
              pauseDuration={0}
              showCursor={true}
              cursorCharacter="█"
              className="text-lg font-mono"
              textColors={['rgba(51, 255, 102, 0.8)']}
              variableSpeed={{ min: 60, max: 90 }}
            />
          </div>
        )}

        {showName && (
          <div className="absolute top-[55%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
            <div className="text-2xl font-mono whitespace-nowrap" style={{ color: '#33ff66' }}>
              {scrambledName}
            </div>
          </div>
        )}

        {showContinue && (
          <div className="absolute bottom-[35%] left-1/2 transform -translate-x-1/2 translate-y-1/2 fade-in">
            <button
              onClick={handleNext}
              className="p-1.5 rounded transition-all hover:scale-105"
              style={{ backgroundColor: '#2CFF05', color: '#0a0a0a', boxShadow: '0 0 10px rgba(51, 255, 102, 0.4)' }}
            >
              <ArrowRight size={16} />
            </button>
          </div>
        )}
      </div>
    );
  }

  // FIRST - Specialty poll
  if (currentStep === 3) {
    return (
      <div className="h-screen relative" style={{ backgroundColor: '#0d0d0d' }}>
        {/* Page counter */}
        <div className="absolute top-4 right-4 text-sm font-mono" style={{ color: 'rgba(51, 255, 102, 0.6)' }}>
          1/7
        </div>

        {/* Spy symbol at 20% from top */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in transition-all duration-1000 ease-in-out">
          <Logo />
        </div>

        {/* Audio bar on top of spy symbol */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 fade-in transition-all duration-1000 ease-in-out">
          <AudioBar />
        </div>

        {/* Subtitle with typing effect */}
        {showTypingText && (
          <div className="absolute bottom-24 left-4 right-4">
            <TypingText
              text={["> Alright, Agent Phoenix. Let's classify your specialty for Mission Control."]}
              typingSpeed={30}
              pauseDuration={0}
              showCursor={true}
              cursorCharacter="█"
              className="text-lg font-mono"
              textColors={['rgba(51, 255, 102, 0.8)']}
              variableSpeed={{ min: 60, max: 90 }}
            />
          </div>
        )}

        {/* Poll */}
        {showPoll && (
          <div className="absolute top-[50%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
            <div className="w-80 p-4 rounded-lg border neon-border" style={{ backgroundColor: 'rgba(26, 26, 26, 0.8)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)' }}>
              <h2 className="text-lg font-bold font-mono mb-3" style={{ color: '#33ff66' }}>
                Which seems most like you?
              </h2>
              <div className="space-y-2">
                {['Analyst (thinker/coder)', 'Operative (designer/creator)', 'Engineer (builder/fixer)', 'Strategist (planner/leader)'].map((option) => (
                  <button
                    key={option}
                    onClick={() => handleSpecialtySelect(option)}
                    className={`w-full p-2 rounded border font-mono text-left transition-all text-sm ${
                      selectedSpecialty === option 
                        ? 'border-green-400 bg-green-400 bg-opacity-20' 
                        : 'border-gray-600 hover:border-green-400'
                    }`}
                    style={{ color: '#33ff66' }}
                  >
                    {option}
                  </button>
                ))}
              </div>
              <div className="flex justify-end mt-3">
                <button
                  onClick={handleNext}
                  disabled={!selectedSpecialty}
                  className="p-1.5 rounded disabled:opacity-50 transition-all hover:scale-105"
                  style={{ backgroundColor: '#2CFF05', color: '#0a0a0a', boxShadow: '0 0 10px rgba(51, 255, 102, 0.4)' }}
                >
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // SECOND - Interests poll
  if (currentStep === 4) {
    return (
      <div className="h-screen relative" style={{ backgroundColor: '#0d0d0d' }}>
        {/* Page counter */}
        <div className="absolute top-4 right-4 text-sm font-mono" style={{ color: 'rgba(51, 255, 102, 0.6)' }}>
          2/7
        </div>

        {/* Spy symbol at 20% from top */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
          <Logo />
        </div>

        {/* Audio bar on top of spy symbol */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 fade-in">
          <AudioBar />
        </div>

        {/* Subtitle with typing effect */}
        {showTypingText && (
          <div className="absolute bottom-24 left-4 right-4">
            <TypingText
              text={["> Command is requesting more intel. Which mission zones interest you?"]}
              typingSpeed={30}
              pauseDuration={0}
              showCursor={true}
              cursorCharacter="█"
              className="text-lg font-mono"
              textColors={['rgba(51, 255, 102, 0.8)']}
              variableSpeed={{ min: 60, max: 90 }}
            />
          </div>
        )}

        {/* Poll */}
        {showInterestsPoll && (
          <div className="absolute top-[50%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
            <div className="w-80 p-4 rounded-lg border neon-border" style={{ backgroundColor: 'rgba(26, 26, 26, 0.8)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)' }}>
              <h2 className="text-lg font-bold font-mono mb-3" style={{ color: '#33ff66' }}>
                Which fields interest you? (select any)
              </h2>
              <div className="grid grid-cols-2 gap-2">
                {['Innovation & Startups', 'AI & ML', 'Gaming', 'Music', 'Hardware', 'Sustainability', 'People & Community', 'Wellness'].map((option) => (
                  <button
                    key={option}
                    onClick={() => handleInterestSelect(option)}
                    className={`p-2 rounded border font-mono text-left transition-all text-sm ${
                      selectedInterests.includes(option) 
                        ? 'border-green-400 bg-green-400 bg-opacity-20' 
                        : 'border-gray-600 hover:border-green-400'
                    }`}
                    style={{ color: '#33ff66' }}
                  >
                    {option}
                  </button>
                ))}
              </div>
              <div className="flex justify-end mt-3">
                <button
                  onClick={handleNext}
                  className="p-1.5 rounded transition-all hover:scale-105"
                  style={{ backgroundColor: '#2CFF05', color: '#0a0a0a', boxShadow: '0 0 10px rgba(51, 255, 102, 0.4)' }}
                >
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // THIRD - DubHacks project input
  if (currentStep === 5) {
    return (
      <div className="h-screen relative" style={{ backgroundColor: '#0d0d0d' }}>
        {/* Page counter */}
        <div className="absolute top-4 right-4 text-sm font-mono" style={{ color: 'rgba(51, 255, 102, 0.6)' }}>
          3/7
        </div>

        {/* Spy symbol at 20% from top */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
          <Logo />
        </div>

        {/* Audio bar on top of spy symbol */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 fade-in">
          <AudioBar />
        </div>

        {/* Subtitle with typing effect */}
        {showTypingText && (
          <div className="absolute bottom-24 left-4 right-4">
            <TypingText
              text={["> The Syndicate still needs to know what experience you have hacking."]}
              typingSpeed={30}
              pauseDuration={0}
              showCursor={true}
              cursorCharacter="█"
              className="text-lg font-mono"
              textColors={['rgba(51, 255, 102, 0.8)']}
              variableSpeed={{ min: 60, max: 90 }}
            />
          </div>
        )}

        {/* Input form */}
        {showProjectInput && (
          <div className="absolute top-[50%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
            <div className="w-80 p-4 rounded-lg border neon-border" style={{ backgroundColor: 'rgba(26, 26, 26, 0.8)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)' }}>
              <h2 className="text-lg font-bold font-mono mb-3" style={{ color: '#33ff66' }}>
                What are you building for DubHacks 2025?
              </h2>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={dubhacksProject}
                  onChange={(e) => handleProjectChange(e.target.value)}
                  className="flex-1 px-3 py-2 rounded border font-mono text-sm"
                  style={{ backgroundColor: '#0d0d0d', borderColor: 'rgba(51, 255, 102, 0.4)', color: '#33ff66' }}
                  placeholder="Describe your project..."
                />
                <button
                  onClick={handleNext}
                  disabled={!dubhacksProject.trim()}
                  className="p-1.5 rounded disabled:opacity-50 transition-all hover:scale-105"
                  style={{ backgroundColor: '#2CFF05', color: '#0a0a0a', boxShadow: '0 0 10px rgba(51, 255, 102, 0.4)' }}
                >
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // FOURTH - Hobbies input
  if (currentStep === 6) {
    return (
      <div className="h-screen relative" style={{ backgroundColor: '#0d0d0d' }}>
        {/* Page counter */}
        <div className="absolute top-4 right-4 text-sm font-mono" style={{ color: 'rgba(51, 255, 102, 0.6)' }}>
          4/7
        </div>

        {/* Spy symbol at 20% from top */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in transition-all duration-1000 ease-in-out">
          <Logo />
        </div>

        {/* Audio bar on top of spy symbol */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 fade-in transition-all duration-1000 ease-in-out">
          <AudioBar />
        </div>

        {/* Subtitle with typing effect */}
        {showTypingText && (
          <div className="absolute bottom-24 left-4 right-4">
            <TypingText
              text={["> The best agents have a strong secret identity. Tell us more about yours."]}
              typingSpeed={30}
              pauseDuration={0}
              showCursor={true}
              cursorCharacter="█"
              className="text-lg font-mono"
              textColors={['rgba(51, 255, 102, 0.8)']}
              variableSpeed={{ min: 60, max: 90 }}
            />
          </div>
        )}

        {/* Input form */}
        {showHobbiesInput && (
          <div className="absolute top-[50%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
            <div className="w-80 p-4 rounded-lg border neon-border" style={{ backgroundColor: 'rgba(26, 26, 26, 0.8)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)' }}>
              <h2 className="text-lg font-bold font-mono mb-3" style={{ color: '#33ff66' }}>
                What are your hobbies and interests? List as many as possible.
              </h2>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={hobbies}
                  onChange={(e) => handleHobbiesChange(e.target.value)}
                  className="flex-1 px-3 py-2 rounded border font-mono text-sm"
                  style={{ backgroundColor: '#0d0d0d', borderColor: 'rgba(51, 255, 102, 0.4)', color: '#33ff66' }}
                  placeholder="List your hobbies and interests..."
                />
                <button
                  onClick={handleNext}
                  disabled={!hobbies.trim()}
                  className="p-1.5 rounded disabled:opacity-50 transition-all hover:scale-105"
                  style={{ backgroundColor: '#2CFF05', color: '#0a0a0a', boxShadow: '0 0 10px rgba(51, 255, 102, 0.4)' }}
                >
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // FIFTH - Personality poll
  if (currentStep === 7) {
    return (
      <div className="h-screen relative" style={{ backgroundColor: '#0d0d0d' }}>
        {/* Page counter */}
        <div className="absolute top-4 right-4 text-sm font-mono" style={{ color: 'rgba(51, 255, 102, 0.6)' }}>
          5/7
        </div>

        {/* Spy symbol at 20% from top */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in transition-all duration-1000 ease-in-out">
          <Logo />
        </div>

        {/* Audio bar on top of spy symbol */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 fade-in transition-all duration-1000 ease-in-out">
          <AudioBar />
        </div>

        {/* Subtitle with typing effect */}
        {showTypingText && (
          <div className="absolute bottom-24 left-4 right-4">
            <TypingText
              text={["> Thanks, Agent Phoenix. How do you prefer to operate in the field?"]}
              typingSpeed={30}
              pauseDuration={0}
              showCursor={true}
              cursorCharacter="█"
              className="text-lg font-mono"
              textColors={['rgba(51, 255, 102, 0.8)']}
              variableSpeed={{ min: 60, max: 90 }}
            />
          </div>
        )}

        {/* Poll */}
        {showPersonalityPoll && (
          <div className="absolute top-[50%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
            <div className="w-80 p-4 rounded-lg border neon-border" style={{ backgroundColor: 'rgba(26, 26, 26, 0.8)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)' }}>
              <h2 className="text-lg font-bold font-mono mb-3" style={{ color: '#33ff66' }}>
                Which kind of person are you?
              </h2>
              <div className="space-y-2">
                {['Stealth mode (quiet & thoughtful)', 'Tactical (fast & curious)', 'Social chameleon (talks to everyone)', 'Chaos agent (unpredictable genius)'].map((option) => (
                  <button
                    key={option}
                    onClick={() => handlePersonalitySelect(option)}
                    className={`w-full p-2 rounded border font-mono text-left transition-all text-sm ${
                      selectedPersonality === option 
                        ? 'border-green-400 bg-green-400 bg-opacity-20' 
                        : 'border-gray-600 hover:border-green-400'
                    }`}
                    style={{ color: '#33ff66' }}
                  >
                    {option}
                  </button>
                ))}
              </div>
              <div className="flex justify-end mt-3">
                <button
                  onClick={handleNext}
                  disabled={!selectedPersonality}
                  className="p-1.5 rounded disabled:opacity-50 transition-all hover:scale-105"
                  style={{ backgroundColor: '#2CFF05', color: '#0a0a0a', boxShadow: '0 0 10px rgba(51, 255, 102, 0.4)' }}
                >
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // SIXTH - Risk clearance poll
  if (currentStep === 8) {
    return (
      <div className="h-screen relative" style={{ backgroundColor: '#0d0d0d' }}>
        {/* Page counter */}
        <div className="absolute top-4 right-4 text-sm font-mono" style={{ color: 'rgba(51, 255, 102, 0.6)' }}>
          6/7
        </div>

        {/* Spy symbol at 20% from top */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in transition-all duration-1000 ease-in-out">
          <Logo />
        </div>

        {/* Audio bar on top of spy symbol */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 fade-in transition-all duration-1000 ease-in-out">
          <AudioBar />
        </div>

        {/* Subtitle with typing effect */}
        {showTypingText && (
          <div className="absolute bottom-24 left-4 right-4">
            <TypingText
              text={["> Select your risk clearance for upcoming missions:"]}
              typingSpeed={30}
              pauseDuration={0}
              showCursor={true}
              cursorCharacter="█"
              className="text-lg font-mono"
              textColors={['rgba(51, 255, 102, 0.8)']}
              variableSpeed={{ min: 60, max: 90 }}
            />
          </div>
        )}

        {/* Poll */}
        {showRiskPoll && (
          <div className="absolute top-[50%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
            <div className="w-80 p-4 rounded-lg border neon-border" style={{ backgroundColor: 'rgba(26, 26, 26, 0.8)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)' }}>
              <h2 className="text-lg font-bold font-mono mb-3" style={{ color: '#33ff66' }}>
                Which clearance level?
              </h2>
              <div className="space-y-2">
                {['Sleeper Cell', 'Top Secret', 'DEFCON 1'].map((option) => (
                  <button
                    key={option}
                    onClick={() => handleRiskSelect(option)}
                    className={`w-full p-2 rounded border font-mono text-left transition-all text-sm ${
                      selectedRiskLevel === option 
                        ? 'border-green-400 bg-green-400 bg-opacity-20' 
                        : 'border-gray-600 hover:border-green-400'
                    }`}
                    style={{ color: '#33ff66' }}
                  >
                    {option}
                  </button>
                ))}
              </div>
              <div className="flex justify-end mt-3">
                <button
                  onClick={handleNext}
                  disabled={!selectedRiskLevel}
                  className="p-1.5 rounded disabled:opacity-50 transition-all hover:scale-105"
                  style={{ backgroundColor: '#2CFF05', color: '#0a0a0a', boxShadow: '0 0 10px rgba(51, 255, 102, 0.4)' }}
                >
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // SEVENTH - Contact input
  if (currentStep === 9) {
    return (
      <div className="h-screen relative" style={{ backgroundColor: '#0d0d0d' }}>
        {/* Page counter */}
        <div className="absolute top-4 right-4 text-sm font-mono" style={{ color: 'rgba(51, 255, 102, 0.6)' }}>
          7/7
        </div>

        {/* Spy symbol at 20% from top */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in transition-all duration-1000 ease-in-out">
          <Logo />
        </div>

        {/* Audio bar on top of spy symbol */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 fade-in transition-all duration-1000 ease-in-out">
          <AudioBar />
        </div>

        {/* Subtitle with typing effect */}
        {showTypingText && (
          <div className="absolute bottom-24 left-4 right-4">
            <TypingText
              text={["> One last thing, Agent — please provide a secure comm channel for post-mission contact."]}
              typingSpeed={30}
              pauseDuration={0}
              showCursor={true}
              cursorCharacter="█"
              className="text-lg font-mono"
              textColors={['rgba(51, 255, 102, 0.8)']}
              variableSpeed={{ min: 60, max: 90 }}
            />
          </div>
        )}

        {/* Input form */}
        {showContactInput && (
          <div className="absolute top-[50%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
            <div className="w-80 p-4 rounded-lg border neon-border" style={{ backgroundColor: 'rgba(26, 26, 26, 0.8)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)' }}>
              <h2 className="text-lg font-bold font-mono mb-3" style={{ color: '#33ff66' }}>
                Instagram, Discord, Linkedin, etc.:
              </h2>
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={contact}
                  onChange={(e) => handleContactChange(e.target.value)}
                  className="flex-1 px-3 py-2 rounded border font-mono text-sm"
                  style={{ backgroundColor: '#0d0d0d', borderColor: 'rgba(51, 255, 102, 0.4)', color: '#33ff66' }}
                  placeholder="@username or profile link..."
                />
                <button
                  onClick={handleNext}
                  disabled={!contact.trim()}
                  className="p-1.5 rounded disabled:opacity-50 transition-all hover:scale-105"
                  style={{ backgroundColor: '#2CFF05', color: '#0a0a0a', boxShadow: '0 0 10px rgba(51, 255, 102, 0.4)' }}
                >
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // EIGHTH - Final message and splash
  if (currentStep === 10) {
    return (
      <div className="h-screen relative" style={{ backgroundColor: '#0d0d0d' }}>
        {/* Spy symbol at 20% from top */}
        <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in transition-all duration-1000 ease-in-out">
          <Logo />
        </div>

        {/* Audio bar on top of spy symbol */}
        {showAudioBar && (
          <div className="absolute top-[20%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-10 fade-in transition-all duration-1000 ease-in-out">
            <AudioBar />
          </div>
        )}

        {/* Final message */}
        {showFinalMessage && (
          <div className="absolute top-[50%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 fade-in">
            <div className="w-80 p-4 rounded-lg border neon-border" style={{ backgroundColor: 'rgba(26, 26, 26, 0.8)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)' }}>
              {(
                <TypingText
                  text={["> The Syndicate thanks you, Agent Phoenix. Now check out the interface that Mission Control has designed for you, and get ready for your first mission. We'll be in touch."]}
                  typingSpeed={30}
                  pauseDuration={0}
                  showCursor={true}
                  cursorCharacter="█"
                  className="text-lg font-mono"
                  textColors={['rgba(51, 255, 102, 0.8)']}
                  variableSpeed={{ min: 60, max: 90 }}
                />
              )
              }
            </div>
          </div>
        )}

        {/* Final splash */}
        {showFinalSplash && (
          <div className="absolute inset-0 flex items-center justify-center px-4" style={{ backgroundColor: '#0d0d0d' }}>
            <h1 className="text-4xl font-bold font-mono whitespace-nowrap neon-glow fade-in" style={{ color: '#33ff66', letterSpacing: '0.1em' }}>
              U N F R E E Z E
            </h1>
          </div>
        )}
      </div>
    );
  }

  return null;
};

export default Onboarding;

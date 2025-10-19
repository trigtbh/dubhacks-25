'use client';

import { useState, useEffect } from 'react';
import { User, Crosshair, Crown, Edit, UserLock, MapPin, ShieldCheck, ChevronDown, ChevronUp } from 'lucide-react';
import Onboarding from './components/Onboarding';

export default function Home() {
  const [currentPage, setCurrentPage] = useState('page1');
  const [timeLeft, setTimeLeft] = useState(3600); // 1 hour in seconds
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);
  const [showOnboarding, setShowOnboarding] = useState(true);
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [isAgentInfoCollapsed, setIsAgentInfoCollapsed] = useState(false);

  // Countdown timer effect
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 0) {
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Swipe handlers
  const minSwipeDistance = 50;

  const onTouchStart = (e: React.TouchEvent) => {
    setTouchEnd(null);
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const onTouchEnd = () => {
    if (!touchStart || !touchEnd) return;
    
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe) {
      // Swipe left - go to next page
      if (currentPage === 'page1') setCurrentPage('page2');
      else if (currentPage === 'page2') setCurrentPage('page3');
    }
    
    if (isRightSwipe) {
      // Swipe right - go to previous page
      if (currentPage === 'page3') setCurrentPage('page2');
      else if (currentPage === 'page2') setCurrentPage('page1');
    }
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'page1':
  return (
          <div className="h-full overflow-y-auto">
          {/* Header */}
            <div className="p-6 pb-4 fade-in">
              <h1 className="text-4xl font-bold font-mono mb-2 neon-glow" style={{color: '#33ff66'}}>Agent Phoenix</h1>
              <p className="text-lg font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>&gt; Secret Name: Alexandra Chen</p>
          </div>

            {/* Agent Info Card */}
            <div className="mx-6 mb-6 fade-in">
              <div className="rounded-lg border neon-border" style={{backgroundColor: 'rgba(26, 26, 26, 0.6)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(5px)'}}>
                <div className="flex items-center justify-between p-5 cursor-pointer" onClick={() => setIsAgentInfoCollapsed(!isAgentInfoCollapsed)}>
                  <h2 className="text-2xl font-semibold font-mono" style={{color: '#33ff66'}}>Agent Info</h2>
                  <div className="flex items-center gap-2">
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        setIsEditingProfile(true);
                      }} 
                      className="hover:scale-110 transition-transform"
                    >
                      <Edit size={20} style={{color: 'rgba(51, 255, 102, 0.8)'}} />
                    </button>
                    {isAgentInfoCollapsed ? (
                      <ChevronDown size={24} style={{color: 'rgba(51, 255, 102, 0.8)'}} />
                    ) : (
                      <ChevronUp size={24} style={{color: 'rgba(51, 255, 102, 0.8)'}} />
                    )}
                  </div>
                </div>
                {!isAgentInfoCollapsed && (
                  <div className="px-5 pb-5">
                    <p className="text-base leading-relaxed font-mono" style={{color: 'rgba(51, 255, 102, 0.7)', lineHeight: '1.7'}}>
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                    </p>
                  </div>
                )}
              </div>
              </div>
              
            {/* Previous Missions Card */}
            <div className="mx-6 mb-6 fade-in">
              <div className="rounded-lg border neon-border" style={{backgroundColor: 'rgba(26, 26, 26, 0.6)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(5px)'}}>
                <div className="p-4 border-b" style={{borderColor: 'rgba(51, 255, 102, 0.25)'}}>
                  <h2 className="text-2xl font-semibold font-mono" style={{color: '#33ff66'}}>Previous Missions</h2>
                </div>
                <div className="max-h-48 overflow-y-auto">
                  <div className="p-3 border-b hover:bg-opacity-20 hover:bg-green-900 transition-colors cursor-pointer" style={{borderColor: 'rgba(51, 255, 102, 0.15)'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Mission 1</h3>
                  </div>
                  <div className="p-3 border-b hover:bg-opacity-20 hover:bg-green-900 transition-colors cursor-pointer" style={{borderColor: 'rgba(51, 255, 102, 0.15)'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Mission 2</h3>
                  </div>
                  <div className="p-3 border-b hover:bg-opacity-20 hover:bg-green-900 transition-colors cursor-pointer" style={{borderColor: 'rgba(51, 255, 102, 0.15)'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Mission 3</h3>
                  </div>
                  <div className="p-3 border-b hover:bg-opacity-20 hover:bg-green-900 transition-colors cursor-pointer" style={{borderColor: 'rgba(51, 255, 102, 0.15)'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Mission 4</h3>
                  </div>
                  <div className="p-3 border-b hover:bg-opacity-20 hover:bg-green-900 transition-colors cursor-pointer" style={{borderColor: 'rgba(51, 255, 102, 0.15)'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Mission 5</h3>
                  </div>
                  <div className="p-3 border-b hover:bg-opacity-20 hover:bg-green-900 transition-colors cursor-pointer" style={{borderColor: 'rgba(51, 255, 102, 0.15)'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Mission 6</h3>
                  </div>
                  <div className="p-3 border-b hover:bg-opacity-20 hover:bg-green-900 transition-colors cursor-pointer" style={{borderColor: 'rgba(51, 255, 102, 0.15)'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Mission 7</h3>
                  </div>
                  <div className="p-3 border-b hover:bg-opacity-20 hover:bg-green-900 transition-colors cursor-pointer" style={{borderColor: 'rgba(51, 255, 102, 0.15)'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Mission 8</h3>
                  </div>
                  <div className="p-3 border-b hover:bg-opacity-20 hover:bg-green-900 transition-colors cursor-pointer" style={{borderColor: 'rgba(51, 255, 102, 0.15)'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Mission 9</h3>
                  </div>
                  <div className="p-3 hover:bg-opacity-20 hover:bg-green-900 transition-colors cursor-pointer">
                    <h3 className="font-medium text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Mission 10</h3>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      case 'page2':
        return (
          <div className="h-full overflow-y-auto">
            {/* Header */}
            <div className="p-6 pb-4 fade-in">
              <h1 className="text-4xl font-bold font-mono mb-2 neon-glow" style={{color: '#33ff66'}}>Current Mission</h1>
              <p className="text-lg font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>&gt; Operation: Caffeine-Withdrawal</p>
            </div>

            {/* Countdown Timer */}
            <div className="px-6 mb-8 text-center fade-in">
              <div className="text-6xl font-mono font-bold pulse" style={{
                color: timeLeft < 60 ? '#FF0000' : timeLeft < 300 ? '#FF9500' : '#FF0000',
                textShadow: timeLeft < 60 ? '0 0 20px #FF0000, 0 0 40px #FF0000' : '0 0 10px #FF0000, 0 0 20px #FF0000'
              }}>
                {formatTime(timeLeft)}
              </div>
            </div>

            {/* Mission Details Card */}
            <div className="mx-6 mb-6 fade-in">
              <div className="rounded-lg border p-5 neon-border" style={{backgroundColor: 'rgba(26, 26, 26, 0.6)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(5px)'}}>
                {/* Co-Op Section */}
                <div className="flex items-center mb-5">
                  <UserLock size={24} style={{color: '#33ff66'}} className="mr-3" />
                  <div>
                    <span className="text-2xl font-semibold font-mono" style={{color: '#33ff66'}}>Co-Op:</span>
                    <p className="text-base font-mono mt-1" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Agent Nebula</p>
                  </div>
                </div>

                {/* Rendezvous Section */}
                <div className="flex items-center mb-6">
                  <MapPin size={24} style={{color: '#33ff66'}} className="mr-3" />
                <div>
                    <span className="text-2xl font-semibold font-mono" style={{color: '#33ff66'}}>Rendezvous:</span>
                    <p className="text-base font-mono mt-1" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Redbull Fridge</p>
                  </div>
                </div>

                {/* Task Section - 2x size */}
                <div className="flex items-start">
                  <ShieldCheck size={24} style={{color: '#33ff66'}} className="mr-3 mt-1" />
                  <div className="flex-1">
                    <span className="text-2xl font-semibold font-mono" style={{color: '#33ff66'}}>Task:</span>
                    <p className="text-base leading-relaxed font-mono mt-1" style={{color: 'rgba(51, 255, 102, 0.8)', lineHeight: '1.7'}}>
                      Exactly when the timer hits zero, drop to the floor and do ten push-ups
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      case 'page3':
        return (
          <div className="h-full overflow-y-auto">
            {/* Header */}
            <div className="p-6 pb-4 fade-in">
              <h1 className="text-4xl font-bold font-mono mb-2 neon-glow" style={{color: '#33ff66'}}>Top Operatives</h1>
            </div>

            {/* Leaderboard Card */}
            <div className="mx-6 mb-6 fade-in">
              <div className="rounded-lg border p-4 neon-border" style={{backgroundColor: 'rgba(26, 26, 26, 0.6)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(5px)'}}>
                <div className="space-y-1">
                  {/* Top 5 Agents */}
                  <div className="flex items-center justify-between py-3 border-b hover:bg-opacity-10 hover:bg-green-900 transition-colors" style={{borderColor: 'rgba(51, 255, 102, 0.25)'}}>
                    <span className="text-lg font-bold font-mono neon-glow" style={{color: '#33ff66'}}>1.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Agent Shadow</span>
                      <span className="text-sm font-mono opacity-70" style={{color: 'rgba(51, 255, 102, 0.8)'}}>12 missions</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between py-3 border-b hover:bg-opacity-10 hover:bg-green-900 transition-colors" style={{borderColor: 'rgba(51, 255, 102, 0.25)'}}>
                    <span className="text-lg font-bold font-mono" style={{color: '#33ff66'}}>2.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Agent Viper</span>
                      <span className="text-sm font-mono opacity-70" style={{color: 'rgba(51, 255, 102, 0.8)'}}>6 missions</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between py-3 border-b hover:bg-opacity-10 hover:bg-green-900 transition-colors" style={{borderColor: 'rgba(51, 255, 102, 0.25)'}}>
                    <span className="text-lg font-bold font-mono" style={{color: '#33ff66'}}>3.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Agent Storm</span>
                      <span className="text-sm font-mono opacity-70" style={{color: 'rgba(51, 255, 102, 0.8)'}}>4 missions</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between py-3 border-b hover:bg-opacity-10 hover:bg-green-900 transition-colors" style={{borderColor: 'rgba(51, 255, 102, 0.25)'}}>
                    <span className="text-lg font-bold font-mono" style={{color: '#33ff66'}}>4.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Agent Falcon</span>
                      <span className="text-sm font-mono opacity-70" style={{color: 'rgba(51, 255, 102, 0.8)'}}>2 missions</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between py-3 border-b hover:bg-opacity-10 hover:bg-green-900 transition-colors" style={{borderColor: 'rgba(51, 255, 102, 0.25)'}}>
                    <span className="text-lg font-bold font-mono" style={{color: '#33ff66'}}>5.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>Agent Thunder</span>
                      <span className="text-sm font-mono opacity-70" style={{color: 'rgba(51, 255, 102, 0.8)'}}>1 mission</span>
                    </div>
                  </div>
                  
                  {/* Centered Ellipsis */}
                  <div className="flex justify-center py-4">
                    <span className="text-2xl font-bold font-mono opacity-50" style={{color: '#33ff66'}}>...</span>
                  </div>
                  
                  {/* Additional Bar */}
                  <div className="py-2 border-b" style={{borderColor: 'rgba(51, 255, 102, 0.25)'}}></div>
                  
                  {/* Position 40 */}
                  <div className="flex items-center justify-between py-3 rounded" style={{backgroundColor: 'rgba(44, 255, 5, 0.05)'}}>
                    <span className="text-lg font-bold font-mono" style={{color: '#33ff66'}}>40.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono font-bold" style={{color: '#33ff66'}}>Agent Phoenix</span>
                      <span className="text-sm font-mono opacity-70" style={{color: 'rgba(51, 255, 102, 0.8)'}}>0 missions</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Syndicate Info Card */}
            <div className="mx-6 mb-6 fade-in">
              <div className="rounded-lg border p-5 neon-border" style={{backgroundColor: 'rgba(26, 26, 26, 0.6)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(5px)'}}>
                <div className="space-y-4">
                  <div className="flex items-center">
                    <span className="text-lg font-bold font-mono mr-3" style={{color: '#33ff66'}}>Syndicate:</span>
                    <span className="text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>University of Washington</span>
                  </div>
                  <div className="flex items-center">
                    <span className="text-lg font-bold font-mono mr-3" style={{color: '#33ff66'}}>Target:</span>
                    <span className="text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>DubHacks 2025</span>
                  </div>
                  <div className="flex items-center">
                    <span className="text-lg font-bold font-mono mr-3" style={{color: '#33ff66'}}>Personnel:</span>
                    <span className="text-base font-mono" style={{color: 'rgba(51, 255, 102, 0.8)'}}>50 Agents</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      default:
        return <div className="flex items-center justify-center h-screen text-2xl font-bold">PROFILE</div>;
    }
  };

  // Show onboarding if first time or editing profile
  if (showOnboarding || isEditingProfile) {
    return (
      <Onboarding 
        onComplete={() => {
          setShowOnboarding(false);
          setIsEditingProfile(false);
        }} 
      />
    );
  }

  return (
    <div className="h-screen flex flex-col" style={{backgroundColor: '#0d0d0d'}}>
      {/* Fixed Header Bar */}
      <div className="fixed top-0 left-0 right-0 py-4 border-b z-50 neon-border" style={{backgroundColor: 'rgba(13, 13, 13, 0.95)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)'}}>
        <h1 className="text-2xl font-bold font-mono text-center neon-glow" style={{color: '#33ff66', letterSpacing: '0.4em'}}>
          U N F R E E Z E
        </h1>
      </div>
      
      <div 
        className="flex-1 pb-16 pt-20"
        onTouchStart={onTouchStart}
        onTouchMove={onTouchMove}
        onTouchEnd={onTouchEnd}
      >
        {renderPage()}
      </div>
      
      <div className="fixed bottom-0 left-0 right-0 border-t z-50 neon-border" style={{backgroundColor: 'rgba(13, 13, 13, 0.95)', borderColor: 'rgba(51, 255, 102, 0.4)', backdropFilter: 'blur(10px)'}}>
        <div className="flex">
          <button
            onClick={() => setCurrentPage('page1')}
            className="flex-1 py-4 text-center flex items-center justify-center"
            style={{
              backgroundColor: currentPage === 'page1' ? '#33ff66' : 'transparent',
              color: currentPage === 'page1' ? '#0d0d0d' : 'rgba(51, 255, 102, 0.7)',
              boxShadow: currentPage === 'page1' ? '0 0 20px rgba(51, 255, 102, 0.4)' : 'none'
            }}
          >
            <User size={24} />
          </button>
          <button
            onClick={() => setCurrentPage('page2')}
            className="flex-1 py-4 text-center flex items-center justify-center"
            style={{
              backgroundColor: currentPage === 'page2' ? '#33ff66' : 'transparent',
              color: currentPage === 'page2' ? '#0d0d0d' : 'rgba(51, 255, 102, 0.7)',
              boxShadow: currentPage === 'page2' ? '0 0 20px rgba(51, 255, 102, 0.4)' : 'none'
            }}
          >
            <Crosshair size={24} />
          </button>
          <button
            onClick={() => setCurrentPage('page3')}
            className="flex-1 py-4 text-center flex items-center justify-center"
            style={{
              backgroundColor: currentPage === 'page3' ? '#33ff66' : 'transparent',
              color: currentPage === 'page3' ? '#0d0d0d' : 'rgba(51, 255, 102, 0.7)',
              boxShadow: currentPage === 'page3' ? '0 0 20px rgba(51, 255, 102, 0.4)' : 'none'
            }}
          >
            <Crown size={24} />
          </button>
        </div>
      </div>
    </div>
  );
}
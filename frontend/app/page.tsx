'use client';

import { useState, useEffect } from 'react';
import { User, Crosshair, Crown, Edit, UserLock, MapPin, ShieldCheck } from 'lucide-react';
import Onboarding from './components/Onboarding';

export default function Home() {
  const [currentPage, setCurrentPage] = useState('page1');
  const [timeLeft, setTimeLeft] = useState(3600); // 1 hour in seconds
  const [touchStart, setTouchStart] = useState<number | null>(null);
  const [touchEnd, setTouchEnd] = useState<number | null>(null);
  const [showOnboarding, setShowOnboarding] = useState(true);
  const [isEditingProfile, setIsEditingProfile] = useState(false);

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
            <div className="p-6 pb-4">
              <h1 className="text-4xl font-bold font-mono mb-2" style={{color: '#2CFF05'}}>Agent Phoenix</h1>
              <p className="text-lg font-mono" style={{color: '#28D14C'}}>&gt; Secret Name: Alexandra Chen</p>
          </div>

            {/* Agent Info Card */}
            <div className="mx-6 mb-6">
              <div className="rounded-lg shadow-sm border p-4" style={{backgroundColor: '#141414', borderColor: '#28D14C'}}>
                <div className="flex items-center justify-between mb-3">
                  <h2 className="text-2xl font-semibold font-mono" style={{color: '#2CFF05'}}>Agent Info</h2>
                  <button onClick={() => setIsEditingProfile(true)}>
                    <Edit size={20} style={{color: '#28D14C'}} />
                  </button>
                </div>
                <p className="text-base leading-relaxed font-mono" style={{color: '#28D14C'}}>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                </p>
              </div>
              </div>
              
            {/* Previous Missions Card */}
            <div className="mx-6 mb-6">
              <div className="rounded-lg shadow-sm border" style={{backgroundColor: '#141414', borderColor: '#28D14C'}}>
                <div className="p-4 border-b" style={{borderColor: '#28D14C'}}>
                  <h2 className="text-2xl font-semibold font-mono" style={{color: '#2CFF05'}}>Previous Missions</h2>
                </div>
                <div className="max-h-48 overflow-y-auto">
                  <div className="p-3 border-b" style={{borderColor: '#28D14C'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: '#28D14C'}}>Mission 1</h3>
                  </div>
                  <div className="p-3 border-b" style={{borderColor: '#28D14C'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: '#28D14C'}}>Mission 2</h3>
                  </div>
                  <div className="p-3 border-b" style={{borderColor: '#28D14C'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: '#28D14C'}}>Mission 3</h3>
                  </div>
                  <div className="p-3 border-b" style={{borderColor: '#28D14C'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: '#28D14C'}}>Mission 4</h3>
                  </div>
                  <div className="p-3 border-b" style={{borderColor: '#28D14C'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: '#28D14C'}}>Mission 5</h3>
                  </div>
                  <div className="p-3 border-b" style={{borderColor: '#28D14C'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: '#28D14C'}}>Mission 6</h3>
                  </div>
                  <div className="p-3 border-b" style={{borderColor: '#28D14C'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: '#28D14C'}}>Mission 7</h3>
                  </div>
                  <div className="p-3 border-b" style={{borderColor: '#28D14C'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: '#28D14C'}}>Mission 8</h3>
                  </div>
                  <div className="p-3 border-b" style={{borderColor: '#28D14C'}}>
                    <h3 className="font-medium text-base font-mono" style={{color: '#28D14C'}}>Mission 9</h3>
                  </div>
                  <div className="p-3">
                    <h3 className="font-medium text-base font-mono" style={{color: '#28D14C'}}>Mission 10</h3>
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
            <div className="p-6 pb-4">
              <h1 className="text-4xl font-bold font-mono mb-2" style={{color: '#2CFF05'}}>Current Mission</h1>
              <p className="text-lg font-mono" style={{color: '#28D14C'}}>&gt; Operation: Caffeine-Withdrawal</p>
            </div>

            {/* Countdown Timer */}
            <div className="px-6 mb-8 text-center">
              <div className="text-6xl font-mono font-bold text-red-600">
                {formatTime(timeLeft)}
              </div>
            </div>

            {/* Mission Details Card */}
            <div className="mx-6 mb-6">
              <div className="rounded-lg shadow-sm border p-4" style={{backgroundColor: '#141414', borderColor: '#28D14C'}}>
                {/* Co-Op Section */}
                <div className="flex items-center mb-4">
                  <UserLock size={24} style={{color: '#2CFF05'}} className="mr-3" />
                  <div>
                    <span className="text-2xl font-semibold font-mono" style={{color: '#2CFF05'}}>Co-Op:</span>
                    <p className="text-base font-mono" style={{color: '#28D14C'}}>Agent Nebula</p>
                  </div>
                </div>

                {/* Rendezvous Section */}
                <div className="flex items-center mb-6">
                  <MapPin size={24} style={{color: '#2CFF05'}} className="mr-3" />
                <div>
                    <span className="text-2xl font-semibold font-mono" style={{color: '#2CFF05'}}>Rendezvous:</span>
                    <p className="text-base font-mono" style={{color: '#28D14C'}}>Redbull Fridge</p>
                  </div>
                </div>

                {/* Task Section - 2x size */}
                <div className="flex items-start">
                  <ShieldCheck size={24} style={{color: '#2CFF05'}} className="mr-3 mt-1" />
                  <div className="flex-1">
                    <span className="text-2xl font-semibold font-mono" style={{color: '#2CFF05'}}>Task:</span>
                    <p className="text-base leading-relaxed font-mono" style={{color: '#28D14C'}}>
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
            <div className="p-6 pb-4">
              <h1 className="text-4xl font-bold font-mono mb-2" style={{color: '#2CFF05'}}>Top Operatives</h1>
            </div>

            {/* Leaderboard Card */}
            <div className="mx-6 mb-6">
              <div className="rounded-lg shadow-sm border p-4" style={{backgroundColor: '#141414', borderColor: '#28D14C'}}>
                <div className="space-y-2">
                  {/* Top 5 Agents */}
                  <div className="flex items-center justify-between py-2 border-b" style={{borderColor: '#28D14C'}}>
                    <span className="text-lg font-bold font-mono" style={{color: '#2CFF05'}}>1.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono" style={{color: '#28D14C'}}>Agent Shadow</span>
                      <span className="text-sm font-mono" style={{color: '#28D14C'}}>12 missions</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between py-2 border-b" style={{borderColor: '#28D14C'}}>
                    <span className="text-lg font-bold font-mono" style={{color: '#2CFF05'}}>2.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono" style={{color: '#28D14C'}}>Agent Viper</span>
                      <span className="text-sm font-mono" style={{color: '#28D14C'}}>6 missions</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between py-2 border-b" style={{borderColor: '#28D14C'}}>
                    <span className="text-lg font-bold font-mono" style={{color: '#2CFF05'}}>3.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono" style={{color: '#28D14C'}}>Agent Storm</span>
                      <span className="text-sm font-mono" style={{color: '#28D14C'}}>4 missions</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between py-2 border-b" style={{borderColor: '#28D14C'}}>
                    <span className="text-lg font-bold font-mono" style={{color: '#2CFF05'}}>4.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono" style={{color: '#28D14C'}}>Agent Falcon</span>
                      <span className="text-sm font-mono" style={{color: '#28D14C'}}>2 missions</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between py-2 border-b" style={{borderColor: '#28D14C'}}>
                    <span className="text-lg font-bold font-mono" style={{color: '#2CFF05'}}>5.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono" style={{color: '#28D14C'}}>Agent Thunder</span>
                      <span className="text-sm font-mono" style={{color: '#28D14C'}}>1 mission</span>
                    </div>
                  </div>
                  
                  {/* Centered Ellipsis */}
                  <div className="flex justify-center py-4">
                    <span className="text-2xl font-bold font-mono" style={{color: '#2CFF05'}}>...</span>
                  </div>
                  
                  {/* Additional Bar */}
                  <div className="py-2 border-b" style={{borderColor: '#28D14C'}}></div>
                  
                  {/* Position 40 */}
                  <div className="flex items-center justify-between py-2">
                    <span className="text-lg font-bold font-mono" style={{color: '#2CFF05'}}>40.</span>
                    <div className="flex items-center justify-between flex-1 ml-4">
                      <span className="text-base font-mono" style={{color: '#28D14C'}}>Agent Phoenix</span>
                      <span className="text-sm font-mono" style={{color: '#28D14C'}}>0 missions</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Syndicate Info Card */}
            <div className="mx-6 mb-6">
              <div className="rounded-lg shadow-sm border p-4" style={{backgroundColor: '#141414', borderColor: '#28D14C'}}>
                <div className="space-y-3">
                  <div className="flex items-center">
                    <span className="text-lg font-bold font-mono mr-3" style={{color: '#2CFF05'}}>Syndicate:</span>
                    <span className="text-base font-mono" style={{color: '#28D14C'}}>University of Washington</span>
                  </div>
                  <div className="flex items-center">
                    <span className="text-lg font-bold font-mono mr-3" style={{color: '#2CFF05'}}>Target:</span>
                    <span className="text-base font-mono" style={{color: '#28D14C'}}>DubHacks 2025</span>
                  </div>
                  <div className="flex items-center">
                    <span className="text-lg font-bold font-mono mr-3" style={{color: '#2CFF05'}}>Personnel:</span>
                    <span className="text-base font-mono" style={{color: '#28D14C'}}>50 Agents</span>
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
    <div className="h-screen flex flex-col" style={{backgroundColor: '#141414'}}>
      {/* Fixed Header Bar */}
      <div className="fixed top-0 left-0 right-0 py-4 border-b z-50" style={{backgroundColor: '#141414', borderColor: '#28D14C'}}>
        <h1 className="text-2xl font-bold font-mono text-center" style={{color: '#2CFF05', letterSpacing: '0.4em'}}>
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
      
      <div className="fixed bottom-0 left-0 right-0 border-t z-50" style={{backgroundColor: '#141414', borderColor: '#28D14C'}}>
        <div className="flex">
          <button
            onClick={() => setCurrentPage('page1')}
            className="flex-1 py-4 text-center flex items-center justify-center"
            style={{
              backgroundColor: currentPage === 'page1' ? '#2CFF05' : '#141414',
              color: currentPage === 'page1' ? '#141414' : '#28D14C'
            }}
          >
            <User size={24} />
          </button>
          <button
            onClick={() => setCurrentPage('page2')}
            className="flex-1 py-4 text-center flex items-center justify-center"
            style={{
              backgroundColor: currentPage === 'page2' ? '#2CFF05' : '#141414',
              color: currentPage === 'page2' ? '#141414' : '#28D14C'
            }}
          >
            <Crosshair size={24} />
          </button>
          <button
            onClick={() => setCurrentPage('page3')}
            className="flex-1 py-4 text-center flex items-center justify-center"
            style={{
              backgroundColor: currentPage === 'page3' ? '#2CFF05' : '#141414',
              color: currentPage === 'page3' ? '#141414' : '#28D14C'
            }}
          >
            <Crown size={24} />
          </button>
        </div>
      </div>
    </div>
  );
}
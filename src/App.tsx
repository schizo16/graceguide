import { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import OnboardingFlow from './components/OnboardingFlow';

function App() {
  const [showOnboarding, setShowOnboarding] = useState(true);

  const handleOnboardingComplete = (_buildName: string) => {
    setShowOnboarding(false);
  };

  return (
    <div className="h-screen w-screen bg-black/80 text-white flex flex-col select-none">
      {showOnboarding ? (
        <OnboardingFlow onComplete={handleOnboardingComplete} />
      ) : (
        <ChatWindow />
      )}
    </div>
  );
}

export default App;

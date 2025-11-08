import '@mantine/core/styles.css';
import { MantineProvider } from '@mantine/core';
import { ModalsProvider } from '@mantine/modals';
import { useState } from 'react';
import { Dashboard } from './pages/Dashboard/Dashboard';
import { AlgorithmProposal } from './pages/AlgorithmProposal/AlgorithmProposal';
import { BacktestSettings } from './pages/Backtest/BacktestSettings';
import { DataManagement } from './pages/DataManagement/DataManagement';
import { DataAnalysis } from './pages/DataAnalysis/DataAnalysis';
import "./App.css";

function App() {
  const [currentPage, setCurrentPage] = useState<string>('dashboard');

  const handleNavigate = (page: string) => {
    setCurrentPage(page);
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard currentPage={currentPage} onNavigate={handleNavigate} />;
      case 'algorithm-proposal':
        return <AlgorithmProposal />;
      case 'backtest':
        return <BacktestSettings />;
      case 'data-management':
        return <DataManagement />;
      case 'data-analysis':
        return <DataAnalysis />;
      default:
        return <Dashboard currentPage={currentPage} onNavigate={handleNavigate} />;
    }
  };

  return (
    <MantineProvider>
      <ModalsProvider>
        {renderPage()}
      </ModalsProvider>
    </MantineProvider>
  );
}

export default App;

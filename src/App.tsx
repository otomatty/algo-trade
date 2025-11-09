import '@mantine/core/styles.css';
import { MantineProvider } from '@mantine/core';
import { ModalsProvider } from '@mantine/modals';
import { useState } from 'react';
import { AppShell } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { Dashboard } from './pages/Dashboard/Dashboard';
import { AlgorithmProposal } from './pages/AlgorithmProposal/AlgorithmProposal';
import { BacktestSettings } from './pages/Backtest/BacktestSettings';
import { DataManagement } from './pages/DataManagement/DataManagement';
import { DataAnalysis } from './pages/DataAnalysis/DataAnalysis';
import { StockPrediction } from './pages/StockPrediction/StockPrediction';
import { Sidebar } from './pages/Dashboard/Sidebar';
import { Header } from './pages/Dashboard/Header';
import './i18n';
import "./App.css";

function App() {
  const [currentPage, setCurrentPage] = useState<string>('dashboard');
  const [opened, { toggle }] = useDisclosure();

  const handleNavigate = (page: string) => {
    setCurrentPage(page);
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard currentPage={currentPage} onNavigate={handleNavigate} />;
      case 'algorithm-proposal':
        return <AlgorithmProposal currentPage={currentPage} onNavigate={handleNavigate} />;
      case 'backtest':
        return <BacktestSettings currentPage={currentPage} onNavigate={handleNavigate} />;
      case 'data-management':
        return <DataManagement currentPage={currentPage} onNavigate={handleNavigate} />;
      case 'data-analysis':
        return <DataAnalysis currentPage={currentPage} onNavigate={handleNavigate} />;
      case 'stock-prediction':
        return <StockPrediction currentPage={currentPage} onNavigate={handleNavigate} />;
      default:
        return <Dashboard currentPage={currentPage} onNavigate={handleNavigate} />;
    }
  };

  return (
    <MantineProvider>
      <ModalsProvider>
        <AppShell
          navbar={{
            width: 250,
            breakpoint: 'sm',
            collapsed: { mobile: !opened },
          }}
          header={{ height: 60 }}
          padding="md"
        >
          <AppShell.Header>
            <Header opened={opened} toggle={toggle} />
          </AppShell.Header>

          <AppShell.Navbar p="md">
            <Sidebar currentPage={currentPage} onNavigate={handleNavigate} />
          </AppShell.Navbar>

          <AppShell.Main>
            {renderPage()}
          </AppShell.Main>
        </AppShell>
      </ModalsProvider>
    </MantineProvider>
  );
}

export default App;

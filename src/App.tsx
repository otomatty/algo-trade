import '@mantine/core/styles.css';
import { MantineProvider } from '@mantine/core';
import { DataAnalysis } from './pages/DataAnalysis/DataAnalysis';
import "./App.css";

function App() {
  return (
    <MantineProvider>
      <DataAnalysis />
    </MantineProvider>
  );
}

export default App;

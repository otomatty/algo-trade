/**
 * Stock Prediction Page
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/App.tsx (via routing)
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ ./NewsCollectionForm
 *   ├─ ./PredictionGenerationForm
 *   ├─ ./PredictionProgress
 *   └─ ./PredictionList
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/stock-prediction/README.md
 */
import { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Container,
  Title,
  Stack,
  Paper,
  Table,
  Text,
  Button,
  Group,
  Center,
  Loader,
} from '@mantine/core';
import { MarketNews } from '../../types/news';
import { StockPrediction as StockPredictionType } from '../../types/stock-prediction';
import { NewsCollectionForm } from './NewsCollectionForm';
import { PredictionGenerationForm } from './PredictionGenerationForm';
import { PredictionProgress } from './PredictionProgress';
import { PredictionList } from './PredictionList';
import { PredictionHistory } from './PredictionHistory';

interface StockPredictionProps {
  currentPage?: string;
  onNavigate?: (page: string) => void;
}

export function StockPrediction({ currentPage, onNavigate }: StockPredictionProps) {
  const [news, setNews] = useState<MarketNews[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentJobId, setCurrentJobId] = useState<string | null>(null);
  const [predictionJobId, setPredictionJobId] = useState<string | null>(null);
  const [predictionStatus, setPredictionStatus] = useState<'idle' | 'generating' | 'completed' | 'error'>('idle');
  const [predictions, setPredictions] = useState<StockPredictionType[]>([]);
  const [showPredictions, setShowPredictions] = useState(false);
  const [predictionsLoading, setPredictionsLoading] = useState(false);

  const loadNews = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await invoke<MarketNews[]>('get_collected_news', {
        limit: 50,
        offset: 0,
        order_by: 'published_at',
        order_desc: true,
      });
      setNews(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load news');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadNews();
  }, []);

  const handleJobStarted = (jobId: string) => {
    setCurrentJobId(jobId);
    // Optionally: Start polling for job status
    // For now, just reload news after a delay
    setTimeout(() => {
      loadNews();
    }, 5000);
  };

  const handlePredictionJobStarted = (jobId: string) => {
    setPredictionJobId(jobId);
    setPredictionStatus('generating');
    setShowPredictions(false);
    setPredictions([]);
    setError(null);
  };

  const handlePredictionCompleted = async () => {
    setPredictionStatus('completed');
    if (predictionJobId) {
      await loadPredictions(predictionJobId);
    }
  };

  const loadPredictions = async (jobId: string) => {
    setPredictionsLoading(true);
    setError(null);
    try {
      const response = await invoke<{ job_id: string; predictions: StockPredictionType[] }>('get_stock_predictions', {
        job_id: jobId,
      });
      setPredictions(response.predictions || []);
      setShowPredictions(true);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to load predictions';
      setError(errorMessage);
      setPredictions([]);
    } finally {
      setPredictionsLoading(false);
    }
  };

  const handlePredictionError = (errorMessage: string) => {
    setPredictionStatus('error');
    setError(errorMessage);
  };

  return (
    <Container size="xl" py="md">
      <Stack gap="md">
        <Title order={2}>Stock Prediction</Title>

        <NewsCollectionForm onJobStarted={handleJobStarted} />

        <PredictionGenerationForm onJobStarted={handlePredictionJobStarted} />

        {predictionStatus === 'generating' && predictionJobId && (
          <PredictionProgress
            jobId={predictionJobId}
            onCompleted={handlePredictionCompleted}
            onError={handlePredictionError}
          />
        )}

        {predictionsLoading && (
          <Center py="xl">
            <Loader />
          </Center>
        )}

        {showPredictions && !predictionsLoading && (
          <PredictionList predictions={predictions} />
        )}

        {!showPredictions && !predictionJobId && !predictionsLoading && (
          <PredictionList predictions={[]} />
        )}

        <Paper p="md" withBorder>
          <Group justify="space-between" mb="md">
            <Title order={3}>Collected News</Title>
            <Button onClick={loadNews} loading={loading}>
              Refresh
            </Button>
          </Group>

          {error && (
            <Text c="red" mb="md">
              {error}
            </Text>
          )}

          <Table>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Title</Table.Th>
                <Table.Th>Source</Table.Th>
                <Table.Th>Published At</Table.Th>
                <Table.Th>Actions</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {news.map((item) => (
                <Table.Tr key={item.id}>
                  <Table.Td>{item.title}</Table.Td>
                  <Table.Td>{item.source}</Table.Td>
                  <Table.Td>
                    {new Date(item.published_at).toLocaleString()}
                  </Table.Td>
                  <Table.Td>
                    {item.url && (
                      <Button
                        size="xs"
                        variant="light"
                        component="a"
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        Open
                      </Button>
                    )}
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>

          {news.length === 0 && !loading && (
            <Text c="dimmed" ta="center" py="xl">
              No news collected yet. Use the form above to collect news.
            </Text>
          )}
        </Paper>

        <PredictionHistory />
      </Stack>
    </Container>
  );
}


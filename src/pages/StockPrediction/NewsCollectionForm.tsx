/**
 * News Collection Form Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/StockPrediction/StockPrediction.tsx (to be created)
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   └─ src/types/news
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/news-collection/README.md
 */
import { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Button,
  Stack,
  Text,
  Alert,
  Paper,
  Checkbox,
  TextInput,
  NumberInput,
  Group,
} from '@mantine/core';

interface NewsCollectionFormProps {
  onJobStarted?: (jobId: string) => void;
}

export function NewsCollectionForm({ onJobStarted }: NewsCollectionFormProps) {
  const [useRss, setUseRss] = useState(true);
  const [useApi, setUseApi] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [keywords, setKeywords] = useState('');
  const [maxArticles, setMaxArticles] = useState(50);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleCollect = async () => {
    if (useApi && !apiKey) {
      setError('API key is required when using NewsAPI');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const keywordsList = keywords
        ? keywords.split(',').map(k => k.trim()).filter(k => k.length > 0)
        : undefined;

      const result = await invoke<{
        job_id: string;
        collected_count: number;
        skipped_count: number;
      }>('collect_market_news', {
        use_rss: useRss,
        use_api: useApi,
        api_key: useApi ? apiKey : undefined,
        keywords: keywordsList,
        max_articles: maxArticles,
      });

      setSuccess(true);
      if (onJobStarted && result.job_id) {
        onJobStarted(result.job_id);
      }
      
      // Show warning if there are warnings
      if (result.warnings && result.warnings.length > 0) {
        setError(`Warning: ${result.warnings.join('; ')}`);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to collect news';
      console.error('News collection error:', err);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper p="md" withBorder>
      <Stack gap="md">
        <Text fw={500} size="lg">Collect Market News</Text>

        <Checkbox
          label="Collect from RSS feeds (Yahoo Finance, Reuters, Bloomberg)"
          checked={useRss}
          onChange={(e) => setUseRss(e.currentTarget.checked)}
        />

        <Checkbox
          label="Collect from NewsAPI (requires API key)"
          checked={useApi}
          onChange={(e) => setUseApi(e.currentTarget.checked)}
        />

        {useApi && (
          <TextInput
            label="NewsAPI Key"
            placeholder="Enter your NewsAPI key"
            value={apiKey}
            onChange={(e) => setApiKey(e.currentTarget.value)}
            type="password"
          />
        )}

        {useApi && (
          <TextInput
            label="Keywords (comma-separated)"
            placeholder="stock, market, finance"
            value={keywords}
            onChange={(e) => setKeywords(e.currentTarget.value)}
            description="Optional: Filter news by keywords"
          />
        )}

        {useApi && (
          <NumberInput
            label="Max Articles"
            value={maxArticles}
            onChange={(value) => setMaxArticles(typeof value === 'number' ? value : 50)}
            min={1}
            max={100}
            description="Maximum number of articles to fetch (1-100)"
          />
        )}

        {error && (
          <Alert color="red" title="Error">
            {error}
          </Alert>
        )}

        {success && (
          <Alert color="green" title="Success">
            News collection started successfully!
          </Alert>
        )}

        <Group justify="flex-end">
          <Button
            onClick={handleCollect}
            loading={loading}
            disabled={useApi && !apiKey}
          >
            Collect News
          </Button>
        </Group>
      </Stack>
    </Paper>
  );
}


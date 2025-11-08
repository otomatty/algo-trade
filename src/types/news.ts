/**
 * News Collection Types
 * 
 * Related Documentation:
 * - Plan: docs/03_plans/news-collection/README.md
 */

export interface MarketNews {
  id: number;
  title: string;
  content: string | null;
  source: string;
  url: string | null;
  published_at: string;
  collected_at: string;
  keywords: string[] | null;
  sentiment: 'positive' | 'neutral' | 'negative' | null;
}


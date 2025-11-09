/**
 * Action Proposal Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/StockPrediction/PredictionDetailModal.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ @mantine/notifications
 *   ├─ src/types/stock-prediction
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/stock-prediction/README.md
 */
import { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';
import {
  Stack,
  Text,
  Radio,
  Textarea,
  Button,
  Group,
  Divider,
  Loader,
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { SavePredictionActionRequest, SavePredictionActionResponse } from '../../types/stock-prediction';

interface ActionProposalProps {
  predictionId: string;
  suggestedAction?: 'buy' | 'sell' | 'hold' | 'watch';
  onActionSaved?: () => void;
}

export function ActionProposal({ predictionId, suggestedAction, onActionSaved }: ActionProposalProps) {
  const [selectedAction, setSelectedAction] = useState<'buy' | 'sell' | 'hold' | 'watch' | 'ignore'>(
    suggestedAction || 'watch'
  );
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSave = async () => {
    if (!predictionId) return;

    setLoading(true);
    try {
      const request: SavePredictionActionRequest = {
        prediction_id: predictionId,
        action: selectedAction,
        notes: notes.trim() || undefined,
      };

      const result = await invoke<SavePredictionActionResponse>('save_prediction_action', request);

      notifications.show({
        title: 'Action Saved',
        message: `Your action "${selectedAction.toUpperCase()}" has been saved successfully.`,
        color: 'green',
      });

      // Reset form
      setNotes('');
      
      if (onActionSaved) {
        onActionSaved();
      }
    } catch (error) {
      notifications.show({
        title: 'Save Failed',
        message: error instanceof Error ? error.message : 'Failed to save action',
        color: 'red',
      });
    } finally {
      setLoading(false);
    }
  };

  const actionLabels: Record<string, string> = {
    buy: 'Buy',
    sell: 'Sell',
    hold: 'Hold',
    watch: 'Watch',
    ignore: 'Ignore',
  };

  const actionColors: Record<string, string> = {
    buy: 'green',
    sell: 'red',
    hold: 'yellow',
    watch: 'blue',
    ignore: 'gray',
  };

  return (
    <Stack gap="md">
      <Divider label="Action Proposal" labelPosition="center" />
      
      <div>
        <Text fw={500} size="sm" mb="xs">
          Select Your Action
        </Text>
        {suggestedAction && (
          <Text size="xs" c="dimmed" mb="md">
            Suggested: {actionLabels[suggestedAction]}
          </Text>
        )}
        <Radio.Group
          value={selectedAction}
          onChange={(value) => setSelectedAction(value as typeof selectedAction)}
        >
          <Stack gap="xs">
            {(['buy', 'sell', 'hold', 'watch', 'ignore'] as const).map((action) => (
              <Radio
                key={action}
                value={action}
                label={actionLabels[action]}
                color={actionColors[action]}
              />
            ))}
          </Stack>
        </Radio.Group>
      </div>

      <Textarea
        label="Notes (Optional)"
        placeholder="Add any notes about this prediction..."
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        minRows={3}
        maxRows={6}
      />

      <Group justify="flex-end">
        <Button
          onClick={handleSave}
          loading={loading}
          disabled={loading}
          color={actionColors[selectedAction]}
        >
          {loading ? (
            <>
              <Loader size="xs" mr="xs" />
              Saving...
            </>
          ) : (
            'Save Action'
          )}
        </Button>
      </Group>
    </Stack>
  );
}


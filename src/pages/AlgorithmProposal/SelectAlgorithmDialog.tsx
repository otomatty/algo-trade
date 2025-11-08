/**
 * Select Algorithm Dialog Component
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/pages/AlgorithmProposal/ProposalList.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ @tauri-apps/api/core
 *   ├─ @mantine/core
 *   ├─ @mantine/notifications
 *   ├─ src/types/algorithm
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/AlgorithmProposal/AlgorithmProposal.spec.md
 *   └─ Plan: docs/03_plans/algorithm-proposal/IMPLEMENTATION_GUIDE.md
 */
import { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { Modal, Stack, Text, TextInput, Button, Group, Badge, Loader } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { AlgorithmProposal } from '../../types/algorithm';

interface SelectAlgorithmDialogProps {
  proposal: AlgorithmProposal | null;
  opened: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export function SelectAlgorithmDialog({ proposal, opened, onClose, onSuccess }: SelectAlgorithmDialogProps) {
  const [customName, setCustomName] = useState('');
  const [loading, setLoading] = useState(false);

  if (!proposal) {
    return null;
  }

  const confidenceColor = proposal.confidence_score
    ? proposal.confidence_score >= 0.8
      ? 'green'
      : proposal.confidence_score >= 0.6
      ? 'yellow'
      : 'red'
    : 'gray';

  const handleSelect = async () => {
    if (!proposal) return;

    setLoading(true);
    try {
      const result = await invoke<{ algorithm_id: number; name: string }>('select_algorithm', {
        proposal_id: proposal.proposal_id,
        custom_name: customName.trim() || undefined,
      });

      notifications.show({
        title: 'Algorithm Selected',
        message: `Algorithm "${result.name}" has been saved successfully.`,
        color: 'green',
      });

      // Reset form
      setCustomName('');
      onClose();
      
      if (onSuccess) {
        onSuccess();
      }
    } catch (error) {
      notifications.show({
        title: 'Selection Failed',
        message: error instanceof Error ? error.message : 'Failed to select algorithm',
        color: 'red',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setCustomName('');
    onClose();
  };

  return (
    <Modal
      opened={opened}
      onClose={handleCancel}
      title="Select Algorithm"
      size="md"
    >
      <Stack gap="md">
        <div>
          <Text fw={500} size="sm" mb="xs">
            Algorithm Name
          </Text>
          <Text size="sm" c="dimmed" mb="xs">
            {proposal.name}
          </Text>
          {proposal.confidence_score !== undefined && (
            <Badge color={confidenceColor} variant="light" size="sm">
              Confidence: {(proposal.confidence_score * 100).toFixed(0)}%
            </Badge>
          )}
        </div>

        <div>
          <Text fw={500} size="sm" mb="xs">
            Description
          </Text>
          <Text size="sm" c="dimmed" lineClamp={3}>
            {proposal.description}
          </Text>
        </div>

        <TextInput
          label="Custom Name (Optional)"
          placeholder="Enter a custom name for this algorithm"
          value={customName}
          onChange={(e) => setCustomName(e.target.value)}
          description="If not specified, the proposal name will be used"
        />

        <Group justify="flex-end" mt="md">
          <Button variant="outline" onClick={handleCancel} disabled={loading}>
            Cancel
          </Button>
          <Button onClick={handleSelect} loading={loading} disabled={loading}>
            {loading ? (
              <>
                <Loader size="xs" mr="xs" />
                Selecting...
              </>
            ) : (
              'Select Algorithm'
            )}
          </Button>
        </Group>
      </Stack>
    </Modal>
  );
}


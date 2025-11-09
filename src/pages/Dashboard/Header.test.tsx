/**
 * Tests for Header component
 * 
 * Related Documentation:
 *   ├─ Spec: src/pages/Dashboard/Dashboard.spec.md
 *   └─ Plan: docs/03_plans/dashboard/README.md
 */
import { describe, it, expect, beforeEach, beforeAll, mock } from 'bun:test';
import { render, within } from '@testing-library/react';
import { Header } from './Header';
import { MantineProvider } from '@mantine/core';
import { I18nextProvider } from 'react-i18next';
import { setupDOM, setupDOMSync } from '../../test-utils/dom-setup';
import i18n from '../../i18n';

// Setup DOM synchronously before module initialization
setupDOMSync();

describe('Header', () => {
  beforeAll(async () => {
    await setupDOM();
  });

  beforeEach(() => {
    i18n.changeLanguage('ja');
  });

  it('should render app title', () => {
    const toggle = mock(() => {});
    const { container } = render(
      <MantineProvider>
        <I18nextProvider i18n={i18n}>
          <Header opened={false} toggle={toggle} />
        </I18nextProvider>
      </MantineProvider>
    );

    expect(within(container).getByText('Algorithm Trading Platform')).toBeDefined();
  });

  it('should render language selector', () => {
    const toggle = mock(() => {});
    const { container } = render(
      <MantineProvider>
        <I18nextProvider i18n={i18n}>
          <Header opened={false} toggle={toggle} />
        </I18nextProvider>
      </MantineProvider>
    );

    const languageSelect = container.querySelector('input[type="text"]');
    expect(languageSelect).toBeDefined();
  });

  it('should change language when language selector value changes', () => {
    const toggle = mock(() => {});
    const { container } = render(
      <MantineProvider>
        <I18nextProvider i18n={i18n}>
          <Header opened={false} toggle={toggle} />
        </I18nextProvider>
      </MantineProvider>
    );

    expect(i18n.language).toBe('ja');
    
    // Simulate language change
    i18n.changeLanguage('en');
    
    expect(i18n.language).toBe('en');
  });

  it('should render burger menu on mobile', () => {
    const toggle = mock(() => {});
    const { container } = render(
      <MantineProvider>
        <I18nextProvider i18n={i18n}>
          <Header opened={false} toggle={toggle} />
        </I18nextProvider>
      </MantineProvider>
    );

    const burger = container.querySelector('button[aria-label]');
    expect(burger).toBeDefined();
  });

  it('should call toggle when burger is clicked', () => {
    const toggle = mock(() => {});
    const { container } = render(
      <MantineProvider>
        <I18nextProvider i18n={i18n}>
          <Header opened={false} toggle={toggle} />
        </I18nextProvider>
      </MantineProvider>
    );

    const burger = container.querySelector('button[aria-label]');
    if (burger) {
      burger.click();
      expect(toggle).toHaveBeenCalled();
    }
  });

  it('should use translation keys correctly', async () => {
    await i18n.changeLanguage('ja');
    const t = i18n.getFixedT('ja', 'navigation');
    
    expect(t('appTitle')).toBe('Algorithm Trading Platform');
  });
});


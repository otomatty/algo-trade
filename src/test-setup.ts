/**
 * Global test setup for Bun tests
 * This file is automatically loaded before all tests
 */
import { setupDOM } from './test-utils/dom-setup';

// Setup DOM environment before any tests run
await setupDOM();

/**
 * i18n Resource Type Definitions
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/i18n/index.ts (for type checking)
 * 
 * Dependencies (External files that this file imports):
 *   └─ react-i18next
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/i18n/ (to be created)
 */
import 'react-i18next';
import commonJa from './locales/ja/common.json';
import navigationJa from './locales/ja/navigation.json';

declare module 'react-i18next' {
  interface CustomTypeOptions {
    defaultNS: 'common';
    resources: {
      common: typeof commonJa;
      navigation: typeof navigationJa;
    };
  }
}


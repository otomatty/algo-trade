/**
 * i18next Configuration
 * 
 * DEPENDENCY MAP:
 * 
 * Parents (Files that import this file):
 *   └─ src/App.tsx
 * 
 * Dependencies (External files that this file imports):
 *   ├─ i18next
 *   ├─ i18next-browser-languagedetector
 *   └─ react-i18next
 * 
 * Related Documentation:
 *   └─ Plan: docs/03_plans/i18n/ (to be created)
 */
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import jaCommon from './locales/ja/common.json';
import jaNavigation from './locales/ja/navigation.json';
import enCommon from './locales/en/common.json';
import enNavigation from './locales/en/navigation.json';

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      ja: {
        common: jaCommon,
        navigation: jaNavigation,
      },
      en: {
        common: enCommon,
        navigation: enNavigation,
      },
    },
    fallbackLng: 'ja',
    defaultNS: 'common',
    ns: ['common', 'navigation'],
    interpolation: {
      escapeValue: false,
    },
    detection: {
      order: ['localStorage', 'navigator'],
      caches: ['localStorage'],
      lookupLocalStorage: 'i18nextLng',
    },
  });

export default i18n;


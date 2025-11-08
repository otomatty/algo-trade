/**
 * DOM setup utility for Bun tests
 * This file provides a common DOM setup for all test files
 */
let domSetup = false;

export async function setupDOM() {
  // Check if DOM is already set up
  if (domSetup && typeof globalThis.document !== 'undefined' && globalThis.document.body) {
    return;
  }

  const { JSDOM } = await import('jsdom');
  const dom = new JSDOM('<!DOCTYPE html><html><head></head><body></body></html>', {
    url: 'http://localhost',
    pretendToBeVisual: true,
    resources: 'usable',
  });
  
  const window = dom.window;
  
  // Set up all global properties
  globalThis.window = window as unknown as Window & typeof globalThis;
  globalThis.document = window.document;
  globalThis.navigator = window.navigator;
  globalThis.HTMLElement = window.HTMLElement;
  globalThis.Element = window.Element;
  globalThis.Node = window.Node;
  globalThis.getComputedStyle = window.getComputedStyle;
  globalThis.CSSStyleDeclaration = window.CSSStyleDeclaration;
  globalThis.Document = window.Document;
  globalThis.HTMLDocument = window.HTMLDocument;
  
  // Mock ResizeObserver
  globalThis.ResizeObserver = class ResizeObserver {
    observe() {}
    unobserve() {}
    disconnect() {}
  } as unknown as typeof ResizeObserver;
  
  // Mock IntersectionObserver
  globalThis.IntersectionObserver = class IntersectionObserver {
    observe() {}
    unobserve() {}
    disconnect() {}
    takeRecords() { return []; }
  } as unknown as typeof IntersectionObserver;
  
  // Mock attachEvent/detachEvent for React DOM compatibility (IE legacy API)
  if (typeof (window as any).HTMLElement !== 'undefined') {
    const HTMLElementPrototype = (window as any).HTMLElement.prototype;
    if (!HTMLElementPrototype.attachEvent) {
      HTMLElementPrototype.attachEvent = function(_event: string, _handler: any) {};
    }
    if (!HTMLElementPrototype.detachEvent) {
      HTMLElementPrototype.detachEvent = function(_event: string, _handler: any) {};
    }
  }
  
  // Mock attachEvent/detachEvent on document.activeElement
  const originalActiveElement = Object.getOwnPropertyDescriptor(document, 'activeElement');
  Object.defineProperty(document, 'activeElement', {
    get: function() {
      const element = originalActiveElement?.get?.call(document) || document.body || null;
      if (element && typeof (element as any).attachEvent === 'undefined') {
        (element as any).attachEvent = function(_event: string, _handler: any) {};
        (element as any).detachEvent = function(_event: string, _handler: any) {};
      }
      return element;
    },
    configurable: true
  });
  
  globalThis.requestAnimationFrame = (callback: FrameRequestCallback) => {
    return setTimeout(callback, 0);
  };
  
  globalThis.cancelAnimationFrame = (id: number) => {
    clearTimeout(id);
  };
  
  // Ensure document.body exists and is accessible
  if (!globalThis.document.body) {
    const body = globalThis.document.createElement('body');
    globalThis.document.documentElement.appendChild(body);
  }
  
  // Ensure document is accessible globally for @testing-library/react
  // This is critical for screen queries to work
  (globalThis as any).document = globalThis.document;
  (globalThis as any).window = globalThis.window;
  
  // Also set it on global object (not just globalThis)
  (global as any).document = globalThis.document;
  (global as any).window = globalThis.window;
  
  domSetup = true;
}

// Synchronous setup for immediate use (works with Bun's --dom flag)
export function setupDOMSync() {
  if (domSetup && typeof globalThis.document !== 'undefined' && globalThis.document.body) {
    return;
  }
  
  // Check if Bun's --dom flag already provides DOM
  if (typeof globalThis.document !== 'undefined') {
    // Ensure document.body exists
    if (!globalThis.document.body) {
      const body = globalThis.document.createElement('body');
      if (globalThis.document.documentElement) {
        globalThis.document.documentElement.appendChild(body);
      }
    }
    
    // Ensure document is accessible globally
    (globalThis as any).document = globalThis.document;
    (globalThis as any).window = globalThis.window;
    (global as any).document = globalThis.document;
    (global as any).window = globalThis.window;
    
    // Mock ResizeObserver if not available
    if (typeof globalThis.ResizeObserver === 'undefined') {
      globalThis.ResizeObserver = class ResizeObserver {
        observe() {}
        unobserve() {}
        disconnect() {}
      } as unknown as typeof ResizeObserver;
    }
    
    // Mock IntersectionObserver if not available
    if (typeof globalThis.IntersectionObserver === 'undefined') {
      globalThis.IntersectionObserver = class IntersectionObserver {
        observe() {}
        unobserve() {}
        disconnect() {}
        takeRecords() { return []; }
      } as unknown as typeof IntersectionObserver;
    }
    
    domSetup = true;
    return;
  }
  
  // If DOM is not available, async setup will be called
}

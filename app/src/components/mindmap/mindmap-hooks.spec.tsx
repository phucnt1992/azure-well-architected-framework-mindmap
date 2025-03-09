import React from 'react';
import { afterAll, beforeAll, describe, expect, test, vi } from 'vitest';
;
import { render, screen } from '@testing-library/react';

import { MindmapHooks } from './mindmap-hooks';

describe("MindmapHooks Component", () => {
  beforeAll(() => {
    // Because of this issue: https://github.com/vitest-dev/vitest/issues/4143,
    // We need to mock the markdown-toolbar module to avoid the import undefined error
    vi.mock('markmap-toolbar', () => {
      const Toolbar = vi.fn();
      Toolbar.prototype.attach = vi.fn();
      Toolbar.prototype.register = vi.fn();
      Toolbar.prototype.setItems = vi.fn();
      Toolbar.prototype.render = vi.fn();

      return {
        Toolbar: Object.assign(Toolbar, {
          defaultItems: []
        })
      };
    })
  });

  afterAll(() => {
    vi.resetAllMocks();
  });

  test("should render the mindmap element", () => {
    // Arrange

    // Mock ResizeObserver to avoid the error: ResizeObserver not defined
    window.ResizeObserver =
      window.ResizeObserver ||
      vi.fn().mockImplementation(() => ({
        disconnect: vi.fn(),
        observe: vi.fn(),
        unobserve: vi.fn(),
      }));

    // Act
    render(<MindmapHooks />);
    // Assert
    const mindmapElement = screen.getByTestId("mindmap");
    expect(mindmapElement).toBeInTheDocument();
  });
});

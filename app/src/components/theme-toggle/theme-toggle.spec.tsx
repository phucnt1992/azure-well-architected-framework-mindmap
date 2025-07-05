import React from 'react';
import { describe, expect, test } from 'vitest';

import { render, screen } from '@testing-library/react';

import { ThemeToggle } from './theme-toggle';

describe("ThemeToggle Component", () => {
  test("should render the ThemeToggle element", () => {
    // Act
    render(<ThemeToggle />);
    // Assert
    const headerElement = screen.getByTestId("header");
    expect(headerElement).toBeInTheDocument();
  });
});

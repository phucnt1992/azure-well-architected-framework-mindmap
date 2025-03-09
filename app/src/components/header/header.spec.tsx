import React from 'react';
import { describe, expect, test } from 'vitest';

import { render, screen } from '@testing-library/react';

import { Header } from './header';

describe("Header Component", () => {
  test("should render the header element", () => {
    // Act
    render(<Header />);
    // Assert
    const headerElement = screen.getByTestId("header");
    expect(headerElement).toBeInTheDocument();
  });
});

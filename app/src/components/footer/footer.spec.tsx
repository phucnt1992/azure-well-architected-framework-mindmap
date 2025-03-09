import { describe, expect, test } from 'vitest';

import { render, screen } from '@testing-library/react';

import { Footer } from './footer';

describe("Footer Component", () => {
  test("renders the footer element", () => {
    // Act
    render(<Footer />);
    // Assert
    const footerElement = screen.getByTestId("footer");
    expect(footerElement).toBeInTheDocument();
  });

  test("displays correct copyright text and include current year", () => {
    // Arrange
    const currentYear = new Date().getFullYear();
    // Act
    render(<Footer />);
    // Assert
    const copyrightText = screen.getByText(
      new RegExp(`Copyright © ${currentYear} - Phuc Nguyen`, "i")
    );
    expect(copyrightText).toBeInTheDocument();
  });
});

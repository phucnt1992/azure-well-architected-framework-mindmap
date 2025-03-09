import { describe, expect, test } from 'vitest';

import { transformer } from './markmap';

describe('markmap', () => {
  // Arrange
  const testCases = [
    // Input, expected output
    ["", ""],
    ["# test", "test"],
    ["- test", "test"],
  ]

  test.each(testCases)('should transform input correctly for "%s"', (input, expectedOutput) => {
    // Act
    const output = transformer.transform(input);

    // Assert
    expect(output.root.content).toBe(expectedOutput);
  });
});

import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { describe, expect, test } from 'vitest';
import Markmap from './Markmap.astro';

describe('Markmap component', () => {
  test('renders correctly', async () => {
    // Arrange
    const container = await AstroContainer.create();

    // Act
    const result = await container.renderToString(Markmap);

    // Assert
    expect(result).toContain('https://cdn.jsdelivr.net/npm/markmap-autoloader@latest');
  })
});

import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { describe, expect, test, vi } from 'vitest';
import Footer from './Footer.astro';

describe('Footer component', () => {
  test('renders correctly', async () => {
    // Arrange
    const container = await AstroContainer.create();
    const currentYear = new Date().getFullYear();

    // Act
    const result = await container.renderToString(Footer, {
      locals: {
        t: ((key: string) => key) as any,
        starlightRoute: ({
          editUrl: new URL('https://example.com/edit'),
          siteTitle: 'Example Site',
          pagination: {
            nextUrl: new URL('https://example.com/page/2'),
            prevUrl: new URL('https://example.com/page/1'),
          }
        }) as any
      },
    });

    // Assert
    expect(result).toContain(currentYear);
    expect(result).toContain('All rights reserved.');
  })
});

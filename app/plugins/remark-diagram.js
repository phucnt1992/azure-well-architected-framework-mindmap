import { visit } from 'unist-util-visit'

export function remarkDiagram() {
  return function (tree, { data }) {
    if (!data.astro.frontmatter['extra']) {
      data.astro.frontmatter.extra = []
    }

    // Add math to extra frontmatter
    visit(tree, 'inlineMath', _ => {
      if (!data.astro.frontmatter.extra.includes('math')) {
        data.astro.frontmatter.extra.push('math')
      }
    })

    // Add markmap to extra frontmatter
    visit(tree, 'code', node => {
      if (node.lang == 'markmap') {
        node.type = 'html'
        node.value = `<div class="${node.lang}"><script type="text/template">${node.value}</script></div>`

        if (!data.astro.frontmatter.extra.includes(node.lang)) {
          data.astro.frontmatter.extra.push(node.lang)
        }
      }
    })
  }
}

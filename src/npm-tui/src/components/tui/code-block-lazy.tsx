import { PrismLight as SyntaxHighlighter } from 'react-syntax-highlighter'
import python from 'react-syntax-highlighter/dist/esm/languages/prism/python'
import dracula from 'react-syntax-highlighter/dist/esm/styles/prism/dracula'
import { CopyButton } from '@/components/tui/copy-button'

import { cn } from '@/lib/utils'

SyntaxHighlighter.registerLanguage('python', python)

export type CodeBlockLazyProps = {
  componentType: 'code-block'
  className?: string
  text: string
  language?: string
}

export default function CodeBlockLazy(props: CodeBlockLazyProps) {
  return (
    <div className="relative">
      <CopyButton
        value={props.text}
        className="absolute right-4 top-3 z-20 w-6 h-6 p-1.5"
        componentType="copy-button"
      />
      <SyntaxHighlighter className={cn(props.className)} PreTag="div" language={props.language} style={dracula}>
        {props.text}
      </SyntaxHighlighter>
    </div>
  )
}

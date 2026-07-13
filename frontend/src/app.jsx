import { useState, useRef, useEffect } from 'react'

function Seal() {
  return <div className="seal">LA</div>
}

function Nav() {
  return (
    <nav className="top">
      <div className="brand">
        <Seal />
        <span>Ledger Advisor</span>
      </div>
      <a className="btn" href="https://github.com/Eshal-Fathima/investment_advisory_agent" target="_blank" rel="noreferrer">View repository</a>
    </nav>
  )
}

function IntroStrip() {
  return (
    <section className="intro-strip">
      <div className="wrap">
        <span className="eyebrow">CrewAI-powered advisory desk</span>
        <h1 className="intro-headline">Ask a question. Get a reasoned answer <em>— read like a ledger.</em></h1>
        <p className="intro-sub">Stock and fund picks, portfolio reviews, market and sector context — a small crew of agents works the question before it reaches you.</p>
      </div>
    </section>
  )
}

function ChatPanel() {
  const [messages, setMessages] = useState([
    { role: 'agent', text: "I'm your investment advisor agent. Ask me about a stock, a fund, or hand me your portfolio to review." },
  ])
  const [input, setInput] = useState('')
  const [isThinking, setIsThinking] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isThinking])

  async function handleSend() {
    const question = input.trim()
    if (!question) return

    setMessages((prev) => [...prev, { role: 'user', text: question }])
    setInput('')
    setIsThinking(true)

    try {
      const response = await fetch('http://localhost:5000/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      })

      if (!response.ok) throw new Error('Request failed')

      const data = await response.json()
      setMessages((prev) => [...prev, { role: 'agent', text: data.answer }])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'agent', text: "Couldn't reach the backend. Is server.py running on port 5000?" },
      ])
    } finally {
      setIsThinking(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <section id="chat">
      <div className="wrap">
        <div className="chat-shell">
          <div className="chat-header">
            <span>Advisory session</span>
            <span className="chat-header-dot">● live-ish</span>
          </div>
          <div className="messages">
            {messages.map((m, i) => (
              <div className={'msg ' + m.role} key={i}>
                <span className="msg-label">{m.role === 'user' ? 'You' : 'Agent'}</span>
                <p>{m.text}</p>
              </div>
            ))}
            {isThinking && (
              <div className="msg agent">
                <span className="msg-label">Agent</span>
                <p className="thinking">thinking…</p>
              </div>
            )}
            <div ref={bottomRef} />
          </div>
          <div className="chat-input-row">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about a stock, a fund, or your portfolio…"
              rows={1}
            />
            <button className="btn-solid" onClick={handleSend}>Send</button>
          </div>
        </div>
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '6px' }} id="disclaimer">
      <div className="wrap" style={{ width: '100%' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <span className="fine">Ledger Advisor — a CrewAI project by Eshal Fathima</span>
          <a className="btn" href="https://github.com/Eshal-Fathima/investment_advisory_agent" target="_blank" rel="noreferrer">github.com/Eshal-Fathima</a>
        </div>
        <p className="disclaimer">
          For research and education only. Nothing here is financial advice, and no output from
          this project should be the sole basis for an investment decision.
        </p>
      </div>
    </footer>
  )
}

export default function App() {
  return (
    <>
      <div className="wrap"><Nav /></div>
      <IntroStrip />
      <ChatPanel />
      <Footer />
    </>
  )
}
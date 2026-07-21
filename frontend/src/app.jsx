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

// ---- formatting helpers for the agent's raw text ----

function sectionEmoji(header) {
  const h = header.toLowerCase()
  if (h.includes('sector')) return '🏭'
  if (h.includes('portfolio')) return '💼'
  if (h.includes('market') || h.includes('trend') || h.includes('economic')) return '📈'
  if (h.includes('risk')) return '⚠️'
  if (h.includes('invest') || h.includes('fund')) return '💰'
  return '📌'
}

function parseItems(itemsText) {
  const itemRegex = /\d+\.\s*\*\*(.+?)\*\*:?\s*([\s\S]*?)(?=\d+\.\s*\*\*|$)/g
  const items = []
  for (const m of itemsText.matchAll(itemRegex)) {
    items.push({ title: m[1].trim(), body: m[2].trim() })
  }
  return items
}

function renderInlineBold(text, keyPrefix) {
  const parts = text.split(/(\*\*.+?\*\*)/g)
  return parts.map((p, i) =>
    p.startsWith('**') && p.endsWith('**') ? <strong key={`${keyPrefix}-${i}`}>{p.slice(2, -2)}</strong> : p
  )
}

function SimpleFormatted({ text, disclaimer }) {
  const lines = text.split('\n').map((l) => l.trim()).filter(Boolean)
  const bulletLines = lines.filter((l) => /^[•\-*]\s+/.test(l))
  const preambleLines = lines.filter((l) => !/^[•\-*]\s+/.test(l))

  // If the model gave us real bullet lines, render them as an actual list
  // instead of a flat paragraph — this is the common case now that the
  // task prompt asks for "•" bullets even on context-only follow-ups.
  if (bulletLines.length > 0) {
    return (
      <div className="agent-formatted">
        {preambleLines.length > 0 && (
          <p className="agent-preamble">{renderInlineBold(preambleLines.join(' '), 'pre')}</p>
        )}
        <ul>
          {bulletLines.map((line, i) => (
            <li key={i}>{renderInlineBold(line.replace(/^[•\-*]\s+/, ''), i)}</li>
          ))}
        </ul>
        {disclaimer && (
          <p className="agent-disclaimer">⚠️ <strong>Disclaimer:</strong> {disclaimer}</p>
        )}
      </div>
    )
  }

  // Last-resort fallback: no bullets detected at all, just show the text
  return (
    <div className="agent-formatted">
      <p style={{ whiteSpace: 'pre-wrap' }}>{renderInlineBold(text, 'flat')}</p>
      {disclaimer && (
        <p className="agent-disclaimer">⚠️ <strong>Disclaimer:</strong> {disclaimer}</p>
      )}
    </div>
  )
}

function formatAgentText(text) {
  if (!text) return null

  const disclaimerSplit = text.split(/\*\*Disclaimer\*\*:?/i)
  const mainText = disclaimerSplit[0].trim()
  const disclaimerText = disclaimerSplit[1] ? disclaimerSplit[1].trim() : null

  const headerRegex = /([A-Z][^:]{3,90}:)\s*(?=\d+\.\s*\*\*)/g
  const headerMatches = [...mainText.matchAll(headerRegex)]

  if (headerMatches.length === 0) {
    return <SimpleFormatted text={mainText} disclaimer={disclaimerText} />
  }

  const sections = []
  for (let i = 0; i < headerMatches.length; i++) {
    const start = headerMatches[i].index
    const end = i + 1 < headerMatches.length ? headerMatches[i + 1].index : mainText.length
    const chunk = mainText.slice(start, end)
    const headerText = headerMatches[i][1]
    const itemsText = chunk.slice(headerText.length)
    sections.push({ header: headerText.replace(/:$/, ''), items: parseItems(itemsText) })
  }

  const preamble = mainText.slice(0, headerMatches[0].index).trim()

  return (
    <div className="agent-formatted">
      {preamble && <p className="agent-preamble">{preamble}</p>}
      {sections.map((s, i) => (
        <div className="agent-section" key={i}>
          <div className="agent-section-title">
            <span className="agent-emoji">{sectionEmoji(s.header)}</span>
            <span>{s.header}</span>
          </div>
          <ul>
            {s.items.map((it, j) => (
              <li key={j}>
                <strong>{it.title}</strong>{it.body ? `: ${it.body}` : ''}
              </li>
            ))}
          </ul>
        </div>
      ))}
      {disclaimerText && (
        <p className="agent-disclaimer">⚠️ <strong>Disclaimer:</strong> {disclaimerText}</p>
      )}
    </div>
  )
}

// ---- per-browser user id, so each visitor gets their own remembered history ----

function getUserId() {
  const key = 'investment_agent_user_id'
  let id = localStorage.getItem(key)
  if (!id) {
    id = 'user_' + Math.random().toString(36).slice(2, 10)
    localStorage.setItem(key, id)
  }
  return id
}

// ---- chat panel ----

const GREETING = { role: 'agent', text: "I'm your investment advisor agent. Ask me about a stock, a fund, or hand me your portfolio to review." }

function ChatPanel() {
  const [messages, setMessages] = useState([GREETING])
  const [input, setInput] = useState('')
  const [isThinking, setIsThinking] = useState(false)
  const [chats, setChats] = useState([])
  const [currentChatId, setCurrentChatId] = useState(null)
  const bottomRef = useRef(null)
  const userIdRef = useRef(getUserId())

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isThinking])

  // Load this user's chat threads for the sidebar when the page opens
  useEffect(() => {
    loadChats()
  }, [])

  async function loadChats() {
    try {
      const response = await fetch(`http://localhost:5000/chats/${userIdRef.current}`)
      if (!response.ok) return
      const data = await response.json()
      setChats(data.chats || [])
    } catch (err) {
      // silently ignore — sidebar history is a nice-to-have, not required to chat
    }
  }

  function startNewChat() {
    setCurrentChatId(null)
    setMessages([GREETING])
  }

  async function openChat(chatId) {
    if (chatId === currentChatId) return
    try {
      const response = await fetch(`http://localhost:5000/chats/${userIdRef.current}/${chatId}`)
      if (!response.ok) return
      const chat = await response.json()
      const loaded = (chat.messages || []).map((m) => ({
        role: m.role === 'user' ? 'user' : 'agent',
        text: m.content,
      }))
      setMessages([GREETING, ...loaded])
      setCurrentChatId(chatId)
    } catch (err) {
      // leave the current view untouched if the fetch fails
    }
  }

  function formatChatDate(iso) {
    if (!iso) return ''
    const d = new Date(iso)
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
  }

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
        body: JSON.stringify({
          question,
          user_id: userIdRef.current,
          chat_id: currentChatId || undefined,
        }),
      })

      if (!response.ok) throw new Error('Request failed')

      const data = await response.json()
      setMessages((prev) => [...prev, { role: 'agent', text: data.answer }])
      if (data.chat_id && data.chat_id !== currentChatId) {
        setCurrentChatId(data.chat_id)
      }
      loadChats() // refresh sidebar so the new/updated thread shows up, newest first
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
          <aside className="chat-sidebar">
            <div className="chat-sidebar-header">Chats</div>
            <div className="chat-sidebar-new">
              <button className="new-chat-btn" onClick={startNewChat}>+ New chat</button>
            </div>
            <div className="chat-sidebar-list">
              {chats.map((c) => (
                <button
                  key={c._id}
                  className={'chat-sidebar-item' + (currentChatId === c._id ? ' active' : '')}
                  onClick={() => openChat(c._id)}
                >
                  <span className="chat-sidebar-item-date">{formatChatDate(c.updated_at)}</span>
                  <span className="chat-sidebar-item-text">{c.title}</span>
                </button>
              ))}
            </div>
          </aside>
          <div className="chat-main">
            <div className="chat-header">
              <span>Advisory session</span>
              <span className="chat-header-dot">● live-ish</span>
            </div>
            <div className="messages">
              {messages.map((m, i) => (
                <div
                  className={'msg ' + m.role}
                  key={i}
                >
                  <span className="msg-label">{m.role === 'user' ? 'You' : 'Agent'}</span>
                  {m.role === 'agent' ? formatAgentText(m.text) : <p>{m.text}</p>}
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
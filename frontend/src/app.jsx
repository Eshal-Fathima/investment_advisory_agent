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
      <div className="nav-links">
        <a href="#capabilities">Capabilities</a>
        <a href="#pipeline">How it runs</a>
        <a href="#disclaimer">Disclosure</a>
      </div>
      
        className="btn"
        href="https://github.com/Eshal-Fathima/investment_advisory_agent"
        target="_blank"
        rel="noreferrer"
      >
        View repository
      </a>
    </nav>
  )
}

function LedgerPanel() {
  const rows = [
    { name: 'Recommendation', tag: 'Stocks & mutual funds', delta: '+2.4%', dir: 'up' },
    { name: 'Portfolio review', tag: 'Allocation & risk read', delta: 'flag', dir: 'down' },
    { name: 'Sector insight', tag: 'IT · Pharma · Energy', delta: '+0.8%', dir: 'up' },
    { name: 'Market read', tag: 'Index & macro context', delta: '-0.3%', dir: 'down' },
  ]
  return (
    <div className="ledger">
      <div className="ledger-head">
        <span>Agent output</span>
        <span>Live session</span>
      </div>
      {rows.map((r, i) => (
        <div className="ledger-row" key={i}>
          <div>
            <span className="name">{r.name}</span>
            <span className="tag">{r.tag}</span>
          </div>
          <span className={'delta ' + r.dir}>{r.delta}</span>
        </div>
      ))}
    </div>
  )
}

function Hero() {
  return (
    <section style={{ borderBottom: '1px solid var(--line)', paddingTop: 0, paddingBottom: 0 }}>
      <div className="wrap hero">
        <div>
          <span className="eyebrow">CrewAI-powered advisory desk</span>
          <h1 className="headline">
            Your portfolio,
            <br />
            <em>read like a ledger.</em>
          </h1>
          <p className="sub">
            Ledger Advisor runs a small crew of specialized agents that research stocks and
            mutual funds, audit your holdings, and translate market noise into a plain,
            line-by-line brief — the way a careful analyst would, not a chatbot guessing at
            tickers.
          </p>
          <div className="cta-row">
            <a className="btn-solid" href="#capabilities">
              See what it covers
            </a>
            
              className="btn"
              href="https://github.com/Eshal-Fathima/investment_advisory_agent"
              target="_blank"
              rel="noreferrer"
            >
              Read the source
            </a>
          </div>
        </div>
        <LedgerPanel />
      </div>
    </section>
  )
}

function Capabilities() {
  const caps = [
    {
      idx: '01',
      title: 'Stock & fund picks',
      body: 'Ask a plain question about a stock or mutual fund and get a reasoned recommendation, not just a ticker and a price.',
    },
    {
      idx: '02',
      title: 'Portfolio review',
      body: 'Hand over your current holdings and the crew reads them back to you — concentration risk, gaps, and what to reconsider.',
    },
    {
      idx: '03',
      title: 'Market & sector insight',
      body: 'Zoom out to sector and index-level context, so a single recommendation is never read in isolation.',
    },
  ]
  return (
    <section id="capabilities">
      <div className="wrap">
        <div className="section-head">
          <div>
            <span className="section-num">§ 01 — Scope</span>
            <h2 className="section-title">Three things it's built to do</h2>
          </div>
          <p className="section-note">
            No portfolio execution, no order placement — this is a research and review desk, not
            a broker.
          </p>
        </div>
        <div className="capabilities">
          {caps.map((c) => (
            <div className="cap" key={c.idx}>
              <span className="idx">{c.idx}</span>
              <h3>{c.title}</h3>
              <p>{c.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function Pipeline() {
  const stages = [
    {
      tag: 'Intake',
      title: 'You ask',
      body: 'A question comes in through the terminal — about a fund, a sector, or your own holdings.',
    },
    {
      tag: 'Crew',
      title: 'Agents research',
      body: 'CrewAI agents split the work: market data, fundamentals, and portfolio context.',
    },
    {
      tag: 'Synthesis',
      title: 'Crew agrees',
      body: 'Findings are reconciled into a single point of view, not three conflicting opinions.',
    },
    {
      tag: 'Output',
      title: 'You get a brief',
      body: 'A plain-language answer, printed back — reasoning included, not just a verdict.',
    },
  ]
  return (
    <section id="pipeline">
      <div className="wrap">
        <div className="section-head">
          <div>
            <span className="section-num">§ 02 — Mechanics</span>
            <h2 className="section-title">How a question moves through the crew</h2>
          </div>
          <p className="section-note">
            Built on CrewAI, so each agent has one job and hands off cleanly to the next.
          </p>
        </div>
        <div className="pipeline">
          {stages.map((s, i) => (
            <div className="stage" key={i}>
              <span className="tag">{s.tag}</span>
              <h4>{s.title}</h4>
              <p>{s.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function Footer() {
  return (
    <footer style={{ flexDirection: 'column', alignItems: 'flex-start', gap: '6px' }} id="disclaimer">
      <div className="wrap" style={{ width: '100%' }}>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '12px',
          }}
        >
          <span className="fine">Ledger Advisor — a CrewAI project by Eshal Fathima</span>
          
            className="btn"
            href="https://github.com/Eshal-Fathima/investment_advisory_agent"
            target="_blank"
            rel="noreferrer"
          >
            github.com/Eshal-Fathima
          </a>
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
      <div className="wrap">
        <Nav />
      </div>
      <Hero />
      <Capabilities />
      <Pipeline />
      <Footer />
    </>
  )
}


import { useState, useRef, useEffect, useCallback } from 'react'

// ─── CSS ─────────────────────────────────────────────────────────────────────
const CSS = `
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --navy-900:#0d1b2e;--navy-800:#112240;--navy-700:#1a3356;--navy-600:#243d62;
  --white:#ffffff;--off-white:#f7f8fc;--surface:#f0f3f9;--surface-2:#e8ecf5;
  --accent:#2e6fda;--accent-light:#4d8af0;--accent-dim:rgba(46,111,218,0.08);
  --gold:#e8a930;--gold-dim:rgba(232,169,48,0.12);
  --text-dark:#0d1b2e;--text-mid:#3d5270;--text-soft:#6b80a0;--text-muted:#9baec8;
  --text-nav:#cdd9ee;--text-nav-soft:#8da3c0;
  --success:#1a9e6a;--success-dim:rgba(26,158,106,0.1);
  --error:#d63f4d;--error-dim:rgba(214,63,77,0.1);
  --border-light:rgba(13,27,46,0.09);--border-navy:rgba(255,255,255,0.08);
  --radius-sm:8px;--radius:12px;--radius-lg:18px;--radius-xl:24px;
  --shadow:0 8px 32px rgba(13,27,46,0.12);--shadow-lg:0 20px 60px rgba(13,27,46,0.18);
  --font-serif:'Playfair Display',Georgia,serif;
  --font-sans:'Plus Jakarta Sans',sans-serif;
  --font-mono:'Fira Code',monospace;
}
html{scroll-behavior:smooth}
body{background:var(--off-white);color:var(--text-dark);font-family:var(--font-sans);font-size:14px;line-height:1.6;min-height:100vh;overflow-x:hidden}
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:var(--surface)}
::-webkit-scrollbar-thumb{background:var(--surface-2);border-radius:4px}
.shell{min-height:100vh;display:flex;flex-direction:column}
.page{animation:pageIn .4s ease}
@keyframes pageIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}

/* ── HEADER ── */
.hdr{background:var(--navy-900);height:66px;display:flex;align-items:center;justify-content:space-between;padding:0 48px;position:sticky;top:0;z-index:200;overflow:hidden}
.hdr-logo{display:flex;align-items:center;gap:14px;position:relative;z-index:1;cursor:pointer}
.logo-mark{width:38px;height:38px;background:var(--accent);border-radius:10px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 4px rgba(46,111,218,.2),0 4px 16px rgba(46,111,218,.35)}
.logo-name{font-family:var(--font-serif);font-size:19px;font-weight:700;color:var(--white);line-height:1.1}
.logo-sub{font-size:9px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--accent-light);margin-top:1px}
.hdr-nav{display:flex;align-items:center;gap:4px;position:relative;z-index:1}
.nav-btn{padding:8px 18px;border-radius:100px;border:none;background:transparent;color:var(--text-nav-soft);font-family:var(--font-sans);font-size:12px;font-weight:600;letter-spacing:.04em;cursor:pointer;transition:all .2s}
.nav-btn:hover{color:var(--white);background:rgba(255,255,255,.06)}
.nav-btn.active{color:var(--white);background:rgba(46,111,218,.2);border:1px solid rgba(46,111,218,.3)}
.hdr-cta{display:flex;align-items:center;gap:10px;position:relative;z-index:1}
.hdr-badge{display:flex;align-items:center;gap:8px;padding:6px 16px;border-radius:100px;background:rgba(46,111,218,.15);border:1px solid rgba(46,111,218,.3);font-size:10px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-light)}
.live-dot{width:7px;height:7px;border-radius:50%;background:#4ade80;box-shadow:0 0 0 2px rgba(74,222,128,.3);animation:livePulse 2s ease-in-out infinite}
@keyframes livePulse{0%,100%{box-shadow:0 0 0 2px rgba(74,222,128,.3)}50%{box-shadow:0 0 0 6px rgba(74,222,128,0)}}
.hdr-launch{padding:8px 20px;border-radius:100px;background:var(--accent);border:none;color:white;font-family:var(--font-sans);font-size:12px;font-weight:700;letter-spacing:.06em;cursor:pointer;transition:all .2s;box-shadow:0 4px 16px rgba(46,111,218,.35)}
.hdr-launch:hover{background:var(--accent-light);transform:translateY(-1px);box-shadow:0 6px 20px rgba(46,111,218,.45)}

/* ── HERO ── */
.home-hero{background:var(--navy-800);padding:88px 48px 100px;position:relative;overflow:hidden}
.hero-content{position:relative;z-index:1;max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 480px;gap:70px;align-items:center}
.hero-eyebrow{display:flex;align-items:center;gap:10px;font-size:10px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--accent-light);margin-bottom:22px}
.hero-ey-line{width:32px;height:1px;background:var(--accent-light);opacity:.5}
.hero-heading{font-family:var(--font-serif);font-size:54px;font-weight:700;color:var(--white);line-height:1.1;margin-bottom:22px}
.hero-heading em{font-style:italic;color:var(--gold)}
.hero-desc{font-size:15px;color:var(--text-nav);line-height:1.85;max-width:490px;margin-bottom:38px}
.hero-btns{display:flex;gap:14px;flex-wrap:wrap}
.btn-primary{padding:14px 32px;border-radius:100px;background:var(--accent);border:none;color:white;font-family:var(--font-sans);font-size:13px;font-weight:700;letter-spacing:.06em;cursor:pointer;transition:all .25s;box-shadow:0 4px 20px rgba(46,111,218,.4);display:flex;align-items:center;gap:8px}
.btn-primary:hover{background:var(--accent-light);transform:translateY(-2px);box-shadow:0 8px 28px rgba(46,111,218,.5)}
.btn-ghost{padding:14px 32px;border-radius:100px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.15);color:var(--text-nav);font-family:var(--font-sans);font-size:13px;font-weight:600;cursor:pointer;transition:all .25s}
.btn-ghost:hover{background:rgba(255,255,255,.1);color:white;border-color:rgba(255,255,255,.25)}
.hero-stats{display:flex;gap:0;margin-top:44px;background:rgba(255,255,255,.04);border:1px solid var(--border-navy);border-radius:var(--radius-lg);overflow:hidden}
.hero-stat{flex:1;padding:20px 24px;border-right:1px solid var(--border-navy)}
.hero-stat:last-child{border-right:none}
.stat-val{font-family:var(--font-serif);font-size:28px;font-weight:700;color:var(--white);line-height:1}
.stat-label{font-size:10px;color:var(--text-nav-soft);letter-spacing:.1em;text-transform:uppercase;margin-top:4px}

/* ── TERMINAL ── */
.terminal-wrap{position:relative;z-index:1}
.terminal{background:#0a0f1a;border:1px solid rgba(255,255,255,0.1);border-radius:var(--radius-xl);overflow:hidden;box-shadow:0 32px 80px rgba(0,0,0,0.5),0 0 0 1px rgba(46,111,218,0.15);font-family:var(--font-mono)}
.term-bar{background:#131c2e;padding:14px 18px;display:flex;align-items:center;gap:10px;border-bottom:1px solid rgba(255,255,255,0.06)}
.term-dots{display:flex;gap:7px}
.term-dot{width:12px;height:12px;border-radius:50%}
.term-title{flex:1;text-align:center;font-size:11px;color:rgba(255,255,255,0.3);letter-spacing:.12em;font-family:var(--font-mono)}
.term-badge{font-size:9px;padding:3px 10px;border-radius:100px;background:rgba(74,222,128,0.1);color:#4ade80;border:1px solid rgba(74,222,128,0.2);letter-spacing:.08em}
.term-body{padding:22px 24px;min-height:320px;position:relative}
.term-line{display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;font-size:12px;line-height:1.7;animation:termFade .3s ease}
@keyframes termFade{from{opacity:0;transform:translateX(-4px)}to{opacity:1;transform:translateX(0)}}
.term-prompt{color:#4ade80;flex-shrink:0;user-select:none}
.term-cmd{color:#e2e8f0}
.term-output{color:#94a3b8;padding-left:20px;font-size:11.5px}
.term-output.success{color:#4ade80}
.term-output.info{color:#60a5fa}
.term-output.warn{color:#fbbf24}
.term-output.highlight{color:#f0a500}
.term-cursor{display:inline-block;width:8px;height:14px;background:#4ade80;animation:blink .9s step-end infinite;vertical-align:middle;margin-left:2px;border-radius:1px}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
.term-progress{margin:8px 0 8px 20px;display:flex;align-items:center;gap:10px}
.term-pb-track{flex:1;height:4px;background:rgba(255,255,255,0.08);border-radius:2px;overflow:hidden;max-width:200px}
.term-pb-fill{height:100%;background:linear-gradient(90deg,#2e6fda,#4ade80);border-radius:2px;transition:width .4s ease}
.term-pb-pct{font-size:10px;color:#60a5fa;font-family:var(--font-mono)}

/* ── FEATURES ── */
.features-sec{padding:88px 48px;max-width:1200px;margin:0 auto;width:100%}
.sec-label{font-size:10px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);margin-bottom:12px}
.sec-title{font-family:var(--font-serif);font-size:38px;font-weight:700;color:var(--text-dark);line-height:1.2;margin-bottom:10px}
.sec-title em{font-style:italic;color:var(--accent)}
.sec-sub{font-size:14px;color:var(--text-soft);max-width:520px;line-height:1.7}
.sec-header{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:52px;flex-wrap:wrap;gap:20px}
.features-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}

/* ── 3D FEATURE CARDS ── */
.feat-card-3d{perspective:1000px}
.feat-card-inner{background:var(--white);border:1px solid var(--border-light);border-radius:var(--radius-xl);padding:34px;transition:transform .45s cubic-bezier(.23,1,.32,1),box-shadow .45s ease,border-color .3s;cursor:pointer;position:relative;overflow:hidden;transform-style:preserve-3d;will-change:transform}
.feat-card-inner:hover{box-shadow:0 28px 70px rgba(13,27,46,0.16),0 0 0 1px rgba(46,111,218,0.15);border-color:rgba(46,111,218,0.2)}
.feat-card-inner::after{content:'';position:absolute;inset:0;border-radius:var(--radius-xl);background:radial-gradient(circle at var(--mx,50%) var(--my,50%),rgba(46,111,218,0.06),transparent 60%);opacity:0;transition:opacity .3s;pointer-events:none}
.feat-card-inner:hover::after{opacity:1}
.feat-shine{position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,transparent,var(--accent),transparent);transform:scaleX(0);transition:transform .4s cubic-bezier(.23,1,.32,1);transform-origin:left;border-radius:0}
.feat-card-inner:hover .feat-shine{transform:scaleX(1)}
.feat-icon-wrap{width:54px;height:54px;border-radius:14px;display:flex;align-items:center;justify-content:center;margin-bottom:22px}
.feat-title{font-family:var(--font-serif);font-size:20px;font-weight:700;color:var(--text-dark);margin-bottom:10px}
.feat-desc{font-size:13px;color:var(--text-soft);line-height:1.75}
.feat-tag{display:inline-flex;align-items:center;gap:6px;margin-top:18px;padding:5px 13px;border-radius:100px;font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.feat-tech{display:flex;gap:6px;margin-top:14px;flex-wrap:wrap}
.feat-pill{padding:3px 10px;border-radius:100px;font-size:9px;font-weight:600;letter-spacing:.08em;background:var(--surface);color:var(--text-mid);border:1px solid var(--border-light);font-family:var(--font-mono)}

/* ── AGENT FLOW SECTION ── */
.flow-sec{padding:88px 48px;background:var(--navy-900);position:relative;overflow:hidden}
.flow-sec-inner{max-width:1200px;margin:0 auto}
.flow-sec .sec-label{color:var(--accent-light)}
.flow-sec .sec-title{color:var(--white)}
.flow-sec .sec-title em{color:var(--gold)}
.flow-sec .sec-sub{color:var(--text-nav-soft)}
.flow-grid{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;margin-top:52px}
.agent-list{display:flex;flex-direction:column;gap:10px}
.agent-row{display:flex;align-items:center;gap:14px;padding:14px 18px;border-radius:var(--radius);border:1px solid rgba(255,255,255,0.06);background:rgba(255,255,255,0.03);cursor:pointer;transition:all .25s;position:relative;overflow:hidden}
.agent-row::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;border-radius:0 2px 2px 0;background:var(--accent);transform:scaleY(0);transition:transform .25s}
.agent-row:hover,.agent-row.active{background:rgba(46,111,218,0.08);border-color:rgba(46,111,218,0.25)}
.agent-row:hover::before,.agent-row.active::before{transform:scaleY(1)}
.agent-num{width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:var(--text-nav-soft);font-family:var(--font-mono);flex-shrink:0;transition:all .25s}
.agent-row:hover .agent-num,.agent-row.active .agent-num{background:var(--accent);border-color:var(--accent);color:white}
.agent-name{font-size:13px;font-weight:600;color:var(--text-nav);transition:color .2s}
.agent-row:hover .agent-name,.agent-row.active .agent-name{color:white}
.agent-desc{font-size:11px;color:var(--text-nav-soft);transition:color .2s;flex:1;text-align:right}
.agent-row:hover .agent-desc{color:var(--text-nav)}
.agent-arrow{font-size:10px;color:var(--accent-light);opacity:0;transform:translateX(-4px);transition:all .2s}
.agent-row:hover .agent-arrow,.agent-row.active .agent-arrow{opacity:1;transform:translateX(0)}
.flow-detail{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:var(--radius-xl);padding:32px;min-height:380px;transition:all .3s}
.flow-detail-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 14px;border-radius:100px;font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:18px}
.flow-detail-title{font-family:var(--font-serif);font-size:24px;font-weight:700;color:white;margin-bottom:10px}
.flow-detail-desc{font-size:13px;color:var(--text-nav-soft);line-height:1.8;margin-bottom:24px}
.flow-detail-props{display:flex;flex-direction:column;gap:8px}
.flow-prop{display:flex;align-items:center;gap:10px;font-size:12px}
.flow-prop-key{color:var(--text-nav-soft);font-family:var(--font-mono);min-width:90px;font-size:11px}
.flow-prop-val{color:var(--accent-light);font-family:var(--font-mono);font-size:11px;padding:2px 8px;background:rgba(46,111,218,0.1);border-radius:4px;border:1px solid rgba(46,111,218,0.2)}
.flow-connector{display:flex;align-items:center;justify-content:center;padding:4px 0;gap:8px}
.flow-conn-line{flex:1;height:1px;background:rgba(255,255,255,0.08)}
.flow-conn-dot{width:6px;height:6px;border-radius:50%;background:rgba(46,111,218,0.5)}

/* ── TECH STACK CARDS ── */
.tech-sec{padding:88px 48px;max-width:1200px;margin:0 auto;width:100%}
.tech-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:52px}
.tech-card{background:var(--white);border:1px solid var(--border-light);border-radius:var(--radius-xl);padding:28px 24px;transition:all .3s;cursor:default;position:relative;overflow:hidden;text-align:center}
.tech-card:hover{transform:translateY(-6px) scale(1.02);box-shadow:0 24px 60px rgba(13,27,46,0.14);border-color:rgba(46,111,218,0.2)}
.tech-card::before{content:'';position:absolute;inset:0;background:radial-gradient(circle at 50% 0%,var(--glow-color,rgba(46,111,218,0.06)),transparent 60%);opacity:0;transition:opacity .3s}
.tech-card:hover::before{opacity:1}
.tech-icon{width:56px;height:56px;border-radius:16px;display:flex;align-items:center;justify-content:center;margin:0 auto 16px}
.tech-name{font-family:var(--font-serif);font-size:17px;font-weight:700;color:var(--text-dark);margin-bottom:6px}
.tech-role{font-size:11px;color:var(--text-soft);line-height:1.6;margin-bottom:14px}
.tech-badge{display:inline-flex;padding:3px 10px;border-radius:100px;font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}

/* ── HOW IT WORKS ── */
.how-sec{padding:88px 48px;background:var(--navy-900);position:relative;overflow:hidden}
.how-sec-inner{max-width:1200px;margin:0 auto}
.how-sec .sec-label{color:var(--accent-light)}
.how-sec .sec-title{color:var(--white)}
.how-sec .sec-title em{color:var(--gold)}
.steps-row{display:grid;grid-template-columns:repeat(3,1fr);gap:0;position:relative;margin-top:56px}
.steps-row::before{content:'';position:absolute;top:38px;left:calc(16.6% + 24px);right:calc(16.6% + 24px);height:1px;background:rgba(255,255,255,0.08);z-index:0}
.step-item{text-align:center;padding:0 28px;position:relative;z-index:1}
.step-num{width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 22px;font-family:var(--font-serif);font-size:20px;font-weight:700;position:relative;transition:all .3s;cursor:default}
.step-num.s-idle{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.12);color:var(--text-nav-soft)}
.step-num.s-active{background:var(--accent);border:2px solid var(--accent);color:white;box-shadow:0 0 0 8px rgba(46,111,218,0.15)}
.step-num.s-done{background:var(--success);border:2px solid var(--success);color:white;box-shadow:0 0 0 8px rgba(26,158,106,0.12)}
.step-title{font-family:var(--font-serif);font-size:18px;font-weight:700;color:white;margin-bottom:10px}
.step-desc{font-size:13px;color:var(--text-nav-soft);line-height:1.75}
.step-sub-list{margin-top:14px;display:flex;flex-direction:column;gap:6px}
.step-sub-item{display:flex;align-items:center;gap:7px;font-size:11px;color:var(--text-nav-soft);justify-content:center}
.step-sub-dot{width:5px;height:5px;border-radius:50%;background:var(--accent-light);flex-shrink:0;opacity:.6}

/* ── ABOUT SECTION ── */
.about-sec{padding:88px 48px;max-width:1200px;margin:0 auto;width:100%}
.about-grid{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;margin-top:52px}
.about-left{}
.about-creator-card{background:var(--navy-900);border-radius:var(--radius-xl);padding:36px;position:relative;overflow:hidden}
.creator-header{display:flex;align-items:center;gap:18px;margin-bottom:24px}
.creator-avatar{width:72px;height:72px;border-radius:20px;background:linear-gradient(135deg,var(--accent),var(--navy-700));display:flex;align-items:center;justify-content:center;font-family:var(--font-serif);font-size:26px;font-weight:700;color:white;flex-shrink:0;border:2px solid rgba(46,111,218,0.4);box-shadow:0 8px 24px rgba(46,111,218,0.3)}
.creator-name{font-family:var(--font-serif);font-size:22px;font-weight:700;color:white}
.creator-title{font-size:11px;color:var(--accent-light);letter-spacing:.1em;margin-top:3px;text-transform:uppercase;font-weight:600}
.creator-bio{font-size:13px;color:var(--text-nav-soft);line-height:1.8;margin-bottom:24px}
.creator-stack{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:24px}
.creator-pill{padding:4px 12px;border-radius:100px;font-size:10px;font-weight:700;background:rgba(46,111,218,0.12);color:var(--accent-light);border:1px solid rgba(46,111,218,0.2);font-family:var(--font-mono)}
.creator-links{display:flex;gap:10px}
.creator-link{padding:9px 20px;border-radius:100px;font-size:11px;font-weight:700;letter-spacing:.06em;cursor:pointer;transition:all .2s;text-decoration:none;display:flex;align-items:center;gap:7px}
.creator-link.gh{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);color:var(--text-nav)}
.creator-link.gh:hover{background:rgba(255,255,255,0.1);color:white}
.about-right{}
.about-stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:28px}
.about-stat-card{background:var(--white);border:1px solid var(--border-light);border-radius:var(--radius-lg);padding:22px;transition:all .3s}
.about-stat-card:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.ast-val{font-family:var(--font-serif);font-size:32px;font-weight:700;color:var(--text-dark);line-height:1}
.ast-label{font-size:11px;color:var(--text-soft);margin-top:5px;letter-spacing:.04em}
.about-desc{font-size:14px;color:var(--text-soft);line-height:1.85}
.about-desc strong{color:var(--text-dark)}

/* ── CTA ── */
.cta-sec{background:var(--navy-800);padding:88px 48px;position:relative;overflow:hidden}
.cta-inner{max-width:700px;margin:0 auto;text-align:center;position:relative;z-index:1}
.cta-title{font-family:var(--font-serif);font-size:42px;font-weight:700;color:white;margin-bottom:18px;line-height:1.2}
.cta-title em{font-style:italic;color:var(--gold)}
.cta-sub{font-size:15px;color:var(--text-nav);margin-bottom:38px;line-height:1.8}
.cta-btns{display:flex;gap:14px;justify-content:center}
.cta-note{font-size:11px;color:var(--text-nav-soft);margin-top:18px;letter-spacing:.04em}

/* ── CHAT PAGE ── */
.hero{background:var(--navy-800);padding:28px 48px 32px;position:relative;overflow:hidden;border-bottom:1px solid rgba(255,255,255,.05)}
.hero-content-chat{position:relative;z-index:1}
.hero-ey{display:flex;align-items:center;gap:10px;font-size:10px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--accent-light);margin-bottom:10px}
.hero-ey-line{width:32px;height:1px;background:var(--accent-light);opacity:.5}
.hero-title{font-family:var(--font-serif);font-size:30px;font-weight:700;color:var(--white);line-height:1.2;margin-bottom:8px}
.hero-title em{font-style:italic;color:var(--gold)}
.hero-sub{font-size:13px;color:var(--text-nav);max-width:520px}
.chat-stats{display:flex;gap:32px;margin-top:20px}
.stat-num{font-family:var(--font-serif);font-size:22px;font-weight:700;color:var(--white);line-height:1}
.stat-lbl{font-size:10px;color:var(--text-nav-soft);letter-spacing:.1em;text-transform:uppercase;margin-top:3px}
.stat-div{width:1px;background:var(--border-navy)}
.main-grid{flex:1;display:grid;grid-template-columns:460px 1fr;max-width:1600px;margin:0 auto;width:100%;padding:32px 48px 40px;gap:28px;align-items:start}
.left-panel{position:sticky;top:88px;background:var(--white);border-radius:var(--radius-xl);border:1px solid var(--border-light);box-shadow:var(--shadow);overflow:hidden}
.lp-top{background:var(--navy-800);padding:28px 28px 24px;position:relative;overflow:hidden}
.lp-ey{font-size:9px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--accent-light);margin-bottom:8px;position:relative;z-index:1}
.lp-title{font-family:var(--font-serif);font-size:24px;font-weight:700;color:var(--white);line-height:1.2;position:relative;z-index:1}
.lp-sub{font-size:12px;color:var(--text-nav-soft);margin-top:5px;position:relative;z-index:1}
.step-bar{display:flex;align-items:center;gap:6px;margin-top:16px;position:relative;z-index:1}
.s-num{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700}
.s-num.done{background:var(--success);color:white}
.s-num.active{background:var(--accent);color:white;box-shadow:0 0 0 3px rgba(46,111,218,.3)}
.s-num.idle{background:rgba(255,255,255,.1);color:var(--text-nav-soft)}
.s-lbl{font-size:10px;letter-spacing:.06em;color:var(--text-nav-soft);font-weight:500}
.s-lbl.active{color:white}
.s-con{flex:1;height:1px;background:rgba(255,255,255,.1);max-width:20px}
.tab-bar{display:flex;border-bottom:1px solid var(--border-light)}
.tab-btn{flex:1;padding:15px 8px;display:flex;flex-direction:column;align-items:center;gap:5px;background:transparent;border:none;cursor:pointer;font-family:var(--font-sans);font-size:9px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--text-muted);transition:color .2s;position:relative}
.tab-btn::after{content:'';position:absolute;bottom:0;left:16px;right:16px;height:2px;background:var(--accent);border-radius:2px 2px 0 0;transform:scaleX(0);transition:transform .22s}
.tab-btn.active{color:var(--accent)}.tab-btn.active::after{transform:scaleX(1)}
.tab-btn:hover:not(.active){color:var(--text-mid)}
.tab-icon-box{width:28px;height:28px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:13px;background:var(--surface);transition:background .2s}
.tab-btn.active .tab-icon-box{background:var(--accent-dim);color:var(--accent)}
.upload-body{padding:24px 24px 0}
.drop-zone{border:2px dashed var(--border-light);border-radius:var(--radius-lg);padding:40px 24px;text-align:center;cursor:pointer;background:var(--off-white);transition:all .22s;position:relative;overflow:hidden}
.drop-zone:hover,.drop-zone.drag-over{border-color:var(--accent);border-style:solid;box-shadow:0 0 0 4px var(--accent-dim)}
.drop-title{font-family:var(--font-serif);font-size:16px;font-weight:600;color:var(--text-dark)}
.drop-sub{font-size:12px;color:var(--text-soft);margin-top:3px}
.type-pills{display:flex;gap:6px;justify-content:center;margin-top:12px}
.type-pill{padding:3px 10px;border-radius:100px;background:var(--surface-2);border:1px solid var(--border-light);font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--text-mid)}
.file-card{display:flex;align-items:center;gap:12px;padding:12px 14px;background:var(--off-white);border:1px solid var(--border-light);border-radius:var(--radius);animation:fadeUp .28s ease}
@keyframes fadeUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.file-badge{width:40px;height:40px;border-radius:10px;background:var(--navy-800);flex-shrink:0;display:flex;align-items:center;justify-content:center}
.file-info{flex:1;min-width:0}
.file-name{font-size:12px;font-weight:600;color:var(--text-dark);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.file-meta{font-size:10px;color:var(--text-soft);font-family:var(--font-mono);margin-top:2px}
.file-del{width:28px;height:28px;border-radius:var(--radius-sm);background:var(--error-dim);border:1px solid rgba(214,63,77,.15);color:var(--error);cursor:pointer;font-size:11px;display:flex;align-items:center;justify-content:center;transition:all .18s;flex-shrink:0}
.file-del:hover{background:var(--error);color:white}
.field-wrap{display:flex;align-items:center;gap:10px;padding:0 12px;background:var(--off-white);border:1.5px solid var(--border-light);border-radius:var(--radius);transition:all .2s}
.field-wrap:focus-within{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim);background:white}
.field-icon{color:var(--text-muted);font-size:12px;flex-shrink:0}
.field-input{flex:1;padding:12px 0;background:transparent;border:none;outline:none;color:var(--text-dark);font-family:var(--font-sans);font-size:13px}
.field-input::placeholder{color:var(--text-muted)}
.field-ta{width:100%;padding:14px 16px;min-height:160px;background:var(--off-white);border:1.5px solid var(--border-light);border-radius:var(--radius);color:var(--text-dark);font-family:var(--font-sans);font-size:13px;resize:vertical;outline:none;transition:all .2s;line-height:1.6}
.field-ta:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim);background:white}
.field-ta::placeholder{color:var(--text-muted)}
.proc-sec{padding:20px 24px 24px}
.proc-sep{height:1px;background:var(--border-light);margin:0 0 20px}
.proc-btn{width:100%;padding:16px 20px;background:var(--navy-900);border:none;border-radius:var(--radius);color:white;font-family:var(--font-sans);font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;cursor:pointer;display:flex;align-items:center;justify-content:center;gap:10px;transition:all .22s;position:relative;overflow:hidden;box-shadow:0 4px 16px rgba(13,27,46,.25)}
.proc-btn::before{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent);transition:left .5s}
.proc-btn:hover::before{left:100%}
.proc-btn:hover{background:var(--navy-700);transform:translateY(-2px);box-shadow:0 8px 24px rgba(13,27,46,.3)}
.btn-ring{width:28px;height:28px;border-radius:7px;background:rgba(46,111,218,.3);display:flex;align-items:center;justify-content:center}
.status-card{display:flex;align-items:center;gap:14px;padding:15px 16px;border-radius:var(--radius);border:1px solid var(--border-light);background:var(--off-white)}
.sc-ic{width:44px;height:44px;border-radius:12px;flex-shrink:0;display:flex;align-items:center;justify-content:center}
.sc-ic.proc{background:rgba(46,111,218,.1);border:1px solid rgba(46,111,218,.2)}
.sc-ic.ready{background:var(--success-dim);border:1px solid rgba(26,158,106,.2)}
.sc-t{font-size:13px;font-weight:600;color:var(--text-dark)}
.sc-s{font-size:10px;color:var(--text-soft);font-family:var(--font-mono);margin-top:3px}
.spinner{width:18px;height:18px;border:2px solid rgba(46,111,218,.2);border-top-color:var(--accent);border-radius:50%;animation:spin .75s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.right-panel{background:var(--white);border-radius:var(--radius-xl);border:1px solid var(--border-light);box-shadow:var(--shadow);display:flex;flex-direction:column;min-height:640px;position:relative;overflow:hidden}
.chat-overlay{position:absolute;inset:0;z-index:20;background:rgba(247,248,252,.92);backdrop-filter:blur(6px);display:flex;align-items:center;justify-content:center;animation:fadeIn .3s ease}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.overlay-box{text-align:center;padding:40px 32px;background:var(--white);border-radius:var(--radius-xl);border:1px solid var(--border-light);box-shadow:var(--shadow);max-width:320px}
.ov-ic{width:64px;height:64px;border-radius:var(--radius-lg);background:var(--navy-800);margin:0 auto 16px;display:flex;align-items:center;justify-content:center}
.ov-title{font-family:var(--font-serif);font-size:22px;font-weight:700;color:var(--text-dark);margin-bottom:8px}
.ov-sub{font-size:12px;color:var(--text-soft);line-height:1.6}
.chat-hdr{background:var(--navy-900);padding:18px 24px;display:flex;align-items:center;justify-content:space-between;border-radius:var(--radius-xl) var(--radius-xl) 0 0;position:relative;overflow:hidden;flex-shrink:0}
.ch-info{display:flex;align-items:center;gap:12px;position:relative;z-index:1}
.ch-ic{width:36px;height:36px;border-radius:10px;background:rgba(46,111,218,.25);border:1px solid rgba(46,111,218,.35);display:flex;align-items:center;justify-content:center}
.ch-title{font-family:var(--font-serif);font-size:17px;font-weight:700;color:white}
.ch-sub{font-size:10px;color:var(--text-nav-soft);letter-spacing:.08em;margin-top:1px}
.ch-acts{display:flex;gap:8px;position:relative;z-index:1}
.ch-btn{width:32px;height:32px;border-radius:8px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);color:var(--text-nav-soft);cursor:pointer;font-size:12px;display:flex;align-items:center;justify-content:center;transition:all .18s}
.ch-btn:hover{background:rgba(214,63,77,.2);border-color:rgba(214,63,77,.3);color:#ff8090}
.msgs{flex:1;overflow-y:auto;padding:28px;display:flex;flex-direction:column;gap:18px}
.welcome-wrap{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 20px;text-align:center}
.welcome-svg{margin-bottom:20px;animation:floatRing 5s ease-in-out infinite}
@keyframes floatRing{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.w-title{font-family:var(--font-serif);font-size:26px;font-weight:700;color:var(--text-dark)}
.w-sub{font-size:13px;color:var(--text-soft);max-width:320px;margin:8px auto 0}
.w-chips{display:flex;gap:8px;margin-top:20px;flex-wrap:wrap;justify-content:center}
.w-chip{padding:5px 12px;border-radius:100px;background:var(--surface);border:1px solid var(--border-light);font-size:10px;font-weight:600;color:var(--text-mid);letter-spacing:.06em;display:flex;align-items:center;gap:5px}
.msg-row{display:flex;gap:10px;max-width:86%;animation:fadeUp .26s ease}
.msg-row.user{align-self:flex-end;flex-direction:row-reverse}
.msg-row.bot{align-self:flex-start}
.msg-av{width:32px;height:32px;border-radius:9px;flex-shrink:0;display:flex;align-items:center;justify-content:center}
.msg-av.user{background:var(--navy-900)}
.msg-av.bot{background:var(--surface);border:1px solid var(--border-light)}
.msg-bub{padding:12px 16px;border-radius:var(--radius);font-size:13.5px;line-height:1.7}
.msg-bub.user{background:var(--navy-900);color:white;border-radius:var(--radius) var(--radius) 4px var(--radius);box-shadow:0 4px 16px rgba(13,27,46,.2)}
.msg-bub.bot{background:var(--off-white);border:1px solid var(--border-light);color:var(--text-dark);border-radius:var(--radius) var(--radius) var(--radius) 4px}
.msg-bub strong{color:var(--accent);font-weight:600}
.msg-bub ul,.msg-bub ol{padding-left:18px;margin:6px 0}
.msg-bub li{margin-bottom:3px}
.msg-bub p{margin-bottom:8px}
.msg-bub p:last-child{margin-bottom:0}
.src-tag{display:inline-flex;align-items:center;gap:5px;margin-top:9px;padding:3px 10px;border-radius:100px;font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase}
.src-tag.doc{background:var(--success-dim);color:var(--success);border:1px solid rgba(26,158,106,.2)}
.src-tag.wiki{background:var(--accent-dim);color:var(--accent);border:1px solid rgba(46,111,218,.2)}
.typing-ind{display:flex;gap:4px;padding:4px 2px}
.typing-ind span{width:7px;height:7px;border-radius:50%;background:var(--text-muted);animation:tyBounce 1.1s ease-in-out infinite}
.typing-ind span:nth-child(2){animation-delay:.18s}
.typing-ind span:nth-child(3){animation-delay:.36s}
@keyframes tyBounce{0%,80%,100%{transform:translateY(0);opacity:.35}40%{transform:translateY(-6px);opacity:1}}
.chat-input-bar{padding:16px 24px 20px;background:var(--white);border-top:1px solid var(--border-light);flex-shrink:0}
.chat-field{display:flex;align-items:flex-end;gap:10px;background:var(--off-white);border:1.5px solid var(--border-light);border-radius:var(--radius-lg);padding:10px 12px;transition:all .2s}
.chat-field:focus-within{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-dim);background:white}
.chat-ta{flex:1;background:transparent;border:none;outline:none;color:var(--text-dark);font-family:var(--font-sans);font-size:13.5px;resize:none;line-height:1.6;min-height:22px;max-height:100px}
.chat-ta::placeholder{color:var(--text-muted)}
.chat-ta:disabled{cursor:not-allowed}
.send-btn{width:38px;height:38px;border-radius:10px;border:none;cursor:pointer;background:var(--navy-900);color:white;flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:all .2s;box-shadow:0 2px 10px rgba(13,27,46,.2)}
.send-btn:hover:not(:disabled){background:var(--navy-700);transform:scale(1.05)}
.send-btn:disabled{opacity:.35;cursor:not-allowed;transform:none}
.input-hint{font-size:10px;color:var(--text-muted);text-align:center;margin-top:8px;letter-spacing:.04em}
.footer{background:var(--navy-900);padding:20px 48px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,.04)}
.ft-left{display:flex;align-items:center;gap:12px}
.ft-logo{font-family:var(--font-serif);font-size:15px;font-weight:700;color:white}
.ft-div{width:1px;height:16px;background:rgba(255,255,255,.1)}
.ft-copy{font-size:11px;color:var(--text-nav-soft)}
.ft-cred{font-size:11px;color:var(--text-nav-soft)}
.ft-cred strong{color:var(--accent-light);font-weight:600}
.toast-stack{position:fixed;bottom:24px;right:24px;z-index:999;display:flex;flex-direction:column;gap:8px}
.toast{display:flex;align-items:center;gap:10px;padding:11px 16px;border-radius:var(--radius);min-width:220px;font-size:12px;font-weight:600;border:1px solid transparent;animation:toastIn .28s ease;box-shadow:var(--shadow)}
@keyframes toastIn{from{opacity:0;transform:translateX(16px)}to{opacity:1;transform:translateX(0)}}
.toast.success{background:rgba(26,158,106,.95);color:white}
.toast.error{background:rgba(214,63,77,.95);color:white}
.toast.info{background:rgba(46,111,218,.95);color:white}
@media(max-width:1100px){
  .main-grid{grid-template-columns:1fr;padding:16px 20px}
  .hero-content{grid-template-columns:1fr}
  .terminal-wrap{display:none}
  .features-grid{grid-template-columns:1fr}
  .tech-grid{grid-template-columns:1fr 1fr}
  .flow-grid{grid-template-columns:1fr}
  .steps-row{grid-template-columns:1fr}
  .about-grid{grid-template-columns:1fr}
  .home-hero{padding:60px 24px 70px}
  .features-sec,.tech-sec,.about-sec{padding:60px 24px}
  .flow-sec,.how-sec,.cta-sec{padding:60px 24px}
  .hdr{padding:0 20px}
}
`

// ─── TERMINAL ANIMATION HOOK ─────────────────────────────────────────────────
function useTerminal() {
  const SEQUENCE = [
    { type: 'cmd', text: 'docmind ingest --file research_paper.pdf' },
    { type: 'out', text: '→ ToolRouterAgent: file detected, routing to ingestion', cls: 'info' },
    { type: 'out', text: '→ IngestionAgent: loading PDF with PyMuPDF...', cls: 'info' },
    { type: 'progress', pct: 35, label: 'chunking' },
    { type: 'out', text: '→ TextSplitter: 47 chunks (size=400, overlap=80)', cls: 'success' },
    { type: 'out', text: '→ EmbeddingService: all-MiniLM-L6-v2 encoding...', cls: 'info' },
    { type: 'progress', pct: 72, label: 'embedding' },
    { type: 'out', text: '→ VectorStoreService: ChromaDB indexed 47 chunks', cls: 'success' },
    { type: 'out', text: '✓ PlannerAgent: has_documents() = True', cls: 'success' },
    { type: 'blank' },
    { type: 'cmd', text: 'docmind query "What model is used for embeddings?"' },
    { type: 'out', text: '→ RetrieverAgent: cosine search k=6, threshold=1.8', cls: 'info' },
    { type: 'progress', pct: 90, label: 'retrieving' },
    { type: 'out', text: '→ Retrieved 4 chunks · avg_score=0.42', cls: 'success' },
    { type: 'out', text: '→ LLMAnswerAgent: Groq llama-3.3-70b generating...', cls: 'info' },
    { type: 'progress', pct: 100, label: 'generating' },
    { type: 'out', text: '→ source: rag · 1.1s · ExecutorAgent finalizing', cls: 'highlight' },
    { type: 'out', text: '"The system uses all-MiniLM-L6-v2 from HuggingFace"', cls: 'success' },
  ]
  const [lines, setLines] = useState([])
  const [cursor, setCursor] = useState(true)
  const idxRef = useRef(0)
  const timerRef = useRef(null)

  useEffect(() => {
    const delays = [400, 300, 400, 800, 500, 400, 800, 500, 400, 200, 400, 400, 700, 500, 500, 800, 400, 500]
    const run = () => {
      const i = idxRef.current
      if (i >= SEQUENCE.length) {
        timerRef.current = setTimeout(() => {
          setLines([])
          idxRef.current = 0
          run()
        }, 3000)
        return
      }
      setLines(prev => [...prev, SEQUENCE[i]])
      idxRef.current = i + 1
      timerRef.current = setTimeout(run, delays[i] || 400)
    }
    timerRef.current = setTimeout(run, 600)
    return () => clearTimeout(timerRef.current)
  }, [])

  useEffect(() => {
    const t = setInterval(() => setCursor(c => !c), 530)
    return () => clearInterval(t)
  }, [])

  return { lines, cursor }
}

// ─── AGENT DATA ──────────────────────────────────────────────────────────────
const AGENTS = [
  {
    num: '01', name: 'ToolRouterAgent', short: 'Entry point',
    color: '#4d8af0', bg: 'rgba(46,111,218,0.15)', border: 'rgba(46,111,218,0.35)',
    desc: 'First node in the LangGraph DAG. Examines incoming state for file_content and file_type. Routes to IngestionAgent if new content is present, otherwise jumps directly to PlannerAgent.',
    props: [
      { key: 'input_state', val: 'file_type, file_content' },
      { key: 'routes_to', val: 'ingestion | planner' },
      { key: 'pattern', val: 'conditional edge' },
    ]
  },
  {
    num: '02', name: 'IngestionAgent', short: 'Load → Chunk → Store',
    color: '#1a9e6a', bg: 'rgba(26,158,106,0.15)', border: 'rgba(26,158,106,0.35)',
    desc: 'Orchestrates the full document pipeline: DocumentLoader (PDF/DOCX/TXT/URL) → RecursiveCharacterTextSplitter (chunk=400, overlap=80) → VectorStoreService.clear() + add_documents().',
    props: [
      { key: 'loaders', val: 'PyMuPDF, Docx2txt, TextLoader, WebBase' },
      { key: 'chunk_size', val: '400 chars · overlap=80' },
      { key: 'output', val: 'chunks_added, metadata' },
    ]
  },
  {
    num: '03', name: 'PlannerAgent', short: 'Decides retrieval path',
    color: '#e8a930', bg: 'rgba(232,169,48,0.15)', border: 'rgba(232,169,48,0.35)',
    desc: 'Inspects VectorStoreService.has_documents(). If the store is populated, routes to RetrieverAgent for semantic search. If empty, jumps directly to FallbackAgent for Wikipedia search.',
    props: [
      { key: 'checks', val: 'vector_store.has_documents()' },
      { key: 'routes_to', val: 'retriever | fallback' },
      { key: 'pattern', val: 'route_after_planner()' },
    ]
  },
  {
    num: '04', name: 'RetrieverAgent', short: 'Semantic similarity search',
    color: '#8b5cf6', bg: 'rgba(139,92,246,0.15)', border: 'rgba(139,92,246,0.35)',
    desc: 'Runs ChromaDB cosine similarity search (k=6, threshold=1.8). Applies two-gate scoring: per-chunk filter at ≤1.8, aggregate quality check at avg_score ≤1.6. Safety-net returns top 2 chunks if all fail.',
    props: [
      { key: 'k', val: '6 chunks retrieved' },
      { key: 'threshold', val: 'cosine ≤ 1.8' },
      { key: 'fallback_gate', val: 'avg_score > 1.6' },
    ]
  },
  {
    num: '05', name: 'LLMAnswerAgent', short: 'Groq generation',
    color: '#f0a500', bg: 'rgba(240,165,0,0.15)', border: 'rgba(240,165,0,0.35)',
    desc: 'Calls Groq llama-3.3-70b-versatile with retrieved context. Supports multi-turn history (last 5 turns). Detects 7 negative patterns in the response — if found, clears context and routes to FallbackAgent.',
    props: [
      { key: 'model', val: 'llama-3.3-70b-versatile' },
      { key: 'temp', val: '0.1 · history: last 5' },
      { key: 'fallback_trigger', val: '7 negative patterns' },
    ]
  },
  {
    num: '06', name: 'FallbackAgent', short: 'Wikipedia search',
    color: '#4d8af0', bg: 'rgba(77,138,240,0.15)', border: 'rgba(77,138,240,0.35)',
    desc: 'Activates when document context is absent or the LLM answer is negative. Uses LangChain WikipediaQueryRun (top_k=3, max 2000 chars/result). Always routes to ExecutorAgent after.',
    props: [
      { key: 'provider', val: 'WikipediaQueryRun' },
      { key: 'top_k', val: '3 results · 2000 chars' },
      { key: 'source_tag', val: 'wikipedia' },
    ]
  },
  {
    num: '07', name: 'ExecutorAgent', short: 'Final node → END',
    color: '#1a9e6a', bg: 'rgba(26,158,106,0.15)', border: 'rgba(26,158,106,0.35)',
    desc: 'Final node in the graph. Formats the answer, handles error states gracefully, appends to conversation history, and sets next_agent=END to terminate the LangGraph StateGraph execution.',
    props: [
      { key: 'output', val: 'answer, source, history' },
      { key: 'error_handle', val: 'injects fallback message' },
      { key: 'terminates', val: 'next_agent = END' },
    ]
  },
]

// ─── SVG ICONS ────────────────────────────────────────────────────────────────
const LogoSVG = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <rect x="2" y="2" width="7" height="9" rx="1.5" fill="white" opacity="0.9"/>
    <rect x="11" y="2" width="7" height="4" rx="1.5" fill="white" opacity="0.6"/>
    <rect x="11" y="8" width="7" height="5" rx="1.5" fill="white" opacity="0.6"/>
    <rect x="2" y="13" width="16" height="4" rx="1.5" fill="white" opacity="0.4"/>
  </svg>
)
const HdrBg = () => (
  <svg style={{position:'absolute',right:0,top:0,height:'100%',opacity:.07,pointerEvents:'none'}} viewBox="0 0 600 66" fill="none">
    <circle cx="550" cy="33" r="80" stroke="white" strokeWidth="0.5"/>
    <circle cx="550" cy="33" r="50" stroke="white" strokeWidth="0.5"/>
    <circle cx="550" cy="33" r="25" stroke="white" strokeWidth="0.5"/>
    {[...Array(12)].map((_,i)=>(<circle key={i} cx={410+(i%6)*32} cy={14+Math.floor(i/6)*24} r="1.5" fill="white"/>))}
  </svg>
)
const HomeHeroBg = () => (
  <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',pointerEvents:'none'}} viewBox="0 0 1400 500" preserveAspectRatio="xMaxYMid slice" fill="none">
    {[...Array(60)].map((_,i)=>(<circle key={i} cx={700+(i%12)*56} cy={20+Math.floor(i/12)*40} r="1.5" fill="white" opacity="0.18"/>))}
    <circle cx="1250" cy="250" r="200" stroke="white" strokeWidth="0.5" opacity="0.05"/>
    <circle cx="1250" cy="250" r="130" stroke="white" strokeWidth="0.5" opacity="0.06"/>
    <circle cx="1250" cy="250" r="65" stroke="white" strokeWidth="0.4" opacity="0.07"/>
    <polygon points="1340,80 1380,58 1420,80 1420,124 1380,146 1340,124" stroke="white" strokeWidth="0.8" opacity="0.08"/>
    <polygon points="1280,160 1310,143 1340,160 1340,194 1310,211 1280,194" stroke="white" strokeWidth="0.6" opacity="0.06"/>
  </svg>
)
const ArrowSVG = () => (
  <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
    <path d="M1 6.5 L12 6.5 M7.5 2 L12 6.5 L7.5 11" stroke="white" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
)
const SendSVG = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <path d="M1 7 L13 7 M8 2 L13 7 L8 12" stroke="white" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
)
const DropSVG = () => (
  <svg width="58" height="58" viewBox="0 0 58 58" fill="none" style={{margin:'0 auto 14px',display:'block'}}>
    <circle cx="29" cy="29" r="27" stroke="var(--accent)" strokeWidth="1.5" strokeDasharray="5 4" opacity="0.3"/>
    <circle cx="29" cy="29" r="19" fill="var(--accent-dim)"/>
    <path d="M22 30 L29 22 L36 30" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <line x1="29" y1="22" x2="29" y2="39" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/>
    <line x1="23" y1="39" x2="35" y2="39" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" opacity="0.5"/>
  </svg>
)
const FileIconSVG = () => (
  <svg width="18" height="22" viewBox="0 0 18 22" fill="none">
    <path d="M2 2a1 1 0 011-1h8l5 5v14a1 1 0 01-1 1H3a1 1 0 01-1-1V2z" fill="rgba(46,111,218,0.2)" stroke="var(--accent-light)" strokeWidth="1.2"/>
    <path d="M11 1v5h5" stroke="var(--accent-light)" strokeWidth="1.2"/>
    <line x1="5" y1="11" x2="13" y2="11" stroke="var(--accent-light)" strokeWidth="1.2" strokeLinecap="round"/>
    <line x1="5" y1="14" x2="13" y2="14" stroke="var(--accent-light)" strokeWidth="1.2" strokeLinecap="round"/>
    <line x1="5" y1="17" x2="9" y2="17" stroke="var(--accent-light)" strokeWidth="1.2" strokeLinecap="round"/>
  </svg>
)
const LockSVG = () => (
  <svg width="30" height="30" viewBox="0 0 30 30" fill="none">
    <rect x="5" y="13" width="20" height="15" rx="3" fill="rgba(46,111,218,0.15)" stroke="var(--accent-light)" strokeWidth="1.5"/>
    <path d="M9 13V10Q9 4 15 4Q21 4 21 10V13" stroke="var(--accent-light)" strokeWidth="1.8" strokeLinecap="round"/>
    <circle cx="15" cy="20" r="2.5" fill="var(--accent-light)"/>
    <line x1="15" y1="22.5" x2="15" y2="25" stroke="var(--accent-light)" strokeWidth="1.5" strokeLinecap="round"/>
  </svg>
)
const CheckSVG = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
    <circle cx="9" cy="9" r="8" stroke="var(--success)" strokeWidth="1.5"/>
    <path d="M5 9 L8 12 L13 6" stroke="var(--success)" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
)
const ChatIconSVG = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
    <path d="M2 3a1 1 0 011-1h10a1 1 0 011 1v7a1 1 0 01-1 1H9l-3 3v-3H3a1 1 0 01-1-1V3z" fill="rgba(46,111,218,0.4)" stroke="var(--accent-light)" strokeWidth="1.2"/>
    <line x1="5" y1="6" x2="11" y2="6" stroke="var(--accent-light)" strokeWidth="1.1" strokeLinecap="round"/>
    <line x1="5" y1="8.5" x2="9" y2="8.5" stroke="var(--accent-light)" strokeWidth="1.1" strokeLinecap="round"/>
  </svg>
)
const BotSVG = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
    <rect x="3" y="5" width="10" height="8" rx="2" fill="var(--accent)" opacity="0.85"/>
    <rect x="5.5" y="2" width="5" height="2.5" rx="1.2" fill="var(--accent)" opacity="0.6"/>
    <line x1="8" y1="4.5" x2="8" y2="5" stroke="var(--accent)" strokeWidth="1.2"/>
    <circle cx="5.5" cy="8.5" r="1.2" fill="white"/>
    <circle cx="10.5" cy="8.5" r="1.2" fill="white"/>
    <rect x="5.5" y="10.5" width="5" height="1" rx="0.5" fill="white" opacity="0.7"/>
    <line x1="1" y1="9" x2="3" y2="9" stroke="var(--accent)" strokeWidth="1.2" strokeLinecap="round"/>
    <line x1="13" y1="9" x2="15" y2="9" stroke="var(--accent)" strokeWidth="1.2" strokeLinecap="round"/>
  </svg>
)
const UserSVG = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
    <circle cx="7" cy="4.5" r="2.5" fill="rgba(255,255,255,0.85)"/>
    <path d="M2 12 Q2 8.5 7 8.5 Q12 8.5 12 12" stroke="rgba(255,255,255,0.85)" strokeWidth="1.5" fill="none" strokeLinecap="round"/>
  </svg>
)
const WelcomeSVG = () => (
  <svg className="welcome-svg" width="92" height="92" viewBox="0 0 92 92" fill="none">
    <circle cx="46" cy="46" r="44" stroke="var(--border-light)" strokeWidth="1.5"/>
    <circle cx="46" cy="46" r="33" stroke="var(--accent)" strokeWidth="1.5" strokeDasharray="7 5" opacity="0.35"/>
    <circle cx="46" cy="46" r="21" fill="var(--accent-dim)"/>
    <path d="M46 30 L49 43 L46 46 L43 43 Z" fill="var(--accent)" opacity="0.75"/>
    <path d="M46 62 L49 49 L46 46 L43 49 Z" fill="var(--accent)" opacity="0.45"/>
    <path d="M30 46 L43 49 L46 46 L43 43 Z" fill="var(--accent)" opacity="0.45"/>
    <path d="M62 46 L49 49 L46 46 L49 43 Z" fill="var(--accent)" opacity="0.75"/>
    {[0,90,180,270].map((deg,i)=>{const r=(deg*Math.PI)/180;return <circle key={i} cx={46+43*Math.cos(r)} cy={46+43*Math.sin(r)} r="3.5" fill="var(--accent)" opacity="0.55"/>})}
  </svg>
)
const HeroBgSVG = () => (
  <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',pointerEvents:'none'}} viewBox="0 0 1200 120" preserveAspectRatio="xMaxYMid slice" fill="none">
    {[...Array(40)].map((_,i)=>(<circle key={i} cx={700+(i%10)*50} cy={15+Math.floor(i/10)*25} r="1.5" fill="white" opacity="0.25"/>))}
    <path d="M900 0 Q1100 60 900 120" stroke="white" strokeWidth="0.5" opacity="0.12"/>
    <path d="M980 0 Q1150 60 980 120" stroke="white" strokeWidth="0.5" opacity="0.08"/>
    <polygon points="1140,25 1165,12 1190,25 1190,52 1165,65 1140,52" stroke="white" strokeWidth="0.8" opacity="0.12"/>
  </svg>
)
const LpBgSVG = () => (
  <svg style={{position:'absolute',right:-10,bottom:-20,opacity:.06,pointerEvents:'none'}} width="140" height="120" viewBox="0 0 140 120" fill="none">
    {[...Array(20)].map((_,i)=>(<circle key={i} cx={(i%5)*22+10} cy={Math.floor(i/5)*22+10} r="2" fill="white"/>))}
    <polygon points="80,50 110,33 140,50 140,83 110,100 80,83" stroke="white" strokeWidth="0.8"/>
  </svg>
)
const ChtHdrBgSVG = () => (
  <svg style={{position:'absolute',right:0,top:0,height:'100%',opacity:.05,pointerEvents:'none'}} viewBox="0 0 500 72" fill="none">
    {[...Array(16)].map((_,i)=>(<circle key={i} cx={310+(i%8)*24} cy={12+Math.floor(i/8)*22} r="1.5" fill="white" opacity="0.5"/>))}
    <circle cx="455" cy="36" r="50" stroke="white" strokeWidth="0.6"/>
    <circle cx="455" cy="36" r="30" stroke="white" strokeWidth="0.6"/>
  </svg>
)

// ─── TECH CARD ICONS ──────────────────────────────────────────────────────────
const LangGraphIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
    <circle cx="7" cy="7" r="4" fill="rgba(46,111,218,0.3)" stroke="#4d8af0" strokeWidth="1.2"/>
    <circle cx="21" cy="7" r="4" fill="rgba(46,111,218,0.3)" stroke="#4d8af0" strokeWidth="1.2"/>
    <circle cx="14" cy="21" r="4" fill="rgba(46,111,218,0.6)" stroke="#4d8af0" strokeWidth="1.2"/>
    <circle cx="7" cy="7" r="1.5" fill="#4d8af0"/>
    <circle cx="21" cy="7" r="1.5" fill="#4d8af0"/>
    <circle cx="14" cy="21" r="1.5" fill="white"/>
    <line x1="7" y1="11" x2="14" y2="17" stroke="#4d8af0" strokeWidth="1" opacity="0.6"/>
    <line x1="21" y1="11" x2="14" y2="17" stroke="#4d8af0" strokeWidth="1" opacity="0.6"/>
    <line x1="11" y1="7" x2="17" y2="7" stroke="#4d8af0" strokeWidth="1" opacity="0.4"/>
  </svg>
)
const GroqIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
    <path d="M14 4 L24 9.5 V18.5 L14 24 L4 18.5 V9.5 Z" fill="rgba(232,169,48,0.15)" stroke="#e8a930" strokeWidth="1.2"/>
    <path d="M14 8 L20 11.5 V18.5 L14 22 L8 18.5 V11.5 Z" fill="rgba(232,169,48,0.25)"/>
    <circle cx="14" cy="15" r="3" fill="#e8a930" opacity="0.9"/>
    <line x1="14" y1="12" x2="14" y2="8" stroke="#e8a930" strokeWidth="1" opacity="0.5"/>
  </svg>
)
const ChromaIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
    <ellipse cx="14" cy="8" rx="10" ry="4" fill="rgba(139,92,246,0.2)" stroke="#8b5cf6" strokeWidth="1.2"/>
    <path d="M4 8 L4 14 Q4 18 14 18 Q24 18 24 14 L24 8" stroke="#8b5cf6" strokeWidth="1.2" fill="rgba(139,92,246,0.1)"/>
    <path d="M4 14 L4 20 Q4 24 14 24 Q24 24 24 20 L24 14" stroke="#8b5cf6" strokeWidth="1" fill="rgba(139,92,246,0.08)" opacity="0.6"/>
    <ellipse cx="14" cy="14" rx="10" ry="4" fill="none" stroke="#8b5cf6" strokeWidth="1" strokeDasharray="3 2" opacity="0.4"/>
  </svg>
)
const HFIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
    <circle cx="14" cy="15" r="9" fill="rgba(255,183,0,0.15)" stroke="#ffb700" strokeWidth="1.2"/>
    <circle cx="10" cy="12" r="2" fill="#ffb700" opacity="0.8"/>
    <circle cx="18" cy="12" r="2" fill="#ffb700" opacity="0.8"/>
    <path d="M9 17 Q14 21 19 17" stroke="#ffb700" strokeWidth="1.5" fill="none" strokeLinecap="round"/>
    <path d="M10 5 L10 9 M18 5 L18 9" stroke="#ffb700" strokeWidth="1.2" strokeLinecap="round" opacity="0.5"/>
    <path d="M8 7 L10 9 L12 7 M16 7 L18 9 L20 7" stroke="#ffb700" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round" opacity="0.5"/>
  </svg>
)
const WikiIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
    <circle cx="14" cy="14" r="10" fill="rgba(26,158,106,0.12)" stroke="#1a9e6a" strokeWidth="1.2"/>
    <ellipse cx="14" cy="14" rx="5" ry="10" fill="none" stroke="#1a9e6a" strokeWidth="1" opacity="0.5"/>
    <line x1="4" y1="14" x2="24" y2="14" stroke="#1a9e6a" strokeWidth="1" opacity="0.5"/>
    <line x1="5.5" y1="9" x2="22.5" y2="9" stroke="#1a9e6a" strokeWidth="0.8" opacity="0.3"/>
    <line x1="5.5" y1="19" x2="22.5" y2="19" stroke="#1a9e6a" strokeWidth="0.8" opacity="0.3"/>
  </svg>
)
const PydanticIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
    <rect x="5" y="5" width="18" height="18" rx="4" fill="rgba(214,63,77,0.12)" stroke="#d63f4d" strokeWidth="1.2"/>
    <line x1="9" y1="10" x2="19" y2="10" stroke="#d63f4d" strokeWidth="1.2" strokeLinecap="round"/>
    <line x1="9" y1="14" x2="16" y2="14" stroke="#d63f4d" strokeWidth="1.2" strokeLinecap="round" opacity="0.7"/>
    <line x1="9" y1="18" x2="13" y2="18" stroke="#d63f4d" strokeWidth="1.2" strokeLinecap="round" opacity="0.5"/>
    <circle cx="19" cy="18" r="3" fill="rgba(214,63,77,0.3)" stroke="#d63f4d" strokeWidth="1"/>
    <path d="M17.5 18 L18.5 19 L21 17" stroke="#d63f4d" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
)
const PyMuPDFIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
    <path d="M6 4 Q6 2 8 2 H18 L22 6 V24 Q22 26 20 26 H8 Q6 26 6 24 Z" fill="rgba(232,169,48,0.1)" stroke="#e8a930" strokeWidth="1.2"/>
    <path d="M18 2 V6 H22" stroke="#e8a930" strokeWidth="1.2"/>
    <line x1="10" y1="12" x2="18" y2="12" stroke="#e8a930" strokeWidth="1" strokeLinecap="round"/>
    <line x1="10" y1="15" x2="18" y2="15" stroke="#e8a930" strokeWidth="1" strokeLinecap="round" opacity="0.7"/>
    <line x1="10" y1="18" x2="14" y2="18" stroke="#e8a930" strokeWidth="1" strokeLinecap="round" opacity="0.5"/>
  </svg>
)
const PythonIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
    <path d="M14 4 C9 4 7 6 7 9 V13 H14 V14 H5 C2 14 2 17 4 20 L8 24 C9 25 11 24 11 22 V20 H17 V22 C17 24 19 25 20 24 L24 20 C26 17 26 14 23 14 H17 V13 H21 C21 10 19 4 14 4 Z" fill="rgba(46,111,218,0.15)" stroke="#4d8af0" strokeWidth="1"/>
    <circle cx="11" cy="8" r="1.5" fill="#4d8af0"/>
    <circle cx="17" cy="20" r="1.5" fill="#4d8af0" opacity="0.6"/>
  </svg>
)

// ─── 3D CARD COMPONENT ───────────────────────────────────────────────────────
function Card3D({ children, onClick }) {
  const ref = useRef(null)
  const handleMove = useCallback((e) => {
    const el = ref.current
    if (!el) return
    const rect = el.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    const cx = rect.width / 2
    const cy = rect.height / 2
    const rotX = ((y - cy) / cy) * -8
    const rotY = ((x - cx) / cx) * 8
    const pctX = (x / rect.width) * 100
    const pctY = (y / rect.height) * 100
    el.style.transform = `perspective(1000px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateZ(6px)`
    el.style.setProperty('--mx', `${pctX}%`)
    el.style.setProperty('--my', `${pctY}%`)
  }, [])
  const handleLeave = useCallback(() => {
    const el = ref.current
    if (!el) return
    el.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)'
  }, [])
  return (
    <div className="feat-card-3d" onClick={onClick}>
      <div className="feat-card-inner" ref={ref} onMouseMove={handleMove} onMouseLeave={handleLeave}>
        <div className="feat-shine"/>
        {children}
      </div>
    </div>
  )
}

// ─── ANIMATED TERMINAL ───────────────────────────────────────────────────────
function AnimatedTerminal({ onLaunch }) {
  const { lines, cursor } = useTerminal()
  const bodyRef = useRef(null)
  useEffect(() => {
    if (bodyRef.current) bodyRef.current.scrollTop = bodyRef.current.scrollHeight
  }, [lines])

  return (
    <div className="terminal-wrap">
      <div className="terminal">
        <div className="term-bar">
          <div className="term-dots">
            <div className="term-dot" style={{background:'#ff5f57'}}/>
            <div className="term-dot" style={{background:'#febc2e'}}/>
            <div className="term-dot" style={{background:'#28c840'}}/>
          </div>
          <div className="term-title">docmind — pipeline trace</div>
          <div className="term-badge">● live</div>
        </div>
        <div className="term-body" ref={bodyRef} style={{overflowY:'auto',maxHeight:340}}>
          {lines.map((line, i) => {
            if (line.type === 'blank') return <div key={i} style={{height:8}}/>
            if (line.type === 'cmd') return (
              <div key={i} className="term-line">
                <span className="term-prompt">$</span>
                <span className="term-cmd">{line.text}</span>
              </div>
            )
            if (line.type === 'out') return (
              <div key={i} className="term-line">
                <span className={`term-output ${line.cls||''}`}>{line.text}</span>
              </div>
            )
            if (line.type === 'progress') return (
              <div key={i} className="term-progress">
                <div className="term-pb-track">
                  <div className="term-pb-fill" style={{width:`${line.pct}%`}}/>
                </div>
                <span className="term-pb-pct">{line.pct}% {line.label}</span>
              </div>
            )
            return null
          })}
          <div className="term-line" style={{marginTop:4}}>
            <span className="term-prompt">$</span>
            <span className="term-cursor"/>
          </div>
        </div>
        <div style={{padding:'12px 24px 16px',borderTop:'1px solid rgba(255,255,255,0.06)',display:'flex',justifyContent:'space-between',alignItems:'center',background:'#0d1525'}}>
          <span style={{fontSize:10,color:'rgba(255,255,255,0.25)',fontFamily:'var(--font-mono)',letterSpacing:'.06em'}}>LangGraph · ChromaDB · Groq · 7 agents</span>
          <button onClick={onLaunch} style={{padding:'7px 18px',borderRadius:100,background:'var(--accent)',border:'none',color:'white',fontSize:10,fontWeight:700,cursor:'pointer',letterSpacing:'.06em',boxShadow:'0 4px 12px rgba(46,111,218,0.4)'}}>Try DocMind →</button>
        </div>
      </div>
    </div>
  )
}

// ─── AGENT FLOW SECTION ──────────────────────────────────────────────────────
function AgentFlowSection() {
  const [active, setActive] = useState(0)
  const a = AGENTS[active]
  return (
    <section className="flow-sec">
      <div className="flow-sec-inner">
        <div>
          <div className="sec-label" style={{color:'var(--accent-light)'}}>Multi-Agent Architecture</div>
          <h2 className="sec-title" style={{color:'white',fontSize:38,marginBottom:10}}>Seven specialized <em>agents,</em><br/>one intelligent pipeline</h2>
          <p className="sec-sub" style={{color:'var(--text-nav-soft)',marginTop:8}}>Each agent has a single responsibility. LangGraph's StateGraph wires them into a conditional DAG — routing decisions made at runtime based on content, similarity scores, and LLM confidence.</p>
        </div>
        <div className="flow-grid">
          <div className="agent-list">
            {AGENTS.map((ag, i) => (
              <div key={i} className={`agent-row ${active===i?'active':''}`} onClick={()=>setActive(i)}>
                <div className="agent-num">{ag.num}</div>
                <div className="agent-name">{ag.name}</div>
                <div className="agent-desc">{ag.short}</div>
                <div className="agent-arrow">›</div>
              </div>
            ))}
          </div>
          <div className="flow-detail" style={{borderColor:a.border}}>
            <div className="flow-detail-badge" style={{background:a.bg,color:a.color,border:`1px solid ${a.border}`}}>
              <span style={{fontFamily:'var(--font-mono)',fontSize:10}}>{a.num}</span>
              {a.name}
            </div>
            <div className="flow-detail-title">{a.name}</div>
            <div className="flow-detail-desc">{a.desc}</div>
            <div style={{height:1,background:'rgba(255,255,255,0.06)',marginBottom:20}}/>
            <div className="flow-detail-props">
              {a.props.map((p,i)=>(
                <div key={i} className="flow-prop">
                  <span className="flow-prop-key">{p.key}</span>
                  <span className="flow-prop-val">{p.val}</span>
                </div>
              ))}
            </div>
            <div style={{marginTop:24,padding:'14px 16px',background:'rgba(255,255,255,0.03)',borderRadius:10,border:'1px solid rgba(255,255,255,0.06)'}}>
              <div style={{fontSize:10,color:'rgba(255,255,255,0.25)',fontFamily:'var(--font-mono)',letterSpacing:'.1em',marginBottom:8}}>STATE TRANSITION</div>
              <div style={{fontFamily:'var(--font-mono)',fontSize:11,color:'rgba(255,255,255,0.5)',lineHeight:1.7}}>
                {active===0 && <span><span style={{color:a.color}}>file_content?</span> → ingestion : planner</span>}
                {active===1 && <span>load → split → clear() → <span style={{color:a.color}}>add_documents()</span></span>}
                {active===2 && <span><span style={{color:a.color}}>has_documents()</span> → retriever : fallback</span>}
                {active===3 && <span>search(k=6) → filter(≤1.8) → <span style={{color:a.color}}>llm : fallback</span></span>}
                {active===4 && <span>generate() → <span style={{color:a.color}}>negative?</span> → fallback : executor</span>}
                {active===5 && <span>wiki.search(q) → <span style={{color:a.color}}>source="wikipedia"</span></span>}
                {active===6 && <span>format() → history.append() → <span style={{color:a.color}}>END</span></span>}
              </div>
            </div>
          </div>
        </div>
      </div>
      <svg style={{position:'absolute',bottom:0,left:0,opacity:.04,pointerEvents:'none'}} width="400" height="300" viewBox="0 0 400 300" fill="none">
        {[...Array(24)].map((_,i)=>(<circle key={i} cx={(i%6)*50+25} cy={Math.floor(i/6)*50+25} r="2" fill="white"/>))}
      </svg>
    </section>
  )
}

// ─── TECH STACK SECTION ──────────────────────────────────────────────────────
const TECH = [
  { icon:<LangGraphIcon/>, name:'LangGraph', role:'Orchestrates the 7-agent StateGraph DAG with conditional routing edges', badge:'Orchestration', bc:'rgba(46,111,218,0.1)', bt:'#4d8af0', glow:'rgba(46,111,218,0.06)', ibg:'rgba(46,111,218,0.12)' },
  { icon:<GroqIcon/>, name:'Groq LLM', role:'llama-3.3-70b-versatile at temp=0.1 for factual, grounded RAG answers', badge:'Inference', bc:'rgba(232,169,48,0.1)', bt:'#e8a930', glow:'rgba(232,169,48,0.06)', ibg:'rgba(232,169,48,0.12)' },
  { icon:<ChromaIcon/>, name:'ChromaDB', role:'Local persistent vector store with cosine similarity search, k=6', badge:'Vector DB', bc:'rgba(139,92,246,0.1)', bt:'#8b5cf6', glow:'rgba(139,92,246,0.06)', ibg:'rgba(139,92,246,0.12)' },
  { icon:<HFIcon/>, name:'HuggingFace', role:'all-MiniLM-L6-v2 sentence-transformer with normalized embeddings on CPU', badge:'Embeddings', bc:'rgba(255,183,0,0.1)', bt:'#ffb700', glow:'rgba(255,183,0,0.06)', ibg:'rgba(255,183,0,0.12)' },
  { icon:<WikiIcon/>, name:'Wikipedia', role:'LangChain WikipediaQueryRun fallback — top-3 results, 2000 chars each', badge:'Fallback', bc:'rgba(26,158,106,0.1)', bt:'#1a9e6a', glow:'rgba(26,158,106,0.06)', ibg:'rgba(26,158,106,0.12)' },
  { icon:<PydanticIcon/>, name:'Pydantic v2', role:'Request/response validation with QueryRequest, QueryResponse, DocumentMetadata', badge:'Validation', bc:'rgba(214,63,77,0.1)', bt:'#d63f4d', glow:'rgba(214,63,77,0.06)', ibg:'rgba(214,63,77,0.12)' },
  { icon:<PyMuPDFIcon/>, name:'PyMuPDF', role:'High-fidelity PDF extraction with per-page metadata and source tracking', badge:'PDF Loader', bc:'rgba(232,169,48,0.1)', bt:'#e8a930', glow:'rgba(232,169,48,0.06)', ibg:'rgba(232,169,48,0.12)' },
  { icon:<PythonIcon/>, name:'Python 3.10+', role:'Async-ready codebase with TypedDict state, singleton services, ABC patterns', badge:'Runtime', bc:'rgba(46,111,218,0.1)', bt:'#4d8af0', glow:'rgba(46,111,218,0.06)', ibg:'rgba(46,111,218,0.12)' },
]

function TechSection({ onLaunch }) {
  return (
    <section className="tech-sec">
      <div className="sec-header">
        <div>
          <div className="sec-label">Technology Stack</div>
          <h2 className="sec-title">Every layer <em>purpose-built</em><br/>for precision RAG</h2>
        </div>
        <p className="sec-sub">Hand-picked components forming a cohesive pipeline — from chunking to generation.</p>
      </div>
      <div className="tech-grid">
        {TECH.map((t,i)=>(
          <div key={i} className="tech-card" style={{'--glow-color':t.glow}} onClick={i<2?onLaunch:undefined}>
            <div className="tech-icon" style={{background:t.ibg,border:`1px solid ${t.bc.replace('0.1','0.3')}`}}>{t.icon}</div>
            <div className="tech-name">{t.name}</div>
            <div className="tech-role">{t.role}</div>
            <div className="tech-badge" style={{background:t.bc,color:t.bt,border:`1px solid ${t.bc.replace('0.1','0.3')}`}}>{t.badge}</div>
          </div>
        ))}
      </div>
    </section>
  )
}

// ─── MAIN APP ─────────────────────────────────────────────────────────────────
export default function App() {
  const [page, setPage] = useState('home')
  const [tab, setTab] = useState('file')
  const [file, setFile] = useState(null)
  const [urlVal, setUrlVal] = useState('')
  const [textVal, setTextVal] = useState('')
  const [processing, setProcessing] = useState(false)
  const [ready, setReady] = useState(false)
  const [docSrc, setDocSrc] = useState(null)
  const [isDrag, setIsDrag] = useState(false)
  const [msgs, setMsgs] = useState([{type:'welcome'}])
  const [chatVal, setChatVal] = useState('')
  const [toasts, setToasts] = useState([])
  const fileRef = useRef(null)
  const msgsRef = useRef(null)
  const taRef = useRef(null)

  useEffect(()=>{if(ready && msgs[0]?.type==='welcome')setMsgs([{type:'bot',content:'Document indexed and ready. What would you like to know?',source:'rag'}])},[ready])
  useEffect(()=>{if(msgsRef.current)msgsRef.current.scrollTop=msgsRef.current.scrollHeight},[msgs])

  const toast=(msg,type='info')=>{const id=Date.now();setToasts(p=>[...p,{id,msg,type}]);setTimeout(()=>setToasts(p=>p.filter(t=>t.id!==id)),4000)}
  const validateFile=f=>{const ext='.'+f.name.split('.').pop().toLowerCase();if(!['.pdf','.docx','.txt'].includes(ext)){toast('Please upload PDF, DOCX, or TXT','error');return}setFile(f);setReady(false);setDocSrc(null);setMsgs([{type:'welcome'}])}
  const processDoc=async()=>{if(processing)return;if(tab==='file'&&!file){toast('Please select a file','error');return}if(tab==='url'){if(!urlVal){toast('Please enter a URL','error');return}try{new URL(urlVal)}catch{toast('Invalid URL','error');return}}if(tab==='text'&&textVal.length<50){toast('Please enter at least 50 characters','error');return}setProcessing(true);try{const fd=new FormData();fd.append('query','Initialize');fd.append('content_type',tab);if(tab==='file')fd.append('file',file);else if(tab==='url')fd.append('url',urlVal);else fd.append('text',textVal);const res=await fetch('/api/process',{method:'POST',body:fd});const data=await res.json();if(data.error)throw new Error(data.error);setReady(true);setDocSrc(tab);toast('Document processed successfully','success')}catch(e){toast(e.message||'Processing failed','error');setReady(false)}finally{setProcessing(false)}}
  const sendMsg=async()=>{if(!chatVal.trim()||!ready)return;const q=chatVal.trim();setMsgs(p=>[...p,{type:'user',content:q}]);setChatVal('');if(taRef.current)taRef.current.style.height='auto';const tid=Date.now();setMsgs(p=>[...p,{type:'typing',id:tid}]);try{const fd=new FormData();fd.append('query',q);fd.append('content_type',docSrc);if(docSrc==='file')fd.append('file',file);else if(docSrc==='url')fd.append('url',urlVal);else fd.append('text',textVal);const res=await fetch('/api/process',{method:'POST',body:fd});const data=await res.json();setMsgs(p=>p.filter(m=>m.id!==tid));setMsgs(p=>[...p,{type:'bot',content:data.error?`Error: ${data.error}`:data.answer,source:data.source}])}catch{setMsgs(p=>p.filter(m=>m.id!==tid));setMsgs(p=>[...p,{type:'bot',content:'Something went wrong. Please try again.'}])}}
  const clearChat=()=>setMsgs(ready?[{type:'bot',content:'Chat cleared. Ask me anything.',source:null}]:[{type:'welcome'}])
  const fmt=b=>b<1024?b+'B':b<1048576?(b/1024).toFixed(1)+'KB':(b/1048576).toFixed(1)+'MB'
  const md=t=>t.replace(/\n/g,'<br/>')
  const step1ok=file||(tab==='url'&&urlVal)||(tab==='text'&&textVal.length>=50)
  const goChat=()=>{setPage('chat');window.scrollTo(0,0)}

  return (
    <>
      <style>{CSS}</style>
      <div className="shell">

        {/* ── HEADER ── */}
        <header className="hdr">
          <HdrBg/>
          <div className="hdr-logo" onClick={()=>setPage('home')}>
            <div className="logo-mark"><LogoSVG/></div>
            <div><div className="logo-name">DocMind</div><div className="logo-sub">AI Document Intelligence</div></div>
          </div>
          <nav className="hdr-nav">
            <button className={`nav-btn ${page==='home'?'active':''}`} onClick={()=>setPage('home')}>Home</button>
            <button className={`nav-btn ${page==='chat'?'active':''}`} onClick={goChat}>Chat</button>
            <button className="nav-btn" onClick={()=>setPage('home')}>Agents</button>
            <button className="nav-btn" onClick={()=>setPage('home')}>Stack</button>
          </nav>
          <div className="hdr-cta">
            <div className="hdr-badge"><div className="live-dot"/>7 Agents Active</div>
            <button className="hdr-launch" onClick={goChat}>Launch App →</button>
          </div>
        </header>

        {/* ══════════════════ HOME PAGE ══════════════════ */}
        {page === 'home' && (
          <div className="page">

            {/* ── HERO ── */}
            <section className="home-hero">
              <HomeHeroBg/>
              <div className="hero-content">
                <div>
                  <div className="hero-eyebrow"><div className="hero-ey-line"/>LangGraph · Multi-Agent RAG Pipeline</div>
                  <h1 className="hero-heading">
                    Ask anything<br/>about <em>your documents.</em>
                  </h1>
                  <p className="hero-desc">
                    DocMind orchestrates 7 specialized AI agents — from ingestion to retrieval to generation — delivering precise, source-grounded answers in under 2 seconds. Built on LangGraph, Groq, and ChromaDB.
                  </p>
                  <div className="hero-btns">
                    <button className="btn-primary" onClick={goChat}>
                      <ArrowSVG/>Get Started Free
                    </button>
                    <button className="btn-ghost" onClick={()=>document.getElementById('agent-flow')?.scrollIntoView({behavior:'smooth'})}>
                      Explore Pipeline
                    </button>
                  </div>
                  <div className="hero-stats">
                    <div className="hero-stat"><div className="stat-val">7</div><div className="stat-label">AI Agents</div></div>
                    <div className="hero-stat"><div className="stat-val">&lt;2s</div><div className="stat-label">Response</div></div>
                    <div className="hero-stat"><div className="stat-val">4</div><div className="stat-label">File Types</div></div>
                    <div className="hero-stat" style={{borderRight:'none'}}><div className="stat-val">k=6</div><div className="stat-label">Chunks/Query</div></div>
                  </div>
                </div>
                <AnimatedTerminal onLaunch={goChat}/>
              </div>
            </section>

            {/* ── FEATURES ── */}
            <div style={{maxWidth:1200,margin:'0 auto',width:'100%'}}>
              <section className="features-sec">
                <div className="sec-header">
                  <div>
                    <div className="sec-label">Core Capabilities</div>
                    <h2 className="sec-title">Built for <em>precision</em><br/>at every layer</h2>
                  </div>
                  <p className="sec-sub">Every component is purpose-built — from ingestion to conditional routing to grounded generation.</p>
                </div>
                <div className="features-grid">
                  <Card3D onClick={goChat}>
                    <div className="feat-icon-wrap" style={{background:'rgba(46,111,218,0.08)',border:'1px solid rgba(46,111,218,0.15)'}}>
                      <LangGraphIcon/>
                    </div>
                    <div className="feat-title">Multi-Agent Pipeline</div>
                    <p className="feat-desc">A 7-node LangGraph StateGraph where each agent owns exactly one concern — routing, ingestion, planning, retrieval, generation, fallback, or execution. No monoliths.</p>
                    <div className="feat-tech">
                      <span className="feat-pill">LangGraph</span>
                      <span className="feat-pill">StateGraph</span>
                      <span className="feat-pill">TypedDict</span>
                    </div>
                    <div className="feat-tag" style={{background:'rgba(46,111,218,0.08)',color:'var(--accent)',border:'1px solid rgba(46,111,218,0.2)'}}>
                      ↳ Conditional DAG routing
                    </div>
                  </Card3D>
                  <Card3D onClick={goChat}>
                    <div className="feat-icon-wrap" style={{background:'rgba(139,92,246,0.08)',border:'1px solid rgba(139,92,246,0.15)'}}>
                      <ChromaIcon/>
                    </div>
                    <div className="feat-title">Semantic Retrieval</div>
                    <p className="feat-desc">ChromaDB cosine similarity search with two quality gates: per-chunk threshold at ≤1.8 and aggregate avg_score ≤1.6. Safety-net returns top-2 to prevent empty context.</p>
                    <div className="feat-tech">
                      <span className="feat-pill">ChromaDB</span>
                      <span className="feat-pill">all-MiniLM-L6-v2</span>
                      <span className="feat-pill">k=6</span>
                    </div>
                    <div className="feat-tag" style={{background:'rgba(139,92,246,0.08)',color:'#8b5cf6',border:'1px solid rgba(139,92,246,0.2)'}}>
                      ↳ Two-gate scoring logic
                    </div>
                  </Card3D>
                  <Card3D onClick={goChat}>
                    <div className="feat-icon-wrap" style={{background:'rgba(26,158,106,0.08)',border:'1px solid rgba(26,158,106,0.15)'}}>
                      <WikiIcon/>
                    </div>
                    <div className="feat-title">Graceful Fallback</div>
                    <p className="feat-desc">When documents don't contain the answer, DocMind detects 7 negative LLM patterns and auto-routes to Wikipedia. Users always receive a response — never a dead end.</p>
                    <div className="feat-tech">
                      <span className="feat-pill">Wikipedia API</span>
                      <span className="feat-pill">pattern detect</span>
                      <span className="feat-pill">source tag</span>
                    </div>
                    <div className="feat-tag" style={{background:'rgba(26,158,106,0.08)',color:'var(--success)',border:'1px solid rgba(26,158,106,0.2)'}}>
                      ↳ Zero dead-ends guaranteed
                    </div>
                  </Card3D>
                </div>
              </section>
            </div>

            {/* ── AGENT FLOW ── */}
            <div id="agent-flow"><AgentFlowSection/></div>

            {/* ── TECH STACK ── */}
            <TechSection onLaunch={goChat}/>

            {/* ── HOW IT WORKS ── */}
            <section className="how-sec">
              <div className="how-sec-inner">
                <div style={{textAlign:'center'}}>
                  <div className="sec-label" style={{display:'flex',justifyContent:'center',color:'var(--accent-light)'}}>How It Works</div>
                  <h2 className="sec-title" style={{textAlign:'center',color:'white'}}>Three steps to <em>instant answers</em></h2>
                  <p style={{color:'var(--text-nav-soft)',fontSize:14,textAlign:'center',marginTop:10,maxWidth:480,margin:'10px auto 0'}}>From raw document to grounded answer — the entire pipeline runs in under 2 seconds.</p>
                </div>
                <div className="steps-row">
                  {[
                    {
                      n:'1', cls:'s-active', title:'Upload Your Content',
                      desc:'Drop a PDF, paste a URL, or type text. ToolRouterAgent detects the content type and routes to IngestionAgent automatically.',
                      sub:['PDF · DOCX · TXT · Web URL','Max 16MB · UTF-8 encoded','Auto-detected file type']
                    },
                    {
                      n:'2', cls:'s-idle', title:'Index & Vectorize',
                      desc:'IngestionAgent chunks (400 chars, 80 overlap), embeds with all-MiniLM-L6-v2, clears stale data, and persists 47+ chunks to ChromaDB.',
                      sub:['chunk_size=400 · overlap=80','HuggingFace embeddings','ChromaDB persistence']
                    },
                    {
                      n:'3', cls:'s-idle', title:'Ask & Receive',
                      desc:'RetrieverAgent fetches k=6 chunks, LLMAnswerAgent calls Groq llama-3.3-70b, ExecutorAgent returns a cited answer with source tag.',
                      sub:['Groq llama-3.3-70b-versatile','Source: rag | wikipedia','Conversation history kept']
                    },
                  ].map((s,i)=>(
                    <div key={i} className="step-item">
                      <div className={`step-num ${s.cls}`}>{s.n}</div>
                      <div className="step-title">{s.title}</div>
                      <p className="step-desc">{s.desc}</p>
                      <div className="step-sub-list">
                        {s.sub.map((sub,j)=>(
                          <div key={j} className="step-sub-item">
                            <div className="step-sub-dot"/>
                            <span style={{fontFamily:'var(--font-mono)',fontSize:10,color:'rgba(255,255,255,0.3)'}}>{sub}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <svg style={{position:'absolute',bottom:0,right:0,opacity:.04,pointerEvents:'none'}} width="300" height="200" viewBox="0 0 300 200" fill="none">
                {[...Array(20)].map((_,i)=>(<circle key={i} cx={(i%5)*50+25} cy={Math.floor(i/5)*40+20} r="2" fill="white"/>))}
              </svg>
            </section>

            {/* ── ABOUT ── */}
            <section className="about-sec">
              <div className="sec-header">
                <div>
                  <div className="sec-label">About</div>
                  <h2 className="sec-title">The mind behind<br/><em>DocMind</em></h2>
                </div>
                <p className="sec-sub">A production-grade RAG system built with clean architecture, real engineering decisions, and zero shortcuts.</p>
              </div>
              <div className="about-grid">
                <div className="about-left">
                  <div className="about-creator-card">
                    <LpBgSVG/>
                    <div className="creator-header">
                      <div className="creator-avatar">NN</div>
                      <div>
                        <div className="creator-name">Naman Nanda</div>
                        <div className="creator-title">Builder · DocMind</div>
                      </div>
                    </div>
                    <p className="creator-bio">
                      Designed and built DocMind end-to-end — from the LangGraph StateGraph architecture to the ChromaDB vector pipeline to the multi-turn Groq chat interface. Every design decision in this codebase has a reason.
                    </p>
                    <div className="creator-stack">
                      {['LangGraph','Groq','ChromaDB','HuggingFace','Python 3.10','Pydantic v2','PyMuPDF'].map(s=>(
                        <span key={s} className="creator-pill">{s}</span>
                      ))}
                    </div>
                    <div className="creator-links">
                      <a href="https://github.com/namannanda" target="_blank" rel="noopener noreferrer" className="creator-link gh">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12"/></svg>
                        GitHub
                      </a>
                      <button className="creator-link gh" onClick={goChat} style={{border:'1px solid rgba(46,111,218,0.35)',color:'var(--accent-light)'}}>
                        Try DocMind →
                      </button>
                    </div>
                  </div>
                </div>
                <div className="about-right">
                  <div className="about-stat-grid">
                    {[
                      {val:'7',label:'Specialized agents in the pipeline'},
                      {val:'4',label:'Supported input types (PDF/DOCX/TXT/URL)'},
                      {val:'400',label:'Chars per chunk, 80 char overlap'},
                      {val:'1.8',label:'Cosine distance threshold for retrieval'},
                    ].map((s,i)=>(
                      <div key={i} className="about-stat-card">
                        <div className="ast-val">{s.val}</div>
                        <div className="ast-label">{s.label}</div>
                      </div>
                    ))}
                  </div>
                  <p className="about-desc">
                    DocMind is engineered around a <strong>clean separation of concerns</strong>. Each of the 7 agents in the LangGraph DAG has a single responsibility. All services — LLM, Embedding, VectorStore, Wikipedia — are <strong>singletons with lazy initialization</strong>, preventing redundant model loads.
                    <br/><br/>
                    The retrieval pipeline applies <strong>two independent quality gates</strong>: a per-chunk cosine distance filter (≤1.8) and an aggregate average score check (≤1.6). The system never returns a dead-end — negative LLM answers trigger automatic Wikipedia fallback, and every answer carries a <strong>source tag</strong> (rag or wikipedia) for transparency.
                  </p>
                </div>
              </div>
            </section>

            {/* ── CTA ── */}
            <section className="cta-sec">
              <HomeHeroBg/>
              <div className="cta-inner">
                <h2 className="cta-title">Ready to talk to<br/>your <em>documents?</em></h2>
                <p className="cta-sub">Upload a PDF, paste a URL, or type text — DocMind's multi-agent pipeline has your answer in under 2 seconds. No setup required.</p>
                <div className="cta-btns">
                  <button className="btn-primary" onClick={goChat}><ArrowSVG/>Launch DocMind</button>
                  <button className="btn-ghost" onClick={()=>document.getElementById('agent-flow')?.scrollIntoView({behavior:'smooth'})}>Explore the Pipeline</button>
                </div>
                <p className="cta-note">Built by Naman Nanda · LangGraph + Groq + ChromaDB + HuggingFace</p>
              </div>
            </section>

          </div>
        )}

        {/* ══════════════════ CHAT PAGE ══════════════════ */}
        {page === 'chat' && (
          <div className="page">
            <div className="hero">
              <HeroBgSVG/>
              <div className="hero-content-chat">
                <div className="hero-ey"><div className="hero-ey-line"/>LangGraph Multi-Agent Pipeline</div>
                <div className="hero-title">Ask anything about<br/><em>your documents.</em></div>
                <div className="hero-sub">Upload a PDF, DOCX, TXT, or paste a URL — DocMind's 7-agent pipeline retrieves, reasons, and responds with source-grounded answers.</div>
                <div className="chat-stats">
                  <div><div className="stat-num">7</div><div className="stat-lbl">Agents</div></div>
                  <div className="stat-div"/>
                  <div><div className="stat-num">k=6</div><div className="stat-lbl">Chunks/Query</div></div>
                  <div className="stat-div"/>
                  <div><div className="stat-num">Groq</div><div className="stat-lbl">llama-3.3-70b</div></div>
                </div>
              </div>
            </div>

            <main className="main-grid">
              <aside className="left-panel">
                <div className="lp-top">
                  <LpBgSVG/>
                  <div className="lp-ey">Document Source</div>
                  <div className="lp-title">Upload Content</div>
                  <div className="lp-sub">PDF · DOCX · TXT · URL supported</div>
                  <div className="step-bar">
                    <div style={{display:'flex',alignItems:'center',gap:6}}>
                      <div className={`s-num ${step1ok?'done':'active'}`}>{step1ok?'✓':'1'}</div>
                      <span className={`s-lbl ${!step1ok?'active':''}`}>Upload</span>
                    </div>
                    <div className="s-con"/>
                    <div style={{display:'flex',alignItems:'center',gap:6}}>
                      <div className={`s-num ${ready?'done':processing?'active':'idle'}`}>{ready?'✓':'2'}</div>
                      <span className={`s-lbl ${processing?'active':''}`}>Process</span>
                    </div>
                    <div className="s-con"/>
                    <div style={{display:'flex',alignItems:'center',gap:6}}>
                      <div className={`s-num ${ready?'active':'idle'}`}>3</div>
                      <span className={`s-lbl ${ready?'active':''}`}>Chat</span>
                    </div>
                  </div>
                </div>
                <div className="tab-bar">
                  {[{id:'file',icon:'fa-file-pdf',label:'File'},{id:'url',icon:'fa-globe',label:'URL'},{id:'text',icon:'fa-align-left',label:'Text'}].map(t=>(
                    <button key={t.id} onClick={()=>{setTab(t.id);setReady(false)}} className={`tab-btn ${tab===t.id?'active':''}`}>
                      <div className="tab-icon-box"><i className={`fas ${t.icon}`}/></div>{t.label}
                    </button>
                  ))}
                </div>
                <div className="upload-body">
                  {tab==='file'&&(!file?(
                    <div className={`drop-zone ${isDrag?'drag-over':''}`} onClick={()=>fileRef.current?.click()} onDragOver={e=>{e.preventDefault();setIsDrag(true)}} onDragLeave={()=>setIsDrag(false)} onDrop={e=>{e.preventDefault();setIsDrag(false);if(e.dataTransfer.files[0])validateFile(e.dataTransfer.files[0])}}>
                      <DropSVG/>
                      <div className="drop-title">Drop your file here</div>
                      <div className="drop-sub">or click to browse files</div>
                      <div className="type-pills">{['PDF','DOCX','TXT'].map(x=><span key={x} className="type-pill">{x}</span>)}</div>
                      <input type="file" ref={fileRef} onChange={e=>{if(e.target.files[0])validateFile(e.target.files[0])}} accept=".pdf,.docx,.txt" hidden/>
                    </div>
                  ):(
                    <div className="file-card">
                      <div className="file-badge"><FileIconSVG/></div>
                      <div className="file-info"><div className="file-name">{file.name}</div><div className="file-meta">{fmt(file.size)} · {file.name.split('.').pop().toUpperCase()}</div></div>
                      <button className="file-del" onClick={()=>{setFile(null);if(fileRef.current)fileRef.current.value='';setReady(false)}}><i className="fas fa-times"/></button>
                    </div>
                  ))}
                  {tab==='url'&&(<div className="field-wrap"><i className="fas fa-link field-icon"/><input type="url" value={urlVal} onChange={e=>setUrlVal(e.target.value)} placeholder="https://example.com/document" className="field-input"/></div>)}
                  {tab==='text'&&(<textarea value={textVal} onChange={e=>setTextVal(e.target.value)} placeholder="Paste your text content here (min 50 chars)…" className="field-ta"/>)}
                </div>
                <div className="proc-sec">
                  <div className="proc-sep"/>
                  {!processing&&!ready&&(<button className="proc-btn" onClick={processDoc}><div className="btn-ring"><ArrowSVG/></div>Process Document</button>)}
                  {processing&&(<div className="status-card"><div className="sc-ic proc"><div className="spinner"/></div><div><div className="sc-t">Processing Document</div><div className="sc-s">IngestionAgent indexing chunks…</div></div></div>)}
                  {ready&&(<div className="status-card"><div className="sc-ic ready"><CheckSVG/></div><div><div className="sc-t">Ready to Chat</div><div className="sc-s">Document indexed · ChromaDB ready</div></div></div>)}
                </div>
              </aside>

              <section className="right-panel">
                {!ready&&(
                  <div className="chat-overlay">
                    <div className="overlay-box">
                      <div className="ov-ic"><LockSVG/></div>
                      <div className="ov-title">Process a Document</div>
                      <div className="ov-sub">Upload and process your document on the left to unlock the DocMind chat interface.</div>
                    </div>
                  </div>
                )}
                <div className="chat-hdr">
                  <ChtHdrBgSVG/>
                  <div className="ch-info">
                    <div className="ch-ic"><ChatIconSVG/></div>
                    <div>
                      <div className="ch-title">DocMind Chat</div>
                      <div className="ch-sub">7-Agent RAG · Groq llama-3.3-70b · ChromaDB</div>
                    </div>
                  </div>
                  <div className="ch-acts"><button className="ch-btn" onClick={clearChat} title="Clear chat"><i className="fas fa-trash-alt"/></button></div>
                </div>
                <div className="msgs" ref={msgsRef}>
                  {msgs.map((m,i)=>{
                    if(m.type==='welcome')return(
                      <div key={i} className="welcome-wrap">
                        <WelcomeSVG/>
                        <div className="w-title">Welcome to DocMind</div>
                        <div className="w-sub">Upload a document using the panel on the left, then ask me anything about its content.</div>
                        <div className="w-chips">
                          {[{icon:'fa-project-diagram',label:'7-Agent Pipeline'},{icon:'fa-database',label:'ChromaDB RAG'},{icon:'fa-bolt',label:'Groq LLM'},{icon:'fa-globe',label:'Wikipedia Fallback'}].map(c=>(<div key={c.label} className="w-chip"><i className={`fas ${c.icon}`} style={{fontSize:9,color:'var(--accent)'}}/>{c.label}</div>))}
                        </div>
                      </div>
                    )
                    if(m.type==='typing')return(<div key={i} className="msg-row bot"><div className="msg-av bot"><BotSVG/></div><div className="msg-bub bot"><div className="typing-ind"><span/><span/><span/></div></div></div>)
                    const isUser=m.type==='user'
                    return(
                      <div key={i} className={`msg-row ${isUser?'user':'bot'}`}>
                        <div className={`msg-av ${isUser?'user':'bot'}`}>{isUser?<UserSVG/>:<BotSVG/>}</div>
                        <div className={`msg-bub ${isUser?'user':'bot'}`}>
                          {isUser?m.content:(<><div dangerouslySetInnerHTML={{__html:md(m.content)}}/>{m.source&&(<div className={`src-tag ${m.source==='rag'?'doc':'wiki'}`}><i className={`fas ${m.source==='rag'?'fa-file-alt':'fa-globe'}`} style={{fontSize:8}}/>{m.source==='rag'?'From Document · RAG':'From Wikipedia · Fallback'}</div>)}</>)}
                        </div>
                      </div>
                    )
                  })}
                </div>
                <div className="chat-input-bar">
                  <div className="chat-field">
                    <textarea ref={taRef} value={chatVal} onChange={e=>setChatVal(e.target.value)} onKeyDown={e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sendMsg()}}} onInput={e=>{e.target.style.height='auto';e.target.style.height=Math.min(e.target.scrollHeight,100)+'px'}} disabled={!ready} placeholder="Ask a question about your document…" rows={1} className="chat-ta"/>
                    <button onClick={sendMsg} disabled={!ready||!chatVal.trim()} className="send-btn"><SendSVG/></button>
                  </div>
                  <div className="input-hint">Enter to send · Shift+Enter for new line</div>
                </div>
              </section>
            </main>
          </div>
        )}

        {/* ── FOOTER ── */}
        <footer className="footer">
          <div className="ft-left">
            <span className="ft-logo">DocMind</span>
            <div className="ft-div"/>
            <span className="ft-copy">© 2026 All rights reserved</span>
          </div>
          <div className="ft-cred">
            <span style={{color:'var(--text-nav-soft)',fontSize:11,fontFamily:'var(--font-mono)'}}>LangGraph · Groq · ChromaDB · HuggingFace</span>
            <span style={{margin:'0 10px',color:'rgba(255,255,255,0.1)'}}>|</span>
            Developed by <strong>Naman Nanda</strong>
          </div>
        </footer>
      </div>

      <div className="toast-stack">
        {toasts.map(t=>(<div key={t.id} className={`toast ${t.type}`}><i className={`fas ${t.type==='success'?'fa-check-circle':t.type==='error'?'fa-exclamation-circle':'fa-info-circle'}`}/>{t.msg}</div>))}
      </div>
    </>
  )
}
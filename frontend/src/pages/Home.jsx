import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ShieldAlert, BookOpen, Film, ArrowRight, Activity, Zap, Cpu, Lock } from 'lucide-react'

export default function Home() {
  const tools = [
    {
      title: 'Spam Analyzer',
      description: 'Analyze emails, SMS, and chat messages for potential spam, phishing, and promotional links using NLP classification.',
      path: '/spam',
      icon: ShieldAlert,
      tag: 'Security',
    },
    {
      title: 'Poem Emotion & Moral',
      description: 'Discover the hidden depths of poetry. Identify fine-grained emotional tones, thematic morals, and structural devices.',
      path: '/poem',
      icon: BookOpen,
      tag: 'Literature',
    },
    {
      title: 'Movie Content Analyzer',
      description: 'Perform rich narrative analysis, classify genres with confidence scores, and generate plot advisories.',
      path: '/movie',
      icon: Film,
      tag: 'Cinema',
    },
  ]

  const benefits = [
    {
      title: 'Real-time Processing',
      description: 'Get immediate extraction outputs and confidence scores under 100ms for standard text structures.',
      icon: Zap,
    },
    {
      title: 'Monochromatic Design',
      description: 'A dark user interface carefully designed for long-session readability and premium presentation.',
      icon: Cpu,
    },
    {
      title: 'Local Privacy & Security',
      description: 'Your inputs are parsed and processed securely. No text details are persisted beyond the analysis pipeline.',
      icon: Lock,
    },
  ]

  const workflowSteps = [
    {
      step: '01',
      title: 'Paste Content',
      description: 'Input any raw text, email, poem stanza, or movie script excerpt into the analyzer interface.',
    },
    {
      step: '02',
      title: 'AI Analysis',
      description: 'Our backend processes the content using custom pre-trained classification models.',
    },
    {
      step: '03',
      title: 'Get Insights',
      description: 'Visualize sentiment metrics, genre distributions, and structured metadata in real-time.',
    },
  ]

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] } },
  }

  return (
    <div className="max-w-[1280px] mx-auto px-6 py-12 space-y-24 md:space-y-36">
      {/* 1. Hero Section */}
      <section className="relative pt-12 md:pt-20 text-center space-y-8 flex flex-col items-center">
        {/* Ambient background glow */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-white/[0.02] rounded-full blur-[120px] pointer-events-none" />

        {/* ELYRA Brand Identity vertical lockup from the top image */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className="flex flex-col items-center text-center space-y-6 mb-2"
        >
          {/* Symbol Mark SVG */}
          <svg
            viewBox="0 0 100 100"
            className="h-28 w-28 md:h-36 md:w-36 drop-shadow-[0_0_35px_rgba(192,132,252,0.12)]"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <defs>
              <linearGradient id="silverSpineGradientLarge" x1="20" y1="15" x2="64" y2="85" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#E4E4E7" />
                <stop offset="20%" stopColor="#FAFAFA" />
                <stop offset="50%" stopColor="#FFFFFF" />
                <stop offset="80%" stopColor="#E4E4E7" />
                <stop offset="100%" stopColor="#A1A1AA" />
              </linearGradient>
              <linearGradient id="purpleWaveGradientLarge" x1="10" y1="50" x2="68" y2="44" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#D8B4FE" />
                <stop offset="50%" stopColor="#C084FC" />
                <stop offset="100%" stopColor="#818CF8" />
              </linearGradient>
              <radialGradient id="spotlightGlowLarge" cx="22" cy="50" r="16" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#FFFFFF" stopOpacity="1" />
                <stop offset="25%" stopColor="#E9D5FF" stopOpacity="0.8" />
                <stop offset="60%" stopColor="#C084FC" stopOpacity="0.25" />
                <stop offset="100%" stopColor="#C084FC" stopOpacity="0" />
              </radialGradient>
              <linearGradient id="starGradientLarge" x1="102" y1="12" x2="106" y2="16" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#E2D5FA" />
                <stop offset="100%" stopColor="#C084FC" />
              </linearGradient>
            </defs>

            <circle cx="22" cy="50" r="18" fill="url(#spotlightGlowLarge)" opacity="0.65" />
            <path
              d="M 64,15 C 32,15 16,28 16,50 C 16,72 32,85 64,85 V 83 C 34,83 28,70 28,50 C 28,30 34,17 64,17 Z"
              fill="url(#silverSpineGradientLarge)"
            />
            <path
              d="M 10,60 C 20,52 20,44 26,44 C 34,44 44,53 52,53 C 60,53 64,48 68,44 C 64,47 52,56 44,56 C 36,56 26,48 10,60 Z"
              fill="url(#purpleWaveGradientLarge)"
            />
            <circle cx="22" cy="50" r="8" fill="url(#spotlightGlowLarge)" opacity="0.95" />
            <path
              d="M 68,27 Q 68,36 60,36 Q 68,36 68,45 Q 68,36 76,36 Q 68,36 68,27 Z"
              fill="url(#purpleWaveGradientLarge)"
            />
          </svg>

          {/* E L Y R A Logotype SVG */}
          <div className="flex flex-col items-center space-y-3">
            <svg
              viewBox="0 0 114 20"
              className="h-7 md:h-9 w-auto text-white"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              {/* Letter E */}
              <path
                d="M 12,0.5 H 0.5 V 19.5 H 12 M 0.5,10 H 9.5"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              {/* Letter L */}
              <path
                d="M 24,0.5 V 19.5 H 35.5"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              {/* Letter Y */}
              <path
                d="M 46.5,0.5 L 54,10 V 19.5 M 61.5,0.5 L 54,10"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              {/* Letter R */}
              <path
                d="M 72.5,19.5 V 0.5 H 81.5 C 85,0.5 86.5,2.5 86.5,5.5 C 86.5,8.5 85,10 81.5,10 H 72.5 M 79.5,10 L 86.5,19.5"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              {/* Letter A */}
              <path
                d="M 96.5,19.5 L 104,0.5 L 111.5,19.5"
                stroke="currentColor"
                strokeWidth="1.8"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              {/* Star inside Letter A */}
              <path
                d="M 104,11.5 Q 104,14 101.5,14 Q 104,14 104,16.5 Q 104,14 106.5,14 Q 104,14 104,11.5 Z"
                fill="url(#starGradientLarge)"
              />
            </svg>
            <span className="text-[7.5px] md:text-[8px] tracking-[0.35em] text-text-muted font-extrabold uppercase leading-none">
              Understand beyond words.
            </span>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1, ease: [0.16, 1, 0.3, 1] }}
          className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-bg-surface border border-border-custom text-xs font-medium text-text-secondary"
        >
          <Activity className="h-3.5 w-3.5 text-status-success animate-pulse" />
          <span>All systems fully operational</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
          className="text-4xl md:text-[64px] leading-tight font-extrabold tracking-tight text-white max-w-4xl mx-auto"
        >
          Unveil the structure and sentiment in your text.
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2, ease: [0.16, 1, 0.3, 1] }}
          className="text-base md:text-lg text-text-secondary max-w-2xl mx-auto leading-relaxed"
        >
          ELYRA is a minimal, premium Content Intelligence platform offering modular pipelines to decode, categorize, and gain deep metadata insights.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
          className="flex flex-col sm:flex-row justify-center items-center gap-4 pt-4"
        >
          <a
            href="#pipelines"
            className="w-full sm:w-auto px-6 py-3 bg-white text-bg-primary rounded-full font-semibold text-sm hover:bg-white/90 active:scale-95 transition-custom text-center"
          >
            Explore Pipelines
          </a>
          <Link
            to="/spam"
            className="w-full sm:w-auto flex items-center justify-center gap-2 px-6 py-3 bg-transparent border border-border-custom hover:border-white/20 text-text-primary rounded-full font-semibold text-sm transition-custom active:scale-95 text-center"
          >
            Start Analyzing <ArrowRight className="h-4 w-4" />
          </Link>
        </motion.div>
      </section>

      {/* 2. Features Grid */}
      <section id="pipelines" className="space-y-12">
        <div className="text-center md:text-left space-y-2">
          <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-white">Analysis Pipelines</h2>
          <p className="text-text-secondary text-sm max-w-lg leading-relaxed">
            Select one of our specialized models below to extract clean visual metadata from raw text datasets.
          </p>
        </div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, margin: '-100px' }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          {tools.map((tool, idx) => {
            const Icon = tool.icon
            return (
              <motion.div
                key={idx}
                variants={itemVariants}
                className="bg-bg-surface hover:bg-bg-elevated border border-border-custom hover:border-border-custom-hover rounded-2xl p-8 flex flex-col justify-between h-full group hover:-translate-y-1 transition-custom shadow-xl relative overflow-hidden"
              >
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <div className="p-3 bg-bg-primary border border-border-custom rounded-xl group-hover:border-white/20 transition-custom">
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <span className="text-[10px] tracking-widest uppercase font-bold text-text-muted px-2.5 py-1 bg-bg-primary border border-border-custom rounded-full">
                      {tool.tag}
                    </span>
                  </div>
                  <div className="space-y-2">
                    <h3 className="text-lg font-bold text-white group-hover:text-white transition-colors">
                      {tool.title}
                    </h3>
                    <p className="text-text-secondary leading-relaxed text-sm">
                      {tool.description}
                    </p>
                  </div>
                </div>
                <div className="pt-8">
                  <Link
                    to={tool.path}
                    className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-bg-primary hover:bg-white hover:text-bg-primary border border-border-custom hover:border-white text-text-primary rounded-xl text-xs font-semibold tracking-tight transition-custom"
                  >
                    Open Analyzer <ArrowRight className="h-3.5 w-3.5" />
                  </Link>
                </div>
              </motion.div>
            )
          })}
        </motion.div>
      </section>

      {/* 3. Why ELYRA Section */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-12 items-center">
        <div className="space-y-4 lg:col-span-1">
          <span className="text-[10px] uppercase font-bold tracking-widest text-text-muted">Why ELYRA</span>
          <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-white leading-tight">
            Built for visual clarity and analytical precision.
          </h2>
          <p className="text-text-secondary text-sm leading-relaxed">
            We focus on clean, high-performance typography and spaces to make your content analysis tasks distraction-free.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 lg:col-span-2">
          {benefits.map((benefit, idx) => {
            const Icon = benefit.icon
            return (
              <div
                key={idx}
                className="bg-bg-surface border border-border-custom rounded-2xl p-6 space-y-4 flex flex-col justify-between"
              >
                <div className="p-2.5 bg-bg-primary border border-border-custom rounded-lg w-fit">
                  <Icon className="h-5 w-5 text-white" />
                </div>
                <div className="space-y-1">
                  <h3 className="text-sm font-semibold text-white">{benefit.title}</h3>
                  <p className="text-xs text-text-secondary leading-relaxed">{benefit.description}</p>
                </div>
              </div>
            )
          })}
        </div>
      </section>

      {/* 4. Workflow Section */}
      <section className="space-y-16">
        <div className="text-center space-y-2">
          <span className="text-[10px] uppercase font-bold tracking-widest text-text-muted">How it works</span>
          <h2 className="text-2xl md:text-3xl font-bold tracking-tight text-white">The Analysis Pipeline</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          {/* Subtle connecting line on desktop */}
          <div className="hidden md:block absolute top-[52px] left-[10%] right-[10%] h-[1px] bg-border-custom z-0" />

          {workflowSteps.map((step, idx) => (
            <div
              key={idx}
              className="bg-bg-surface border border-border-custom rounded-2xl p-8 space-y-6 relative z-10 flex flex-col justify-between"
            >
              <div className="flex justify-between items-center">
                <span className="text-xs font-mono font-bold px-3 py-1 bg-bg-primary border border-border-custom rounded-full text-text-secondary">
                  {step.step}
                </span>
                <span className="h-2 w-2 rounded-full bg-border-custom" />
              </div>
              <div className="space-y-2">
                <h3 className="text-base font-bold text-white">{step.title}</h3>
                <p className="text-xs text-text-secondary leading-relaxed">{step.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Connected Platform Status */}
      <section className="bg-bg-surface border border-border-custom rounded-2xl p-8 flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-1 text-center md:text-left">
          <h3 className="text-sm font-bold text-white">Service Health Indicator</h3>
          <p className="text-text-secondary text-xs">All intelligence pipelines are operating normally.</p>
        </div>
        <div className="flex items-center gap-3 bg-bg-primary border border-border-custom px-4 py-2.5 rounded-full">
          <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-status-success opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-status-success" />
          </span>
          <span className="text-text-secondary text-xs font-medium">FastAPI Server Connected</span>
        </div>
      </section>
    </div>
  )
}


import { useState } from 'react'
import { motion } from 'framer-motion'
import { ShieldAlert, ArrowRight, RefreshCw, CheckCircle2, AlertTriangle } from 'lucide-react'
import api from '../services/api'

export default function SpamAnalyzer() {
  const [text, setText] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState(null)

  const handleAnalyze = async (e) => {
    e.preventDefault()
    if (!text.trim()) return

    setAnalyzing(true)
    
    try {
      const response = await api.post('/api/spam/analyze', { text })
      const data = response.data
      setResult({
        isSpam: data.is_spam,
        confidence: data.confidence,
        message: data.message,
        spamScore: data.spam_score,
        hamScore: data.ham_score,
        keywordsDetected: data.keywords_detected
      })
    } catch (err) {
      console.warn("Backend API unreachable. Falling back to frontend mock simulation.", err)
      // Simulate fallback prediction logic
      setTimeout(() => {
        const textLower = text.toLowerCase()
        const isSpam = textLower.includes('free') || textLower.includes('winner') || textLower.includes('money') || textLower.includes('claim') || textLower.includes('prize')
        const confidence = isSpam ? 0.92 : 0.88
        setResult({
          isSpam,
          confidence,
          message: isSpam ? 'Text identified as potential spam (Offline Mode).' : 'Text appears to be safe (Offline Mode).',
          spamScore: isSpam ? confidence : 1 - confidence,
          hamScore: isSpam ? 1 - confidence : confidence,
          keywordsDetected: ['free', 'money', 'claim', 'urgent', 'winner', 'prize', 'offer'].filter(w => textLower.includes(w))
        })
        setAnalyzing(false)
      }, 800)
      return
    }
    setAnalyzing(false)
  }

  const handleReset = () => {
    setText('')
    setResult(null)
  }

  return (
    <div className="max-w-[1280px] mx-auto px-6 py-12 md:py-20 space-y-12 animate-fade-in">
      {/* Header */}
      <div className="space-y-3 max-w-2xl">
        <div className="flex items-center gap-2 text-text-secondary">
          <ShieldAlert className="h-5 w-5 text-white" />
          <span className="text-xs uppercase tracking-widest font-bold">Security Pipeline</span>
        </div>
        <h1 className="text-3xl md:text-[48px] font-extrabold tracking-tight text-white leading-tight">
          Spam Analyzer
        </h1>
        <p className="text-text-secondary text-sm md:text-base leading-relaxed">
          Evaluate emails, SMS, and messaging datasets for potential spam, phishing, and promotional links.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">
        {/* Input Card */}
        <div className="lg:col-span-3 bg-bg-surface border border-border-custom rounded-2xl p-6 md:p-8 space-y-6">
          <form onSubmit={handleAnalyze} className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-xs uppercase tracking-wider font-bold text-text-secondary">
                Message Content
              </label>
              <span className="text-xs text-text-muted">{text.length} characters</span>
            </div>
            
            <textarea
              className="w-full h-64 bg-bg-primary border border-border-custom rounded-xl p-4 text-text-primary placeholder:text-text-muted focus:border-white focus:outline-none transition-custom text-sm resize-none leading-relaxed"
              placeholder="Paste email or text snippet here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              disabled={analyzing}
            />

            <div className="flex items-center justify-end gap-3 pt-2">
              {text.trim() && (
                <button
                  type="button"
                  onClick={handleReset}
                  className="px-4 py-2.5 rounded-full border border-border-custom hover:border-white/20 text-xs font-semibold text-text-secondary hover:text-white transition-custom cursor-pointer"
                >
                  Clear
                </button>
              )}
              <button
                type="submit"
                disabled={analyzing || !text.trim()}
                className="flex items-center gap-2 py-2.5 px-6 rounded-full bg-white hover:bg-white/90 text-bg-primary font-semibold text-xs tracking-tight transition-custom disabled:opacity-50 disabled:pointer-events-none cursor-pointer"
              >
                {analyzing ? (
                  <>
                    <RefreshCw className="h-3 w-3 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <span>Run Pipeline</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-2 bg-bg-surface border border-border-custom rounded-2xl p-6 md:p-8 flex flex-col justify-between min-h-[350px]">
          <div>
            <h3 className="text-xs uppercase tracking-wider font-bold text-text-secondary mb-6 pb-3 border-b border-border-custom">
              Analysis Summary
            </h3>

            {result ? (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
                className="space-y-6"
              >
                {/* Result Flag */}
                <div
                  className={`flex items-center gap-3 p-4 rounded-xl border text-xs font-bold tracking-wide uppercase ${
                    result.isSpam
                      ? 'bg-status-error/10 border-status-error/20 text-status-error'
                      : 'bg-status-success/10 border-status-success/20 text-status-success'
                  }`}
                >
                  {result.isSpam ? (
                    <>
                      <AlertTriangle className="h-4.5 w-4.5" />
                      <span>Flagged as Spam</span>
                    </>
                  ) : (
                    <>
                      <CheckCircle2 className="h-4.5 w-4.5" />
                      <span>Clean (Ham Content)</span>
                    </>
                  )}
                </div>

                <div className="space-y-4">
                  {/* Single Premium Spam Risk Indicator */}
                  <div className="space-y-1.5">
                    <div className="flex justify-between text-xs font-medium">
                      <span className="text-text-secondary">Spam Probability</span>
                      <span className={result.isSpam ? 'text-status-error font-semibold' : 'text-status-success font-semibold'}>
                        {(result.spamScore * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="w-full bg-bg-primary h-2 rounded-full overflow-hidden border border-border-custom">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${result.spamScore * 100}%` }}
                        transition={{ duration: 0.8, ease: 'easeOut' }}
                        className={`h-full rounded-full transition-colors ${result.isSpam ? 'bg-status-error' : 'bg-status-success'}`}
                      />
                    </div>
                  </div>
                </div>

                {/* Detected Keywords */}
                {result.keywordsDetected.length > 0 && (
                  <div className="space-y-2 pt-2">
                    <span className="block text-[10px] uppercase font-bold text-text-muted">
                      Trigger Keywords Detected
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {result.keywordsDetected.map((w, i) => (
                        <span
                          key={i}
                          className="text-[11px] bg-bg-primary border border-border-custom text-text-secondary px-2.5 py-1 rounded-md"
                        >
                          {w}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="text-[11px] text-text-muted pt-2">
                  {result.message}
                </div>
              </motion.div>
            ) : (
              <div className="flex flex-col items-center justify-center py-16 text-center space-y-3">
                <ShieldAlert className="h-8 w-8 text-text-muted" />
                <p className="text-xs text-text-secondary">
                  Provide text and run analysis pipeline to yield predictions.
                </p>
              </div>
            )}
          </div>

          <div className="text-[10px] text-text-muted border-t border-border-custom pt-4 mt-8 flex justify-between items-center">
            <span className="flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-status-success animate-pulse" />
              ELYRA Content Guard active
            </span>
            <span>Secure Analysis</span>
          </div>
        </div>
      </div>
    </div>
  )
}


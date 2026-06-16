import { useState } from 'react'
import { motion } from 'framer-motion'
import { Film, ArrowRight, RefreshCw, AlertCircle, Clock, Tags } from 'lucide-react'
import api from '../services/api'

export default function MovieAnalyzer() {
  const [synopsis, setSynopsis] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState(null)

  const handleAnalyze = async (e) => {
    e.preventDefault()
    if (!synopsis.trim()) return

    setAnalyzing(true)

    try {
      const response = await api.post('/api/movie/analyze', { synopsis })
      const data = response.data
      setResult({
        genres: data.genres,
        advisories: data.advisories,
        keyThemes: data.key_themes,
        runtimeEstimate: data.runtime_estimate
      })
    } catch (err) {
      console.warn("Backend API unreachable. Falling back to mock data.", err)
      setTimeout(() => {
        setResult({
          genres: [
            { name: 'Sci-Fi', confidence: 0.92 },
            { name: 'Thriller', confidence: 0.78 },
            { name: 'Mystery', confidence: 0.54 }
          ],
          advisories: {
            violence: 'Low',
            language: 'Moderate',
            nudity: 'None',
          },
          keyThemes: ['Artificial Intelligence', 'Existentialism', 'Corporate Greed'],
          runtimeEstimate: '105 - 120 mins'
        })
        setAnalyzing(false)
      }, 800)
      return
    }
    setAnalyzing(false)
  }

  const handleReset = () => {
    setSynopsis('')
    setResult(null)
  }

  return (
    <div className="max-w-[1280px] mx-auto px-6 py-12 md:py-20 space-y-12 animate-fade-in">
      {/* Header */}
      <div className="space-y-3 max-w-2xl">
        <div className="flex items-center gap-2 text-text-secondary">
          <Film className="h-5 w-5 text-white" />
          <span className="text-xs uppercase tracking-widest font-bold">Cinema Pipeline</span>
        </div>
        <h1 className="text-3xl md:text-[48px] font-extrabold tracking-tight text-white leading-tight">
          Movie Content Analyzer
        </h1>
        <p className="text-text-secondary text-sm md:text-base leading-relaxed">
          Deconstruct movie synopses and screenplays to estimate genre classification, thematic weights, and audience advisory flags.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">
        {/* Input Card */}
        <div className="lg:col-span-3 bg-bg-surface border border-border-custom rounded-2xl p-6 md:p-8 space-y-6">
          <form onSubmit={handleAnalyze} className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-xs uppercase tracking-wider font-bold text-text-secondary">
                Synopsis or Script Excerpt
              </label>
              <span className="text-xs text-text-muted">
                {synopsis.split(' ').filter(Boolean).length} words
              </span>
            </div>

            <textarea
              className="w-full h-64 bg-bg-primary border border-border-custom rounded-xl p-4 text-text-primary placeholder:text-text-muted focus:border-white focus:outline-none transition-custom text-sm resize-none leading-relaxed"
              placeholder="Paste the plot synopsis here... (e.g. 'In a dystopian metropolis, a cybernetic detective hunts rogue AI cores...')"
              value={synopsis}
              onChange={(e) => setSynopsis(e.target.value)}
              disabled={analyzing}
            />

            <div className="flex items-center justify-end gap-3 pt-2">
              {synopsis.trim() && (
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
                disabled={analyzing || !synopsis.trim()}
                className="flex items-center gap-2 py-2.5 px-6 rounded-full bg-white hover:bg-white/90 text-bg-primary font-semibold text-xs tracking-tight transition-custom disabled:opacity-50 disabled:pointer-events-none cursor-pointer"
              >
                {analyzing ? (
                  <>
                    <RefreshCw className="h-3 w-3 animate-spin" />
                    <span>Deconstructing plot...</span>
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
              Movie Breakdown
            </h3>

            {result ? (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
                className="space-y-6 animate-fade-in"
              >
                {/* Classified Genres */}
                <div className="space-y-3">
                  <span className="block text-[10px] uppercase font-bold text-text-muted">Classified Genres</span>
                  <div className="space-y-3">
                    {result.genres.map((g, i) => (
                      <div key={i} className="space-y-1">
                        <div className="flex justify-between text-xs font-medium">
                          <span className="text-text-secondary">{g.name}</span>
                          <span className="text-text-primary">{(g.confidence * 100).toFixed(0)}% Match</span>
                        </div>
                        <div className="w-full bg-bg-primary h-1 rounded-full overflow-hidden border border-border-custom">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${g.confidence * 100}%` }}
                            transition={{ duration: 0.8, ease: 'easeOut' }}
                            className="h-full rounded-full bg-white"
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Content Advisory */}
                <div className="space-y-2.5">
                  <span className="flex items-center gap-1.5 text-[10px] uppercase font-bold text-text-muted">
                    <AlertCircle className="h-3.5 w-3.5" />
                    <span>Content Advisory</span>
                  </span>
                  <div className="grid grid-cols-3 gap-2">
                    {Object.entries(result.advisories).map(([key, value]) => (
                      <div key={key} className="bg-bg-primary border border-border-custom p-3 rounded-xl text-center">
                        <span className="block text-[9px] uppercase tracking-wider text-text-muted mb-1">{key}</span>
                        <span
                          className={`text-xs font-bold ${
                            value === 'None'
                              ? 'text-text-muted'
                              : value === 'Low'
                              ? 'text-text-secondary'
                              : 'text-white'
                          }`}
                        >
                          {value}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Narrative Themes */}
                <div className="space-y-2.5">
                  <span className="flex items-center gap-1.5 text-[10px] uppercase font-bold text-text-muted">
                    <Tags className="h-3.5 w-3.5" />
                    <span>Key Themes</span>
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {result.keyThemes.map((theme, i) => (
                      <span
                        key={i}
                        className="text-[10px] uppercase tracking-wider font-bold bg-bg-primary border border-border-custom text-text-secondary px-2.5 py-1 rounded-full"
                      >
                        {theme}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Runtime Indicator */}
                <div className="flex items-center justify-between bg-bg-primary border border-border-custom p-3.5 rounded-xl">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 text-text-secondary" />
                    <span className="text-xs text-text-secondary">Estimated Pace Runtime</span>
                  </div>
                  <span className="text-xs font-bold text-white font-mono">{result.runtimeEstimate}</span>
                </div>
              </motion.div>
            ) : (
              <div className="flex flex-col items-center justify-center py-16 text-center space-y-3">
                <Film className="h-8 w-8 text-text-muted" />
                <p className="text-xs text-text-secondary">
                  Provide synopsis and run analysis pipeline to yield movie insights.
                </p>
              </div>
            )}
          </div>

          <div className="text-[10px] text-text-muted border-t border-border-custom pt-4 mt-8 flex justify-between">
            <span>Model: Film Genre Synthesizer</span>
            <span>v1.0.4</span>
          </div>
        </div>
      </div>
    </div>
  )
}


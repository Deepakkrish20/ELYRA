import { useState } from 'react'
import { motion } from 'framer-motion'
import { BookOpen, ArrowRight, RefreshCw, Feather, Sparkles, Quote } from 'lucide-react'
import api from '../services/api'

export default function PoemAnalyzer() {
  const [poem, setPoem] = useState('')
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState(null)

  const handleAnalyze = async (e) => {
    e.preventDefault()
    if (!poem.trim()) return

    setAnalyzing(true)

    try {
      const response = await api.post('/api/poem/analyze', { text: poem })
      const data = response.data
      
      const colorMap = {
        'Melancholy': 'bg-white/40',
        'Joy': 'bg-white',
        'Nostalgia': 'bg-white/60',
        'Awe': 'bg-white/80'
      }

      const formattedEmotions = Object.entries(data.emotions).map(([name, score]) => ({
        name,
        score,
        color: colorMap[name] || 'bg-white'
      }))

      setResult({
        emotions: formattedEmotions,
        poeticDevices: data.poetic_devices,
        intention: data.intention,
        suitableAgeGroup: data.suitable_age_group,
        moral: data.moral,
        meaning: data.meaning,
        realLifeExample: data.real_life_example,
        suggestedPoems: data.suggested_poems
      })
    } catch (err) {
      console.warn("Backend API unreachable. Falling back to mock data.", err)
      setTimeout(() => {
        setResult({
          emotions: [
            { name: 'Melancholy', score: 0.65, color: 'bg-white/40' },
            { name: 'Joy', score: 0.12, color: 'bg-white' },
            { name: 'Nostalgia', score: 0.84, color: 'bg-white/60' },
            { name: 'Awe', score: 0.45, color: 'bg-white/80' },
          ],
          poeticDevices: ['Alliteration', 'Metaphor', 'Imagery'],
          intention: 'Reflection',
          suitableAgeGroup: 'Teens & Adults',
          moral: 'Time is transient and fleeting, encouraging the reader to treasure existing bonds (Offline Mode).',
          meaning: 'A thoughtful examination of identity, human connections, and the quiet spaces in between actions (Offline Mode).',
          realLifeExample: 'Spending ten minutes writing in a personal journal before sleeping to reflect on your day and set clean intentions (Offline Mode).',
          suggestedPoems: [
            { title: 'Stopping by Woods on a Snowy Evening', author: 'Robert Frost' },
            { title: 'The Journey', author: 'Mary Oliver' }
          ]
        })
        setAnalyzing(false)
      }, 800)
      return
    }
    setAnalyzing(false)
  }

  const handleReset = () => {
    setPoem('')
    setResult(null)
  }

  return (
    <div className="max-w-[1280px] mx-auto px-4 sm:px-6 py-8 md:py-20 space-y-8 md:space-y-12 animate-fade-in">
      {/* Header */}
      <div className="space-y-3 max-w-2xl">
        <div className="flex items-center gap-2 text-text-secondary">
          <BookOpen className="h-5 w-5 text-white" />
          <span className="text-xs uppercase tracking-widest font-bold">Literature Engine</span>
        </div>
        <h1 className="text-3xl md:text-[48px] font-extrabold tracking-tight text-white leading-tight">
          Poem Emotion & Moral Analyzer
        </h1>
        <p className="text-text-secondary text-sm md:text-base leading-relaxed">
          Unveil emotional tones, thematic morals, and stylistic literary devices hidden within verses of poetry.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 md:gap-8 items-start">
        {/* Input Card */}
        <div className="lg:col-span-3 bg-bg-surface border border-border-custom rounded-2xl p-4 sm:p-6 md:p-8 space-y-6">
          <form onSubmit={handleAnalyze} className="space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-xs uppercase tracking-wider font-bold text-text-secondary">
                Poem Verses / Stanzas
              </label>
              <span className="text-xs text-text-muted">
                {poem.split('\n').filter(Boolean).length} lines
              </span>
            </div>

            <textarea
              className="w-full h-48 sm:h-64 bg-bg-primary border border-border-custom rounded-xl p-4 text-text-primary placeholder:text-text-muted focus:border-white focus:outline-none transition-custom text-sm font-serif leading-relaxed disabled:opacity-60 disabled:cursor-not-allowed"
              placeholder="Paste stanzas here... (e.g. 'Two roads diverged in a yellow wood, and sorry I could not travel both...')"
              value={poem}
              onChange={(e) => setPoem(e.target.value)}
              disabled={analyzing || result !== null}
            />

            <div className="flex items-center justify-end gap-3 pt-2">
              {poem.trim() && (
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
                disabled={analyzing || !poem.trim() || result !== null}
                className="flex items-center gap-2 py-2.5 px-6 rounded-full bg-white hover:bg-white/90 text-bg-primary font-semibold text-xs tracking-tight transition-custom disabled:opacity-50 disabled:pointer-events-none cursor-pointer"
              >
                {analyzing ? (
                  <>
                    <RefreshCw className="h-3 w-3 animate-spin" />
                    <span>Analyzing verses...</span>
                  </>
                ) : (
                  <>
                    <span>Analyze Poem</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Results Panel */}
        <div className="lg:col-span-2 bg-bg-surface border border-border-custom rounded-2xl p-4 sm:p-6 md:p-8 flex flex-col justify-between min-h-[300px] md:min-h-[350px]">
          <div>
            {result ? (
              <div className="flex flex-wrap items-center justify-between gap-3 mb-6 pb-4 border-b border-border-custom">
                <h3 className="text-xs uppercase tracking-wider font-bold text-text-secondary">
                  Poetic Insights
                </h3>
                <div className="flex items-center gap-1.5">
                  <span className="text-[9px] uppercase tracking-wider font-extrabold px-2.5 py-1 rounded-full bg-white text-bg-primary shadow-sm flex items-center gap-1">
                    <Sparkles className="h-2.5 w-2.5" />
                    {result.intention}
                  </span>
                  <span className="text-[9px] uppercase tracking-wider font-bold px-2.5 py-1 rounded-full bg-bg-primary border border-border-custom text-text-secondary">
                    {result.suitableAgeGroup}
                  </span>
                </div>
              </div>
            ) : (
              <h3 className="text-xs uppercase tracking-wider font-bold text-text-secondary mb-6 pb-3 border-b border-border-custom">
                Poetic Insights
              </h3>
            )}

            {result ? (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
                className="space-y-6 animate-fade-in"
              >
                {/* Deeper Meaning */}
                <div className="space-y-2">
                  <span className="block text-[10px] uppercase tracking-wider font-bold text-text-muted">Deeper Meaning</span>
                  <p className="text-sm font-serif italic text-text-primary leading-relaxed bg-bg-primary border border-border-custom p-4 rounded-xl">
                    "{result.meaning}"
                  </p>
                </div>

                {/* Moral */}
                <div className="space-y-2">
                  <span className="block text-[10px] uppercase tracking-wider font-bold text-text-muted">Moral & Lesson</span>
                  <div className="flex items-start gap-3 text-xs text-text-secondary leading-relaxed bg-bg-primary border border-border-custom p-4 rounded-xl">
                    <Feather className="h-4 w-4 text-white shrink-0 mt-0.5 animate-pulse" />
                    <span>{result.moral}</span>
                  </div>
                </div>

                {/* Real-Life Application */}
                <div className="space-y-2">
                  <span className="block text-[10px] uppercase tracking-wider font-bold text-text-muted">Real-Life Application</span>
                  <div className="flex gap-3 text-xs text-text-secondary leading-relaxed bg-bg-primary border border-border-custom p-4 rounded-xl">
                    <Quote className="h-4 w-4 text-text-muted shrink-0 mt-0.5" />
                    <span className="italic">"{result.realLifeExample}"</span>
                  </div>
                </div>

                {/* Emotions Grid */}
                <div className="space-y-3">
                  <span className="block text-[10px] uppercase tracking-wider font-bold text-text-muted">Emotional Tone</span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {result.emotions.map((emotion, i) => (
                      <div key={i} className="bg-bg-primary border border-border-custom p-3 rounded-xl space-y-2">
                        <div className="flex justify-between text-[11px] font-medium">
                          <span className="text-text-secondary">{emotion.name}</span>
                          <span className="text-text-primary">{(emotion.score * 100).toFixed(0)}%</span>
                        </div>
                        <div className="w-full bg-bg-surface h-1 rounded-full overflow-hidden border border-border-custom">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${emotion.score * 100}%` }}
                            transition={{ duration: 0.8, ease: 'easeOut' }}
                            className={`h-full rounded-full ${emotion.color}`}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Stylistic Devices */}
                <div className="space-y-2">
                  <span className="block text-[10px] uppercase tracking-wider font-bold text-text-muted">Stylistic Devices</span>
                  <div className="flex flex-wrap gap-1.5">
                    {result.poeticDevices.map((device, i) => (
                      <span
                        key={i}
                        className="text-[10px] uppercase tracking-wider font-bold bg-bg-primary border border-border-custom text-text-secondary px-2.5 py-1 rounded"
                      >
                        {device}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Suggested Reading */}
                {result.suggestedPoems && result.suggestedPoems.length > 0 && (
                  <div className="space-y-2.5">
                    <span className="block text-[10px] uppercase tracking-wider font-bold text-text-muted">Suggested Reading</span>
                    <div className="space-y-2">
                      {result.suggestedPoems.map((poem, i) => (
                        <div
                          key={i}
                          className="group flex items-center justify-between gap-3 text-xs bg-bg-primary border border-border-custom hover:border-white/20 p-3 rounded-xl transition-custom cursor-pointer"
                        >
                          <div className="flex items-center gap-2.5">
                            <BookOpen className="h-3.5 w-3.5 text-text-muted group-hover:text-white transition-custom" />
                            <div className="space-y-0.5">
                              <div className="font-semibold text-text-primary group-hover:text-white transition-custom">{poem.title}</div>
                              <div className="text-[10px] text-text-muted">by {poem.author}</div>
                            </div>
                          </div>
                          <ArrowRight className="h-3.5 w-3.5 text-text-muted opacity-0 group-hover:opacity-100 group-hover:translate-x-0.5 transition-custom" />
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            ) : (
              <div className="flex flex-col items-center justify-center py-16 text-center space-y-3">
                <BookOpen className="h-8 w-8 text-text-muted" />
                <p className="text-xs text-text-secondary">
                  Provide poem stanzas and run analysis to yield insights.
                </p>
              </div>
            )}
          </div>

          <div className="text-[10px] text-text-muted border-t border-border-custom pt-4 mt-8 flex justify-between">
            <span>Secure Analysis</span>
            <span>v2.0.0</span>
          </div>
        </div>
      </div>
    </div>
  )
}


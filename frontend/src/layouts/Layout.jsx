import { useState, useEffect, useRef } from 'react'
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { ShieldAlert, BookOpen, Film, Menu, X, ArrowRight, ChevronDown } from 'lucide-react'
import ElyraLogo from '../components/ElyraLogo'

export default function Layout() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const dropdownRef = useRef(null)
  const navigate = useNavigate()

  const navItems = [
    { name: 'Home', path: '/' },
    { name: 'Spam Analyzer', path: '/spam', icon: ShieldAlert },
    { name: 'Poem Analyzer', path: '/poem', icon: BookOpen },
    { name: 'Movie Analyzer', path: '/movie', icon: Film },
  ]

  // Dynamic header styling on scroll
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setScrolled(true)
      } else {
        setScrolled(false)
      }
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSelectTool = (path) => {
    setDropdownOpen(false)
    setMobileMenuOpen(false)
    navigate(path)
  }

  return (
    <div className="min-h-screen flex flex-col bg-bg-primary text-text-primary selection:bg-white/10 selection:text-text-primary">
      {/* Sticky Header with Backdrop Blur */}
      <header
        className={`sticky top-0 z-50 w-full transition-all duration-300 ${
          scrolled
            ? 'bg-bg-primary/70 backdrop-blur-md border-b border-border-custom py-3'
            : 'bg-transparent border-b border-transparent py-5'
        }`}
      >
        <div className="max-w-[1280px] mx-auto px-6 flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <ElyraLogo className="h-8 w-8" showText={true} textClass="h-4" />
            <span className="text-[10px] tracking-wider uppercase bg-bg-elevated text-text-muted font-semibold px-2 py-0.5 rounded-full border border-border-custom">
              v1.0
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1 bg-bg-surface/50 border border-border-custom px-1.5 py-1 rounded-full backdrop-blur-md">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `px-4 py-1.5 rounded-full text-sm font-medium tracking-tight transition-custom ${
                    isActive
                      ? 'bg-bg-elevated text-white border border-white/10'
                      : 'text-text-secondary hover:text-white hover:bg-bg-elevated/40'
                  }`
                }
              >
                {item.name}
              </NavLink>
            ))}
          </nav>

          {/* Right CTA Button & Dropdown */}
          <div className="hidden md:block relative" ref={dropdownRef}>
            <button
              onClick={() => setDropdownOpen(!dropdownOpen)}
              className="flex items-center gap-2 px-4 py-2 bg-white text-bg-primary rounded-full text-sm font-semibold tracking-tight hover:bg-white/90 transition-custom active:scale-95 cursor-pointer"
            >
              Analyze Now
              <ChevronDown className={`h-4 w-4 transition-transform duration-300 ${dropdownOpen ? 'rotate-185' : ''}`} />
            </button>

            {dropdownOpen && (
              <div className="absolute right-0 mt-2.5 w-60 bg-bg-surface border border-border-custom rounded-2xl p-2 shadow-2xl animate-fade-in">
                <div className="px-3 py-2 text-xs font-semibold uppercase tracking-wider text-text-muted">
                  Choose Pipeline
                </div>
                <div className="space-y-0.5">
                  {navItems.slice(1).map((item) => {
                    const Icon = item.icon
                    return (
                      <button
                        key={item.path}
                        onClick={() => handleSelectTool(item.path)}
                        className="w-full flex items-center justify-between text-left px-3 py-2.5 rounded-xl text-sm text-text-secondary hover:text-white hover:bg-bg-elevated/50 transition-custom group cursor-pointer"
                      >
                        <div className="flex items-center gap-3">
                          <Icon className="h-4 w-4 text-text-muted group-hover:text-white transition-colors" />
                          <span>{item.name}</span>
                        </div>
                        <ArrowRight className="h-3.5 w-3.5 opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all" />
                      </button>
                    )
                  })}
                </div>
              </div>
            )}
          </div>

          {/* Mobile menu trigger */}
          <div className="flex items-center gap-3 md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-text-secondary hover:text-white hover:bg-bg-elevated/40 rounded-full transition-custom"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation Drawer */}
        {mobileMenuOpen && (
          <div className="md:hidden absolute top-full left-0 w-full bg-bg-surface/95 border-b border-border-custom backdrop-blur-xl animate-slide-up">
            <div className="px-4 py-4 space-y-1.5 max-w-md mx-auto">
              {navItems.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={({ isActive }) =>
                    `block px-4 py-2.5 rounded-xl text-sm font-medium tracking-tight transition-custom ${
                      isActive
                        ? 'bg-bg-elevated text-white border border-white/10'
                        : 'text-text-secondary hover:text-white hover:bg-bg-elevated/40'
                    }`
                  }
                >
                  {item.name}
                </NavLink>
              ))}
              <div className="pt-3 border-t border-border-custom">
                <p className="px-4 pb-2 text-[10px] uppercase font-bold tracking-wider text-text-muted">Direct Analysis</p>
                <div className="grid grid-cols-3 gap-2 px-2">
                  <button onClick={() => handleSelectTool('/spam')} className="p-2 bg-bg-elevated rounded-xl border border-border-custom hover:border-white/20 text-center text-xs flex flex-col items-center gap-1 text-text-secondary hover:text-white transition-custom">
                    <ShieldAlert className="h-4 w-4" />
                    <span>Spam</span>
                  </button>
                  <button onClick={() => handleSelectTool('/poem')} className="p-2 bg-bg-elevated rounded-xl border border-border-custom hover:border-white/20 text-center text-xs flex flex-col items-center gap-1 text-text-secondary hover:text-white transition-custom">
                    <BookOpen className="h-4 w-4" />
                    <span>Poem</span>
                  </button>
                  <button onClick={() => handleSelectTool('/movie')} className="p-2 bg-bg-elevated rounded-xl border border-border-custom hover:border-white/20 text-center text-xs flex flex-col items-center gap-1 text-text-secondary hover:text-white transition-custom">
                    <Film className="h-4 w-4" />
                    <span>Movie</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </header>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col">
        <Outlet />
      </main>

      {/* Premium Editorial Footer */}
      <footer className="border-t border-border-custom bg-bg-surface py-16 text-xs text-text-muted mt-auto">
        <div className="max-w-[1280px] mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-10 md:gap-6 mb-12">
            {/* Branding Column */}
            <div className="md:col-span-2 space-y-4">
              <Link to="/">
                <ElyraLogo className="h-10 w-10" showText={true} showSubtitle={true} textClass="h-5" />
              </Link>
              <p className="text-text-secondary max-w-sm leading-relaxed">
                Advanced Content Intelligence. Redefining text metadata extraction, sentiment indexing, and genre synthesis through simple, elegant pipelines.
              </p>
            </div>

            {/* Quick Links */}
            <div className="space-y-3">
              <h4 className="text-white font-semibold tracking-wider uppercase text-[10px]">Pipelines</h4>
              <ul className="space-y-2">
                <li><Link to="/spam" className="hover:text-white transition-colors">Spam Analyzer</Link></li>
                <li><Link to="/poem" className="hover:text-white transition-colors">Poem Analyzer</Link></li>
                <li><Link to="/movie" className="hover:text-white transition-colors">Movie Analyzer</Link></li>
              </ul>
            </div>

            {/* Company / Legal */}
            <div className="space-y-3">
              <h4 className="text-white font-semibold tracking-wider uppercase text-[10px]">Developers</h4>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API Reference</a></li>
                <li><a href="#" className="hover:text-white transition-colors">System Status</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-border-custom pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
            <p>© {new Date().getFullYear()} ELYRA Platform. All rights reserved.</p>
            <div className="flex gap-6 text-text-muted">
              <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
              <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
              <a href="#" className="hover:text-white transition-colors">Security</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}


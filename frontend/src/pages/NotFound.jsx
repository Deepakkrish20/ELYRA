import { Link } from 'react-router-dom'
import { HelpCircle, ArrowLeft } from 'lucide-react'

export default function NotFound() {
  return (
    <div className="max-w-md mx-auto text-center py-32 px-6 flex flex-col items-center justify-center space-y-6">
      <HelpCircle className="h-12 w-12 text-text-muted mb-2 animate-pulse" />
      <h1 className="text-4xl font-extrabold tracking-tight text-white">404 - Not Found</h1>
      <p className="text-text-secondary text-sm leading-relaxed max-w-xs">
        The pipeline page you are requesting could not be located in our routing indexes.
      </p>
      <Link
        to="/"
        className="inline-flex items-center gap-2 bg-white hover:bg-white/90 text-bg-primary font-semibold py-2.5 px-6 rounded-full transition-custom text-xs tracking-tight"
      >
        <ArrowLeft className="h-4 w-4" />
        Return Home
      </Link>
    </div>
  )
}


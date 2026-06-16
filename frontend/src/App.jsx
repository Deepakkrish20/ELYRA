import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './layouts/Layout'
import Home from './pages/Home'
import SpamAnalyzer from './pages/SpamAnalyzer'
import PoemAnalyzer from './pages/PoemAnalyzer'
import MovieAnalyzer from './pages/MovieAnalyzer'
import NotFound from './pages/NotFound'

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="spam" element={<SpamAnalyzer />} />
          <Route path="poem" element={<PoemAnalyzer />} />
          <Route path="movie" element={<MovieAnalyzer />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </Router>
  )
}

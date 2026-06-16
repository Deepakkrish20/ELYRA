/**
 * Format percentages nicely
 */
export function formatPercentage(val) {
  return `${(val * 100).toFixed(0)}%`
}

/**
 * Truncate long strings for summaries
 */
export function truncateText(text, length = 100) {
  if (text.length <= length) return text
  return text.substring(0, length) + '...'
}

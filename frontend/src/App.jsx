import { useState, useEffect } from 'react'
import './App.css'

const API_BASE_URL = 'http://127.0.0.1:8000'

function App() {
  const [menu, setMenu] = useState(null)
  const [preferences, setPreferences] = useState(null)
  const [history, setHistory] = useState(null)
  const [recommendation, setRecommendation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [selectedFood, setSelectedFood] = useState(null)
  const [feedbackSent, setFeedbackSent] = useState(false)

  useEffect(() => {
    fetchMenu()
    fetchPreferences()
    fetchHistory()
  }, [])

  const fetchMenu = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/menu`)
      if (!response.ok) throw new Error('Failed to fetch menu')
      const data = await response.json()
      setMenu(data)
    } catch (err) {
      setError('Could not load menu. Is the backend running?')
    }
  }

  const fetchPreferences = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/preferences`)
      if (!response.ok) throw new Error('Failed to fetch preferences')
      const data = await response.json()
      setPreferences(data)
    } catch (err) {
      console.error('Failed to fetch preferences:', err)
    }
  }

  const fetchHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/history`)
      if (!response.ok) throw new Error('Failed to fetch history')
      const data = await response.json()
      setHistory(data)
    } catch (err) {
      console.error('Failed to fetch history:', err)
    }
  }

  const getRecommendation = async () => {
    setLoading(true)
    setError(null)
    setRecommendation(null)
    setFeedbackSent(false)
    setSelectedFood(null)

    try {
      const response = await fetch(`${API_BASE_URL}/recommend`, {
        method: 'POST',
      })
      if (!response.ok) throw new Error('Failed to get recommendation')
      const data = await response.json()
      setRecommendation(data)
    } catch (err) {
      setError('Could not get recommendation. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const submitFeedback = async (action, feedbackText) => {
    if (!selectedFood) {
      alert('Please select a food first')
      return
    }

    try {
      const response = await fetch(`${API_BASE_URL}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          food: selectedFood,
          action,
          feedback: feedbackText,
        }),
      })

      if (!response.ok) throw new Error('Failed to submit feedback')

      setFeedbackSent(true)
      fetchHistory()
    } catch (err) {
      setError('Could not submit feedback. Please try again.')
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1 className="title">EeshApp</h1>
        <p className="subtitle">Your mess-food companion</p>
      </header>

      {error && <div className="error">{error}</div>}

      {menu && (
        <section className="section">
          <h2 className="section-title">
            {menu.day} • {menu.meal}
          </h2>
          <div className="menu-list">
            {menu.menu.map((food) => (
              <div key={food} className="food-card">
                {food}
              </div>
            ))}
          </div>
        </section>
      )}

      <section className="section">
        <h2 className="section-title">What should I eat?</h2>
        <button
          className="recommend-button"
          onClick={getRecommendation}
          disabled={loading}
        >
          {loading ? 'Thinking...' : 'Get my recommendation'}
        </button>

        {recommendation && (
          <div className="recommendation">
            <div className="recommendation-text">
              {recommendation.recommendation}
            </div>

            {!feedbackSent && (
              <div className="feedback-section">
                <h3 className="feedback-title">How did it go?</h3>
                <div className="food-selector">
                  <p className="food-selector-label">Select food:</p>
                  {recommendation.menu.map((food) => (
                    <button
                      key={food}
                      className={`food-selector-button ${
                        selectedFood === food ? 'selected' : ''
                      }`}
                      onClick={() => setSelectedFood(food)}
                    >
                      {food}
                    </button>
                  ))}
                </div>
                <div className="feedback-buttons">
                  <button
                    className="feedback-button"
                    onClick={() => submitFeedback('ate', 'Ate as suggested')}
                  >
                    Ate it 👍
                  </button>
                  <button
                    className="feedback-button"
                    onClick={() => submitFeedback('ate', "Didn't like it")}
                  >
                    Didn't like it
                  </button>
                  <button
                    className="feedback-button"
                    onClick={() => submitFeedback('skipped', 'Skipped')}
                  >
                    Skipped
                  </button>
                  <button
                    className="feedback-button"
                    onClick={() =>
                      submitFeedback('ordered_outside', 'Ordered outside')
                    }
                  >
                    Ordered outside
                  </button>
                </div>
              </div>
            )}

            {feedbackSent && (
              <div className="feedback-success">
                Thanks for your feedback! ✨
              </div>
            )}
          </div>
        )}
      </section>

      {preferences && preferences.preferences.length > 0 && (
        <section className="section preferences-section">
          <h2 className="section-title">What Eesha likes</h2>
          <div className="preferences-list">
            {preferences.preferences
              .filter((p) => p.preference === 'like')
              .map((pref) => (
                <span key={pref.food} className="preference-tag like">
                  {pref.food}
                </span>
              ))}
            {preferences.preferences
              .filter((p) => p.preference === 'dislike')
              .map((pref) => (
                <span key={pref.food} className="preference-tag dislike">
                  {pref.food}
                </span>
              ))}
          </div>
        </section>
      )}

      {history && history.history.length > 0 && (
        <section className="section history-section">
          <h2 className="section-title">Recent meals</h2>
          <div className="history-list">
            {history.history.slice(0, 3).map((entry) => (
              <div key={entry.id} className="history-item">
                <span className="history-date">{entry.date}</span>
                <span className="history-food">{entry.food}</span>
                <span className="history-action">{entry.action}</span>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}

export default App

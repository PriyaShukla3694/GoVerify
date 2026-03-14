import { useState, useRef, useEffect } from 'react';

export function useBehaviorTracker(sessionId) {
  const [metrics, setMetrics] = useState({
    typing_speed: 0,
    error_rate: 0,
    pause_time: 0,
  });

  const stateRef = useRef({
    startTime: null,
    totalKeystrokes: 0,
    backspaces: 0,
    lastFocusTime: null,
    totalPauses: 0,
    pauseCount: 0,
  });

  // Attach these handlers to input fields
  const handlers = {
    onKeyDown: (e) => {
      const state = stateRef.current;
      if (!state.startTime) state.startTime = Date.now();
      
      state.totalKeystrokes++;
      if (e.key === 'Backspace' || e.key === 'Delete') {
        state.backspaces++;
      }
    },
    onFocus: () => {
      const state = stateRef.current;
      if (state.lastFocusTime) {
        const pause = Date.now() - state.lastFocusTime;
        state.totalPauses += pause;
        state.pauseCount++;
      }
    },
    onBlur: () => {
      stateRef.current.lastFocusTime = Date.now();
      calculateMetrics();
    }
  };

  const calculateMetrics = async () => {
    const state = stateRef.current;
    if (!state.startTime || state.totalKeystrokes < 5) return;

    const timeElapsedSec = (Date.now() - state.startTime) / 1000;
    const typing_speed = (state.totalKeystrokes / timeElapsedSec) * 60; // CPM
    const error_rate = state.backspaces / state.totalKeystrokes;
    const pause_time = state.pauseCount > 0 ? (state.totalPauses / state.pauseCount) : 0;

    const newMetrics = { typing_speed, error_rate, pause_time };
    setMetrics(newMetrics);

    // Send asynchronously to backend to predict
    try {
      const response = await fetch('http://localhost:5000/api/v1/metrics/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...newMetrics, session_id: sessionId })
      });
      const data = await response.json();
      
      // Dispatch custom event if easy mode is suggested
      if (data.suggest_easy_mode) {
        window.dispatchEvent(new CustomEvent('SUGGEST_EASY_MODE', { detail: data.literacy_level }));
      }
    } catch (e) {
      console.warn("Telemetry API unreachable", e);
    }
  };

  return { handlers, metrics };
}

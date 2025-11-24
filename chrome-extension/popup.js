// Popup script for YouTube Sentiment Analyzer
console.log('Popup script loaded');

// Global variables
let allResults = [];
let currentFilter = 'all';

// DOM elements
const apiUrlInput = document.getElementById('api-url');
const testApiBtn = document.getElementById('test-api');
const apiStatus = document.getElementById('api-status');
const analyzeBtn = document.getElementById('analyze-btn');
const loading = document.getElementById('loading');
const statistics = document.getElementById('statistics');
const filterControls = document.getElementById('filter-controls');
const results = document.getElementById('results');
const error = document.getElementById('error');
const exportBtn = document.getElementById('export-btn');
const darkModeToggle = document.getElementById('dark-mode-toggle');

// Load saved API URL and dark mode preference
chrome.storage.local.get(['apiUrl', 'darkMode'], (data) => {
  if (data.apiUrl) {
    apiUrlInput.value = data.apiUrl;
  }
  if (data.darkMode) {
    document.body.classList.add('dark-mode');
    darkModeToggle.textContent = '‚òÄÔ∏è';
  }
});

// Save API URL on change
apiUrlInput.addEventListener('change', () => {
  chrome.storage.local.set({ apiUrl: apiUrlInput.value });
});

// Test API connection
testApiBtn.addEventListener('click', async () => {
  const apiUrl = apiUrlInput.value.trim();
  
  apiStatus.textContent = 'Testing connection...';
  apiStatus.className = 'status-message';
  
  try {
    const response = await fetch(`${apiUrl}/health`);
    const data = await response.json();
    
    if (data.status === 'healthy') {
      apiStatus.textContent = '‚úÖ API is healthy and ready!';
      apiStatus.classList.add('success');
    } else {
      throw new Error('API returned unhealthy status');
    }
  } catch (err) {
    apiStatus.textContent = '‚ùå Connection failed. Check API URL.';
    apiStatus.classList.add('error');
    console.error('API test error:', err);
  }
});

// Analyze comments
analyzeBtn.addEventListener('click', async () => {
  const apiUrl = apiUrlInput.value.trim();
  
  // Hide previous results/errors
  hideAll();
  loading.classList.remove('hidden');
  
  try {
    // Get active tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Check if we're on YouTube
    if (!tab.url.includes('youtube.com')) {
      throw new Error('Please navigate to a YouTube video page');
    }
    
    // Extract comments from the page
    const response = await chrome.tabs.sendMessage(tab.id, { action: 'extractComments' });
    
    if (!response || !response.comments || response.comments.length === 0) {
      throw new Error('No comments found. Try scrolling down to load more comments.');
    }
    
    console.log(`Extracted ${response.comments.length} comments`);
    
    // Prepare API request
    const commentsForApi = response.comments.map(c => ({ text: c.text }));
    
    // Call sentiment analysis API
    const apiResponse = await fetch(`${apiUrl}/predict_batch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ comments: commentsForApi })
    });
    
    if (!apiResponse.ok) {
      throw new Error(`API error: ${apiResponse.status}`);
    }
    
    const data = await apiResponse.json();
    
    // Store results
    allResults = data.results.map((result, index) => ({
      ...result,
      author: response.comments[index].author,
      timestamp: response.comments[index].timestamp
    }));
    
    // Display results
    displayStatistics(data.statistics, data.processing_time_ms);
    displayResults(allResults);
    
    // Show UI elements
    loading.classList.add('hidden');
    statistics.classList.remove('hidden');
    filterControls.classList.remove('hidden');
    results.classList.remove('hidden');
    exportBtn.classList.remove('hidden');
    
  } catch (err) {
    loading.classList.add('hidden');
    error.textContent = `Error: ${err.message}`;
    error.classList.remove('hidden');
    console.error('Analysis error:', err);
  }
});

// Display statistics
function displayStatistics(stats, processingTime) {
  document.getElementById('positive-count').textContent = stats.positive;
  document.getElementById('neutral-count').textContent = stats.neutral;
  document.getElementById('negative-count').textContent = stats.negative;
  
  document.getElementById('positive-percent').textContent = `${stats.positive_percentage}%`;
  document.getElementById('neutral-percent').textContent = `${stats.neutral_percentage}%`;
  document.getElementById('negative-percent').textContent = `${stats.negative_percentage}%`;
  
  document.getElementById('total-comments').textContent = stats.total_comments;
  document.getElementById('processing-time').textContent = `${processingTime}ms`;
  document.getElementById('avg-confidence').textContent = `${(stats.average_confidence * 100).toFixed(1)}%`;
}

// Display results
function displayResults(resultsToDisplay) {
  results.innerHTML = '';
  
  const filteredResults = currentFilter === 'all' 
    ? resultsToDisplay 
    : resultsToDisplay.filter(r => r.sentiment === currentFilter);
  
  if (filteredResults.length === 0) {
    results.innerHTML = '<p style="text-align: center; padding: 20px; color: #999;">No comments match this filter</p>';
    return;
  }
  
  filteredResults.forEach((result) => {
    const item = document.createElement('div');
    item.className = `result-item ${result.sentiment}`;
    
    const sentimentEmoji = {
      'positive': 'Ì∏ä',
      'neutral': 'Ì∏ê',
      'negative': 'Ì∏û'
    };
    
    item.innerHTML = `
      <div class="result-text">${escapeHtml(result.text)}</div>
      <div class="result-meta">
        <span>${sentimentEmoji[result.sentiment]} ${capitalizeFirst(result.sentiment)}</span>
        <span>Confidence: ${(result.confidence * 100).toFixed(1)}%</span>
      </div>
    `;
    
    results.appendChild(item);
  });
}

// Filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    // Update active state
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    // Update filter and redisplay
    currentFilter = btn.dataset.filter;
    displayResults(allResults);
  });
});

// Export results
exportBtn.addEventListener('click', () => {
  const csvContent = generateCSV(allResults);
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `youtube-sentiment-analysis-${Date.now()}.csv`;
  a.click();
  
  URL.revokeObjectURL(url);
});

// Dark mode toggle
darkModeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  const isDark = document.body.classList.contains('dark-mode');
  darkModeToggle.textContent = isDark ? '‚òÄÔ∏è' : 'Ìºô';
  chrome.storage.local.set({ darkMode: isDark });
});

// Utility functions
function hideAll() {
  loading.classList.add('hidden');
  statistics.classList.add('hidden');
  filterControls.classList.add('hidden');
  results.classList.add('hidden');
  error.classList.add('hidden');
  exportBtn.classList.add('hidden');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function capitalizeFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function generateCSV(data) {
  const headers = ['Text', 'Sentiment', 'Confidence', 'Author', 'Timestamp'];
  const rows = data.map(r => [
    `"${r.text.replace(/"/g, '""')}"`,
    r.sentiment,
    r.confidence.toFixed(4),
    r.author || '',
    r.timestamp || ''
  ]);
  
  return [
    headers.join(','),
    ...rows.map(row => row.join(','))
  ].join('\n');
}

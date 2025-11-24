// Content script to extract YouTube comments
console.log('YouTube Sentiment Analyzer: Content script loaded');

// Function to extract visible comments from the page
function extractComments() {
  const comments = [];
  
  // YouTube comment selectors
  const commentElements = document.querySelectorAll('ytd-comment-thread-renderer');
  
  commentElements.forEach((element, index) => {
    try {
      // Get comment text
      const commentTextElement = element.querySelector('#content-text');
      
      if (commentTextElement) {
        const text = commentTextElement.innerText.trim();
        
        if (text && text.length > 0) {
          comments.push({
            id: index,
            text: text,
            author: element.querySelector('#author-text')?.innerText.trim() || 'Unknown',
            timestamp: element.querySelector('.published-time-text')?.innerText.trim() || ''
          });
        }
      }
    } catch (error) {
      console.error('Error extracting comment:', error);
    }
  });
  
  return comments;
}

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'extractComments') {
    console.log('Extracting comments...');
    const comments = extractComments();
    console.log(`Found ${comments.length} comments`);
    sendResponse({ comments: comments });
  }
  return true; // Keep message channel open for async response
});

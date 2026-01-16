// Video hover functionality
function initializeVideoHover() {
  document.querySelectorAll('.publication-media video').forEach(video => {
    video.addEventListener('mouseenter', () => {
      video.play();
    });

    video.addEventListener('mouseleave', () => {
      video.pause();
      video.currentTime = 0;
    });
  });
}

// Utility function to convert multi-line text to single line
function convertToSingleLine(input) {
  return input.replace(/\s+/g, ' ').trim();
}

// Share content functionality
function shareContent(button) {
  let contentSection = button.closest('.publication');
  let contentId, contentTitle;

  if (contentSection) {
    contentId = contentSection.id;
    contentTitle = contentSection.querySelector('a').textContent;
  } else {
    contentSection = button.closest('.header');
    contentId = "";
    contentTitle = contentSection.querySelector('h1').textContent;
  }

  contentTitle = convertToSingleLine(contentTitle);

  const shareUrl = window.location.origin + window.location.pathname + '#' + contentId;

  let shareText;
  if (contentId.startsWith('article')) {
    shareText = 'Check out this article: ' + contentTitle;
  } else if (contentId.startsWith('tutorial')) {
    shareText = 'I found this helpful tutorial: ' + contentTitle;
  } else {
    shareText = 'Check this out: ' + contentTitle;
  }

  if (navigator.share) {
    navigator.share({
      title: contentTitle,
      text: shareText,
      url: shareUrl
    })
    .then(() => console.log('Share successful'))
    .catch((error) => console.log('Error sharing:', error));
  } else {
    const shareLinks = {
      facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`,
      twitter: `https://twitter.com/intent/tweet?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(shareText)}`,
      linkedin: `https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(shareUrl)}&title=${encodeURIComponent(contentTitle)}`,
      email: `mailto:?subject=${encodeURIComponent(contentTitle)}&body=${encodeURIComponent(shareText + '\n\n' + shareUrl)}`
    };

    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '50%';
    modal.style.left = '50%';
    modal.style.transform = 'translate(-50%, -50%)';
    modal.style.backgroundColor = 'white';
    modal.style.padding = '20px';
    modal.style.borderRadius = '5px';
    modal.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
    modal.style.zIndex = '1000';

    modal.innerHTML = `
      <h3>Share: ${contentTitle}</h3>
      <p><a href="${shareLinks.facebook}" target="_blank">Share on Facebook</a></p>
      <p><a href="${shareLinks.twitter}" target="_blank">Share on Twitter</a></p>
      <p><a href="${shareLinks.linkedin}" target="_blank">Share on LinkedIn</a></p>
      <p><a href="${shareLinks.email}">Share via Email</a></p>
      <button onclick="this.parentNode.remove()">Close</button>
    `;

    document.body.appendChild(modal);
  }
}

// Add share buttons to all content sections
function addShareButtons() {
  const contentSections = document.querySelectorAll('.publication-details');

  contentSections.forEach(section => {
    const shareButton = document.createElement('button');
    shareButton.className = 'share-button';
    shareButton.textContent = 'Share';

    const sectionId = section.id;
    if (sectionId.startsWith('article')) {
      shareButton.textContent = 'Share This Article';
    } else if (sectionId.startsWith('tutorial')) {
      shareButton.textContent = 'Share This Tutorial';
    }

    shareButton.addEventListener('click', function() {
      shareContent(this);
    });

    section.appendChild(shareButton);
  });
}

// Initialize all functionality when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  initializeVideoHover();
  addShareButtons();
});
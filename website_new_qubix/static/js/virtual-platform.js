// Virtual Platform specific functionality

document.addEventListener('DOMContentLoaded', function() {
    initPlatformDemo();
    initPricingCalculator();
    initVideoPlayer();
});

// Platform demo functionality
function initPlatformDemo() {
    const demoBtn = document.querySelector('.demo-btn');
    const demoModal = document.querySelector('.demo-modal');
    
    if (demoBtn && demoModal) {
        demoBtn.addEventListener('click', function() {
            demoModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });

        demoModal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
    }
}

// Pricing calculator
function initPricingCalculator() {
    const attendeeSlider = document.querySelector('#attendee-count');
    const durationSlider = document.querySelector('#event-duration');
    const priceDisplay = document.querySelector('#calculated-price');
    
    if (attendeeSlider && durationSlider && priceDisplay) {
        function calculatePrice() {
            const attendees = parseInt(attendeeSlider.value);
            const duration = parseInt(durationSlider.value);
            
            let basePrice = 50000; // Base price in INR
            let attendeeMultiplier = Math.ceil(attendees / 100) * 0.1;
            let durationMultiplier = duration * 0.2;
            
            let totalPrice = basePrice * (1 + attendeeMultiplier + durationMultiplier);
            
            priceDisplay.textContent = `₹${totalPrice.toLocaleString('en-IN')}`;
        }
        
        attendeeSlider.addEventListener('input', calculatePrice);
        durationSlider.addEventListener('input', calculatePrice);
        
        calculatePrice(); // Initial calculation
    }
}

// Video player functionality
function initVideoPlayer() {
    const videoThumbnails = document.querySelectorAll('.video-thumbnail');
    
    videoThumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            const videoId = this.dataset.videoId;
            const videoContainer = this.parentElement;
            
            const iframe = document.createElement('iframe');
            iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
            iframe.frameBorder = '0';
            iframe.allowFullscreen = true;
            iframe.style.width = '100%';
            iframe.style.height = '100%';
            iframe.style.position = 'absolute';
            iframe.style.top = '0';
            iframe.style.left = '0';
            
            videoContainer.appendChild(iframe);
            this.style.display = 'none';
        });
    });
}

// Feature comparison functionality
function initFeatureComparison() {
    const comparisonTable = document.querySelector('.feature-comparison');
    
    if (comparisonTable) {
        const rows = comparisonTable.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#f8fafc';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });
    }
}

// Platform capabilities showcase
function initCapabilitiesShowcase() {
    const capabilityCards = document.querySelectorAll('.capability-card');
    
    capabilityCards.forEach(card => {
        card.addEventListener('click', function() {
            const details = this.querySelector('.capability-details');
            const isExpanded = details.style.display === 'block';
            
            // Close all other cards
            capabilityCards.forEach(otherCard => {
                if (otherCard !== this) {
                    otherCard.querySelector('.capability-details').style.display = 'none';
                    otherCard.classList.remove('expanded');
                }
            });
            
            // Toggle current card
            details.style.display = isExpanded ? 'none' : 'block';
            this.classList.toggle('expanded', !isExpanded);
        });
    });
}

document.addEventListener("DOMContentLoaded", function() {
    // Filter functionality for conference directory
    const filterBtn = document.getElementById('filter-btn');
    if(filterBtn) {
        filterBtn.addEventListener('click', filterPackages);
    }
    
    // Cost calculator functionality
    const calculateBtn = document.getElementById('calculate-btn');
    if(calculateBtn) {
        calculateBtn.addEventListener('click', calculateCosts);
    }
    
    // Initialize any tabs
    initTabs();
});

// Filter packages based on selected criteria
function filterPackages() {
    const attendees = document.getElementById('attendees').value;
    const budget = document.getElementById('budget').value;
    const type = document.getElementById('type').value;
    
    // Get all package cards
    const packages = document.querySelectorAll('.package-card');
    
    packages.forEach(package => {
        let showPackage = true;
        
        // Filter by attendees
        if(attendees !== 'all') {
            const packageSize = package.getAttribute('data-size');
            if(packageSize !== attendees) {
                showPackage = false;
            }
        }
        
        // Filter by budget
        if(budget !== 'all' && showPackage) {
            const packageBudget = package.getAttribute('data-budget');
            if(packageBudget !== budget) {
                showPackage = false;
            }
        }
        
        // Filter by type
        if(type !== 'all' && showPackage) {
            const packageTypes = package.getAttribute('data-type').split(',');
            if(!packageTypes.includes(type)) {
                showPackage = false;
            }
        }
        
        // Show or hide based on filters
        if(showPackage) {
            package.style.display = 'block';
        } else {
            package.style.display = 'none';
        }
    });
}

// Calculate estimated conference costs
function calculateCosts() {
    const attendees = parseInt(document.getElementById('est-attendees').value);
    const duration = parseInt(document.getElementById('est-duration').value);
    
    // Get selected services
    const venue = document.querySelector('input[value="venue"]').checked;
    const av = document.querySelector('input[value="av"]').checked;
    const catering = document.querySelector('input[value="catering"]').checked;
    const decor = document.querySelector('input[value="decor"]').checked;
    const registration = document.querySelector('input[value="registration"]').checked;
    
    // Base calculations (these would be loaded from your cost database in a real implementation)
    const venueCostPerPerson = 800; // ₹800 per person per day
    const avBaseCost = 15000; // ₹15,000 base cost
    const avCostPerPerson = 200; // ₹200 per person
    const cateringCostPerPerson = 1200; // ₹1,200 per person per day
    const decorBaseCost = 20000; // ₹20,000 base cost
    const registrationCostPerPerson = 300; // ₹300 per person
    
    // Calculate individual costs
    let venueCost = venue ? venueCostPerPerson * attendees * duration : 0;
    let avCost = av ? avBaseCost + (avCostPerPerson * attendees) : 0;
    let cateringCost = catering ? cateringCostPerPerson * attendees * duration : 0;
    let decorCost = decor ? decorBaseCost + (attendees * 100) : 0;
    let registrationCost = registration ? registrationCostPerPerson * attendees : 0;
    
    // Calculate total
    const totalCost = venueCost + avCost + cateringCost + decorCost + registrationCost;
    
    // Format numbers with commas for Indian numbering system
    function formatIndianCurrency(num) {
        return num.toString().replace(/(\d)(?=(\d\d)+\d$)/g, "$1,");
    }
    
    // Display the results
    const resultsDiv = document.getElementById('cost-breakdown');
    
    resultsDiv.innerHTML = `
        <div class="cost-breakdown">
            ${venue ? `<div class="cost-item">
                <span class="cost-label">Venue Rental:</span>
                <span class="cost-value">₹${formatIndianCurrency(venueCost)}</span>
            </div>` : ''}
            
            ${av ? `<div class="cost-item">
                <span class="cost-label">Audio-Visual Equipment:</span>
                <span class="cost-value">₹${formatIndianCurrency(avCost)}</span>
            </div>` : ''}
            
            ${catering ? `<div class="cost-item">
                <span class="cost-label">Catering:</span>
                <span class="cost-value">₹${formatIndianCurrency(cateringCost)}</span>
            </div>` : ''}
            
            ${decor ? `<div class="cost-item">
                <span class="cost-label">Decor & Staging:</span>
                <span class="cost-value">₹${formatIndianCurrency(decorCost)}</span>
            </div>` : ''}
            
            ${registration ? `<div class="cost-item">
                <span class="cost-label">Registration Services:</span>
                <span class="cost-value">₹${formatIndianCurrency(registrationCost)}</span>
            </div>` : ''}
            
            <div class="cost-item total">
                <span class="cost-label">Total Estimated Cost:</span>
                <span class="cost-value">₹${formatIndianCurrency(totalCost)}</span>
            </div>
        </div>
        <p class="disclaimer">Note: This is an approximate estimate. Contact us for a detailed quote.</p>
        <button class="btn btn-primary request-quote-btn">Request Detailed Quote</button>
    `;
    
    // Add event listener to the new button
    const requestQuoteBtn = document.querySelector('.request-quote-btn');
    if(requestQuoteBtn) {
        requestQuoteBtn.addEventListener('click', function() {
            window.location.href = '/contact.html?type=detailed-quote&attendees=' + attendees;
        });
    }
}

// Initialize tabs functionality
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    
    if(tabBtns.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                // Remove active class from all tabs
                tabBtns.forEach(b => b.classList.remove('active'));
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Hide all tab content
                const tabContents = document.querySelectorAll('.tab-content');
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Show the selected tab content
                const tabToShow = this.getAttribute('data-tab');
                document.getElementById(`${tabToShow}-tab`).classList.add('active');
            });
        });
    }
}

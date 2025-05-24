// Function to include HTML components
function includeHTML() {
    const includeElements = document.querySelectorAll('[data-include]');
    
    includeElements.forEach(function(element) {
        const file = element.getAttribute("data-include");
        
        fetch(file)
            .then(response => {
                if (response.ok) {
                    return response.text();
                }
                return Promise.reject(response);
            })
            .then(text => {
                element.innerHTML = text;
                element.removeAttribute("data-include");
                
                // Execute any scripts that were in the included HTML
                const scripts = element.querySelectorAll('script');
                scripts.forEach(script => {
                    const newScript = document.createElement('script');
                    
                    if (script.src) {
                        newScript.src = script.src;
                    } else {
                        newScript.textContent = script.textContent;
                    }
                    
                    document.head.appendChild(newScript);
                    script.remove();
                });
            })
            .catch(error => {
                console.warn(`Error loading ${file}: ${error}`);
                element.innerHTML = "Component could not be loaded";
            });
    });
}

// Execute when DOM is fully loaded
document.addEventListener('DOMContentLoaded', includeHTML);

document.addEventListener("DOMContentLoaded", function() {
    // Admin functionality for updating costs
    
    // Save Basic Package button
    const saveBasicBtn = document.getElementById('save-basic');
    if(saveBasicBtn) {
        saveBasicBtn.addEventListener('click', saveBasicPackage);
    }
    
    // Save Add-ons button
    const saveAddonsBtn = document.getElementById('save-addons');
    if(saveAddonsBtn) {
        saveAddonsBtn.addEventListener('click', saveAddons);
    }
    
    // Save All Changes button
    const saveAllBtn = document.getElementById('save-all-changes');
    if(saveAllBtn) {
        saveAllBtn.addEventListener('click', saveAllChanges);
    }
    
    // Restore Defaults button
    const restoreDefaultsBtn = document.getElementById('restore-defaults');
    if(restoreDefaultsBtn) {
        restoreDefaultsBtn.addEventListener('click', restoreDefaults);
    }
});

// Save Basic Package costs
function saveBasicPackage() {
    // Get all the input values
    const minPrice = document.getElementById('basic-min-price').value;
    const maxPrice = document.getElementById('basic-max-price').value;
    const stagePrice = document.getElementById('basic-stage').value;
    const audioPrice = document.getElementById('basic-audio').value;
    const micsPrice = document.getElementById('basic-mics').value;
    const screenPrice = document.getElementById('basic-screen').value;
    const projectorPrice = document.getElementById('basic-projector').value;
    const backdropPrice = document.getElementById('basic-backdrop').value;
    
    // In a real application, you would send this data to a server
    // Here we'll simulate success with an alert
    
    const costsData = {
        minPrice,
        maxPrice,
        components: {
            stage: stagePrice,
            audio: audioPrice,
            mics: micsPrice,
            screen: screenPrice,
            projector: projectorPrice,
            backdrop: backdropPrice
        }
    };
    
    console.log('Saving Basic Package:', costsData);
    
    // Simulate API call with a delay
    setTimeout(() => {
        showSuccessMessage('Basic Package costs updated successfully!');
    }, 1000);
}

// Save Add-ons costs
function saveAddons() {
    // Get all the input values for add-ons
    const laptopPrice = document.getElementById('addon-laptop').value;
    const clickerPrice = document.getElementById('addon-clicker').value;
    const pointerPrice = document.getElementById('addon-pointer').value;
    const standeePrice = document.getElementById('addon-standee').value;
    const internetMinPrice = document.getElementById('addon-internet-min').value;
    const internetMaxPrice = document.getElementById('addon-internet-max').value;
    const lapelPrice = document.getElementById('addon-lapel').value;
    const pendrivePrice = document.getElementById('addon-pendrive').value;
    
    // In a real application, you would send this data to a server
    
    const addonsData = {
        laptop: laptopPrice,
        clicker: clickerPrice,
        pointer: pointerPrice,
        standee: standeePrice,
        internetMin: internetMinPrice,
        internetMax: internetMaxPrice,
        lapel: lapelPrice,
        pendrive: pendrivePrice
    };
    
    console.log('Saving Add-ons:', addonsData);
    
    // Simulate API call with a delay
    setTimeout(() => {
        showSuccessMessage('Add-ons costs updated successfully!');
    }, 1000);
}

// Save all changes
function saveAllChanges() {
    // This would save all packages and add-ons
    console.log('Saving all changes...');
    
    // Simulate API call with a delay
    setTimeout(() => {
        showSuccessMessage('All costs updated successfully!');
    }, 1500);
}

// Restore default values
function restoreDefaults() {
    // This would reset all inputs to default values from the server
    console.log('Restoring default values...');
    
    if(confirm('Are you sure you want to restore all costs to default values? This will discard any unsaved changes.')) {
        // Simulate API call with a delay
        setTimeout(() => {
            // Basic Package defaults
            document.getElementById('basic-min-price').value = 27000;
            document.getElementById('basic-max-price').value = 37000;
            document.getElementById('basic-stage').value = 8000;
            document.getElementById('basic-audio').value = 10000;
            document.getElementById('basic-mics').value = 3000;
            document.getElementById('basic-screen').value = 2500;
            document.getElementById('basic-projector').value = 3500;
            document.getElementById('basic-backdrop').value = 6000;
            
            // Add-ons defaults
            document.getElementById('addon-laptop').value = 2000;
            document.getElementById('addon-clicker').value = 600;
            document.getElementById('addon-pointer').value = 500;
            document.getElementById('addon-standee').value = 1200;
            document.getElementById('addon-internet-min').value = 4000;
            document.getElementById('addon-internet-max').value = 10000;
            document.getElementById('addon-lapel').value = 700;
            document.getElementById('addon-pendrive').value = 400;
            
            showSuccessMessage('All costs restored to default values!');
        }, 1000);
    }
}

// Show success message
function showSuccessMessage(message) {
    // Create a success message element
    const successMsg = document.createElement('div');
    successMsg.classList.add('success-message');
    successMsg.textContent = message;
    
    // Add it to the page
    document.body.appendChild(successMsg);
    
    // Remove it after a delay
    setTimeout(() => {
        successMsg.classList.add('fade-out');
        setTimeout(() => {
            document.body.removeChild(successMsg);
        }, 500);
    }, 3000);
}

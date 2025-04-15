document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const sourceText = document.getElementById('source-text');
    const targetText = document.getElementById('target-text');
    const detectedLanguage = document.getElementById('detected-language');
    const targetLanguage = document.getElementById('target-language');
    const swapBtn = document.getElementById('swap-btn');
    const sourceAudioBtn = document.getElementById('source-audio-btn');
    const targetAudioBtn = document.getElementById('target-audio-btn');
    
    // Variables
    let lastDetectedLanguage = null;
    let typingTimer;
    const doneTypingInterval = 500; // Time in ms (0.5 seconds)
    
    // Initialize
    function init() {
        // Clear initial values
        sourceText.value = '';
        targetText.value = '';
        detectedLanguage.textContent = 'Detecting language...';
        
        // Event listeners
        sourceText.addEventListener('input', handleSourceTextChange);
        targetLanguage.addEventListener('change', handleTranslation);
        swapBtn.addEventListener('click', handleSwapLanguages);
        sourceAudioBtn.addEventListener('click', () => handleSpeakText(sourceText.value, lastDetectedLanguage));
        targetAudioBtn.addEventListener('click', () => handleSpeakText(targetText.value, targetLanguage.value));
    }
    
    // Handle source text change
    function handleSourceTextChange() {
        clearTimeout(typingTimer);
        
        if (sourceText.value) {
            // Reset timer
            typingTimer = setTimeout(function() {
                detectLanguage();
            }, doneTypingInterval);
        } else {
            // Clear target text if source is empty
            targetText.value = '';
            detectedLanguage.textContent = 'Detecting language...';
        }
    }
    
    // Detect language
    async function detectLanguage() {
        if (!sourceText.value.trim()) {
            detectedLanguage.textContent = 'Detecting language...';
            return;
        }
        
        try {
            const response = await fetch('/api/detect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: sourceText.value
                })
            });
            
            const data = await response.json();
            
            if (data.success && data.language) {
                detectedLanguage.textContent = data.language.name;
                lastDetectedLanguage = data.language.code;
                
                // Automatically translate after detecting language
                handleTranslation();
            } else {
                detectedLanguage.textContent = 'Unknown';
                lastDetectedLanguage = null;
            }
        } catch (error) {
            console.error('Error detecting language:', error);
            detectedLanguage.textContent = 'Error detecting';
        }
    }
    
    // Handle translation
    async function handleTranslation() {
        if (!sourceText.value.trim()) {
            targetText.value = '';
            return;
        }
        
        try {
            const response = await fetch('/api/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: sourceText.value,
                    target_lang: targetLanguage.value,
                    source_lang: lastDetectedLanguage
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                targetText.value = data.translated_text;
            } else {
                targetText.value = 'Translation error: ' + (data.error || 'Unknown error');
            }
        } catch (error) {
            console.error('Error translating:', error);
            targetText.value = 'Translation service error';
        }
    }
    
    // Handle swap languages
    function handleSwapLanguages() {
        // Only allow swap if we have a detected language
        if (!lastDetectedLanguage) return;
        
        const tempText = sourceText.value;
        sourceText.value = targetText.value;
        targetText.value = tempText;
        
        // Set target language dropdown to the previously detected language
        for (let i = 0; i < targetLanguage.options.length; i++) {
            if (targetLanguage.options[i].value === lastDetectedLanguage) {
                targetLanguage.selectedIndex = i;
                break;
            }
        }
        
        // Re-detect language of the new source text
        detectLanguage();
    }
    
    // Handle speak text
    async function handleSpeakText(text, lang) {
        if (!text.trim()) return;
        
        try {
            // First stop any currently playing audio
            await fetch('/api/stop-audio', {
                method: 'POST'
            });
            
            // Then play the new text
            const response = await fetch('/api/speak', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    lang: lang || 'en'
                })
            });
            
            const data = await response.json();
            
            if (!data.success) {
                console.error('TTS error:', data.error);
            }
        } catch (error) {
            console.error('Error with text-to-speech:', error);
        }
    }
    
    // Initialize the app
    init();
});
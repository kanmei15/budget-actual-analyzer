document.addEventListener('DOMContentLoaded', () => {
    setupFileUpload(
        'upload-budget-area',
        'file-input-budget',
        '/api/upload-budget',
        '/api/aggregate/budget',
        '予算');
});
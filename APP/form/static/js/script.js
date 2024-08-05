document.addEventListener('DOMContentLoaded', function() {
    function fetchCSV(url, callback) {
        Papa.parse(url, {
            download: true,
            header: true,
            complete: function(results) {
                callback(results.data);
            },
            error: function(error) {
                console.error(`Error fetching CSV from ${url}:`, error);
            }
        });
    }

    function populateSelect(selectElement, options, valueField, textField) {
        selectElement.innerHTML = options.map(item => 
            `<option value="${item[valueField]}">${item[textField]}</option>`
        ).join('');
    }

    function initializeForm() {
        const wilayaSelect = document.getElementById('wilaya');
        const dairaSelect = document.getElementById('daira');
        const baladiaSelect = document.getElementById('baladia');

        fetchCSV('/static/data/wilayas.csv', function(wilayas) {
            populateSelect(wilayaSelect, wilayas, 'ID', 'Name_Wilaya');
        });

        wilayaSelect.addEventListener('change', function() {
            const selectedWilayaId = this.value;
            fetchCSV('/static/data/dairas.csv', function(dairas) {
                const filteredDairas = dairas.filter(daira => daira.ID_Wilaya == selectedWilayaId);
                populateSelect(dairaSelect, filteredDairas, 'ID', 'Name_Daira');
                dairaSelect.dispatchEvent(new Event('change')); // Trigger Baladia update
            });
        });

        dairaSelect.addEventListener('change', function() {
            const selectedDairaId = this.value;
            fetchCSV('/static/data/baladias.csv', function(baladias) {
                const filteredBaladias = baladias.filter(baladia => baladia.ID_Daira == selectedDairaId);
                populateSelect(baladiaSelect, filteredBaladias, 'ID', 'Name_Baladia');
            });
        });

        // Set the current date for تاريخ اليوم input field
        document.getElementById('date1').value = new Date().toISOString().substr(0, 10);
    }

    initializeForm();
});

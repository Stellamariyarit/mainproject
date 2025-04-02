// function getPrediction() {
//     const city = document.getElementById('locationInput').value;
//     if (!city) {
//       alert('Please enter a city name');
//       return;
//     }
    
//     // Example of simulating prediction data
//     const predictionData = Math.floor(Math.random() * 100);
//     let alertMessage = "";
  
//     if (predictionData < 20) {
//       alertMessage = "🟢 Green Alert: No Significant Rainfall Expected";
//     } else if (predictionData < 50) {
//       alertMessage = "🟡 Yellow Alert: Moderate Rainfall Expected";
//     } else if (predictionData < 80) {
//       alertMessage = "🟠 Orange Alert: Heavy Rainfall Expected";
//     } else {
//       alertMessage = "🔴 Red Alert: Very Heavy Rainfall, Take Precautions";
//     }
  
//     document.getElementById('predictionResult').innerText = `Predicted Rainfall: ${predictionData} mm`;
//     document.getElementById('alertMessage').innerText = alertMessage;
  
//     // Chart.js Graph Example
//     const ctx = document.getElementById('rainfallChart').getContext('2d');
//     const rainfallChart = new Chart(ctx, {
//       type: 'line',
//       data: {
//         labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
//         datasets: [{
//           label: 'Rainfall (mm)',
//           data: [20, 45, 30, predictionData, 60, 80],
//           borderColor: '#007bff',
//           fill: false
//         }]
//       }
//     });
//   }
  



function getPrediction() {
    const city = document.getElementById('locationInput').value;
    if (!city) {
      alert('Please enter a city name');
      return;
    }
  
    fetch(`/predict_rainfall_api?city=${city}`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          alert(data.error);
          return;
        }
  
        const predictionData = Math.floor((data.rf_prediction + data.svm_prediction + data.lstm_prediction) / 3);
        let alertMessage = "";
  
        if (predictionData < 20) {
          alertMessage = "🟢 Green Alert: No Significant Rainfall Expected";
        } else if (predictionData < 50) {
          alertMessage = "🟡 Yellow Alert: Moderate Rainfall Expected";
        } else if (predictionData < 80) {
          alertMessage = "🟠 Orange Alert: Heavy Rainfall Expected";
        } else {
          alertMessage = "🔴 Red Alert: Very Heavy Rainfall, Take Precautions";
        }
  
        document.getElementById('predictionResult').innerText = `Predicted Rainfall: ${predictionData.toFixed(2)} mm`;
        document.getElementById('alertMessage').innerText = alertMessage;
  
        // Chart.js Graph Example
        const ctx = document.getElementById('rainfallChart').getContext('2d');
        const rainfallChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
              label: 'Rainfall (mm)',
              data: [20, 45, 30, predictionData, 60, 80],
              borderColor: '#007bff',
              fill: false
            }]
          }
        });
      })
      .catch(error => {
        console.error('Error fetching prediction:', error);
        alert('Failed to get prediction. Please try again.');
      });
  }
  
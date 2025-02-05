/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 * 
 */

const pieConfig = {
  type: 'doughnut',
  data: {
    datasets: [
      {
        data: [90, 90],
        /**
         * These colors come from Tailwind CSS palette
         * https://tailwindcss.com/docs/customizing-colors/#default-color-palette
         */
        backgroundColor: ['#fde8b0', '#ee8370'],
        label: 'Dataset 1',
      },
    ],
    labels: ['Employees', 'Clients'],
  },
  options: {
    responsive: true,
    cutoutPercentage: 80,
    /**
     * Default legends are ugly and impossible to style.
     * See examples in charts.html to add your own legends
     *  */
    legend: {
      display: false,
    },
  },
}

// change this to the id of your chart element in HMTL
const pieCtx = document.getElementById('pie')
window.myPie = new Chart(pieCtx, pieConfig)

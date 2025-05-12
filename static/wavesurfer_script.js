// Create a Wavesurfer instance
const regions = RegionsPlugin.create()

const wavesurfer = WaveSurfer.create({
    container: '#waveform',
    waveColor: 'violet',
    progressColor: 'purple',
    barWidth: 2,
    height: 100,
    plugins: [regions],
});

wavesurfer.load(failitee)

// Play/Pause button functionality
document.getElementById('playPause').addEventListener('click', () => {
    wavesurfer.playPause();
});

wavesurfer.on('error', (error) => {
    window.alert('Error loading audio: ' + error);
})

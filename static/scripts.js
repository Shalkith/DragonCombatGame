
async function improve(dragonid, type,name) {
  try {
    // Send improvement request to backend
    const response = await fetch(`/improve/${dragonid}/${name}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
      console.error('Failed to improve stat');
      const errorData = await response.json();
      const message = errorData.detail.message || 'Improvement failed';
      alert(message);
      return;
    }

    // Get new value from response (if API returns it)
    const data = await response.json();
    const newValue = data.message.new_value ?? null;
    console.log('Improvement successful:', data.message.new_value);

    // Find element and increment visually if no value is returned
    const el = document.getElementById(`${type}-${name}`);
    if (el) {
      let current = parseInt(el.textContent);
      el.textContent = newValue ?? (current + 1);

      // temporary glow animation
      el.style.transition = "color 0.3s";
      el.style.color = "#f1c40f";
      setTimeout(() => el.style.color = "#58d68d", 500);
    }

  } catch (err) {
    console.error('Error:', err);
    alert('An error occurred.');
  }
}

function submitChallenge(challengerId, defenderId) {
    console.log(`Submitting challenge: ${challengerId} vs ${defenderId}`);

    fetch(`/initiatechallenge/${challengerId}/${defenderId}`)
      .then(response => {
        if (!response.ok) throw new Error("Failed to initiate challenge");
        return response.json();
      })
      .then(data => {
        alert(`Challenge initiated between Dragon ${challengerId} and ${defenderId}!`);
        console.log(data);
      })
      .catch(err => {
        console.error(err);
        alert("Error initiating challenge");
      });
  }
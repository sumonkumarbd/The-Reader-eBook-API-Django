function showEndpoint(index) {
  // Hide all endpoint items
  const endpointItems = document.querySelectorAll(".endpoint-item");
  endpointItems.forEach((item) => {
    item.classList.remove("active");
  });

  // Show the selected endpoint item
  endpointItems[index].classList.add("active");

  // Update tab selection
  const endpointTabs = document.querySelectorAll(".endpoint-tab");
  endpointTabs.forEach((tab) => {
    tab.classList.remove("active");
  });
  endpointTabs[index].classList.add("active");
}

function copyToClipboard(button) {
  const text = button.previousSibling.textContent.trim();
  navigator.clipboard.writeText(text).then(() => {
    const originalText = button.textContent;
    button.textContent = "Copied!";
    setTimeout(() => {
      button.textContent = originalText;
    }, 2000);
  });
}

// This is your test publishable API key.
const stripe = Stripe("pk_test_51MpD8VHjForJHjCt0k588Bqt0avQVFo4mn7qLGdEcskklPj0hEds8uJNe6qbQFUtglDgcNR58dpUpAViJcL2iyqG00cDOktWn0");

initialize();

// Create a Checkout Session as soon as the page loads
async function initialize() {
  const response = await fetch("/create-checkout-session", {
    method: "POST",
  });

  const { clientSecret } = await response.json();

  const checkout = await stripe.initEmbeddedCheckout({
    clientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}
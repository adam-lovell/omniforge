import Stripe from 'stripe';

const stripe = new Stripe('YOUR_SECRET_KEY'); // Replace with your Stripe API key

export const createCheckoutSession = async (userEmail) => {
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      mode: 'subscription',
      success_url: 'https://yourwebsite.com/success',
      cancel_url: 'https://yourwebsite.com/cancel',
      customer_email: userEmail,
      line_items: [
        {
          price: 'YOUR_PRICE_ID', // Replace with actual Stripe price ID
          quantity: 1
        }
      ]
    });

    return session.url; // Returns the payment link
  } catch (error) {
    console.error("Error creating Stripe session:", error.message);
    return null;
  }
};
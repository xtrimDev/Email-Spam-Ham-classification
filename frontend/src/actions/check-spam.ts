'use server'

export async function checkSpam(formData: FormData) {
  const email = formData.get('email') as string

  try {
    const response = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: email })
    });

    if (!response.ok) {
      console.error('Server Error:');
    } else {
      const responseData = await response.json();

      return {
        isSpam: responseData.prediction,
        confidence: responseData.confidence,
      }
    }
  } catch (error) {
    console.error('Server Error:');
  }

  return {
    isSpam: 0,
    confidence: 0,
  }
}


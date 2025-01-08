
import { Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { checkSpam } from '../actions/check-spam'

import React, { useState } from 'react';

export default function SpamChecker() {
  const [isPending, setIsPending] = useState(false);
  const [result, setResult] = useState<{
    isSpam: boolean;
    confidence: number;
  } | null>(null);

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    try {
      setIsPending(true);
      const result = await checkSpam(formData);
      setResult(result);
    } catch (error) {
      console.error('Error checking spam:', error);
    } finally {
      setIsPending(false);
    }
  }

  return (
    <div className="min-h-screen p-4 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-2xl mx-auto space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Email Spam Checker</CardTitle>
            <CardDescription>
              Paste your email content below to check if it might be considered spam
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={onSubmit} className="space-y-4">
              <Textarea
                name="email"
                placeholder="Paste email content here..."
                className="min-h-[200px]"
                required
              />
              <Button 
                type="submit" 
                className="w-full"
                disabled={isPending}
              >
                {isPending ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  'Check for Spam'
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {result && (
          <Alert variant={result.isSpam ? 'destructive' : 'safe'}>
            <AlertTitle>
              {result.isSpam ? 'Spam Detected!' : 'Looks Safe!'}
            </AlertTitle>
            <AlertDescription className="space-y-2">
              <p>
                Confidence: {result.confidence.toFixed(1)}%
              </p>
            </AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  );
}


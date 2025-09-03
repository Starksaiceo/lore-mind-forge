import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Brain, TrendingUp, Zap, Shield, Target, BarChart3 } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-muted/20">
      {/* Navigation */}
      <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Brain className="h-8 w-8 text-primary" />
              <span className="text-2xl font-bold">AI CEO</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/login">
                <Button variant="ghost">Login</Button>
              </Link>
              <Link to="/signup">
                <Button>Get Started</Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 text-center">
        <div className="mx-auto max-w-4xl">
          <h1 className="mb-6 text-5xl font-bold leading-tight">
            Your Autonomous
            <span className="text-primary"> AI CEO</span>
          </h1>
          <p className="mb-8 text-xl text-muted-foreground">
            The world's first fully autonomous AI business operator. Set goals, 
            watch profits grow, and scale without limits while you sleep.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/signup">
              <Button size="lg" className="text-lg px-8 py-4">
                Start Your AI Business
              </Button>
            </Link>
            <Button size="lg" variant="outline" className="text-lg px-8 py-4">
              Watch Demo
            </Button>
          </div>
          <div className="mt-8 text-sm text-muted-foreground">
            Join 10,000+ entrepreneurs building autonomous businesses
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold mb-4">Autonomous Business Intelligence</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Advanced AI that learns, adapts, and executes business strategies independently
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card className="animate-fade-in">
            <CardHeader>
              <Target className="h-10 w-10 text-primary mb-2" />
              <CardTitle>Smart Goal Setting</CardTitle>
              <CardDescription>
                AI analyzes market trends and sets achievable business objectives automatically
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="text-sm space-y-2 text-muted-foreground">
                <li>• Market trend analysis</li>
                <li>• Revenue optimization</li>
                <li>• Risk assessment</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="animate-fade-in">
            <CardHeader>
              <TrendingUp className="h-10 w-10 text-primary mb-2" />
              <CardTitle>Revenue Optimization</CardTitle>
              <CardDescription>
                Continuously optimizes pricing, marketing, and operations for maximum profit
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="text-sm space-y-2 text-muted-foreground">
                <li>• Dynamic pricing</li>
                <li>• Cost optimization</li>
                <li>• Profit maximization</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="animate-fade-in">
            <CardHeader>
              <Zap className="h-10 w-10 text-primary mb-2" />
              <CardTitle>24/7 Automation</CardTitle>
              <CardDescription>
                Works around the clock, making decisions and executing strategies while you sleep
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="text-sm space-y-2 text-muted-foreground">
                <li>• Continuous operation</li>
                <li>• Real-time decisions</li>
                <li>• Zero downtime</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="animate-fade-in">
            <CardHeader>
              <BarChart3 className="h-10 w-10 text-primary mb-2" />
              <CardTitle>Advanced Analytics</CardTitle>
              <CardDescription>
                Deep insights into performance, market conditions, and growth opportunities
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="text-sm space-y-2 text-muted-foreground">
                <li>• Performance tracking</li>
                <li>• Predictive analytics</li>
                <li>• Growth insights</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="animate-fade-in">
            <CardHeader>
              <Brain className="h-10 w-10 text-primary mb-2" />
              <CardTitle>Learning Memory</CardTitle>
              <CardDescription>
                Learns from every decision and outcome to continuously improve performance
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="text-sm space-y-2 text-muted-foreground">
                <li>• Adaptive learning</li>
                <li>• Experience retention</li>
                <li>• Performance improvement</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="animate-fade-in">
            <CardHeader>
              <Shield className="h-10 w-10 text-primary mb-2" />
              <CardTitle>Enterprise Security</CardTitle>
              <CardDescription>
                Bank-level security with encrypted data and compliance-ready infrastructure
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="text-sm space-y-2 text-muted-foreground">
                <li>• End-to-end encryption</li>
                <li>• SOC 2 compliance</li>
                <li>• Data protection</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary/5 py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Build Your AI Empire?</h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join thousands of entrepreneurs who've already started their autonomous businesses
          </p>
          <Link to="/signup">
            <Button size="lg" className="text-lg px-8 py-4">
              Start Free Trial
            </Button>
          </Link>
          <div className="mt-4 text-sm text-muted-foreground">
            No credit card required • 14-day free trial
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-background">
        <div className="container mx-auto px-4 py-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Brain className="h-6 w-6 text-primary" />
              <span className="font-semibold">AI CEO</span>
            </div>
            <div className="text-sm text-muted-foreground">
              © 2024 AI CEO. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
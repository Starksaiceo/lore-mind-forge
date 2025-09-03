import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Brain, TrendingUp, Target, Activity, DollarSign, Settings, LogOut } from 'lucide-react'
import { api, Goal, MemoryLog, Revenue } from '@/lib/api'
import { useToast } from '@/hooks/use-toast'

export default function Dashboard() {
  const [goals, setGoals] = useState<Goal[]>([])
  const [memoryLogs, setMemoryLogs] = useState<MemoryLog[]>([])
  const [revenue, setRevenue] = useState<Revenue | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const { toast } = useToast()

  const user = JSON.parse(localStorage.getItem('user') || '{}')

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [goalsData, memoryData, revenueData] = await Promise.all([
        api.getGoals(),
        api.getMemoryLogs(),
        api.getRevenue(),
      ])
      
      setGoals(goalsData)
      setMemoryLogs(memoryData.slice(0, 5)) // Latest 5 logs
      setRevenue(revenueData)
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to load dashboard data",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
    window.location.href = '/'
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Brain className="h-12 w-12 text-primary animate-pulse mx-auto mb-4" />
          <p className="text-muted-foreground">Loading your AI CEO dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Brain className="h-8 w-8 text-primary" />
              <div>
                <h1 className="text-2xl font-bold">AI CEO Dashboard</h1>
                <p className="text-muted-foreground">Welcome back, {user.name}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Button variant="ghost" size="icon">
                <Settings className="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="icon" onClick={handleLogout}>
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Revenue Overview */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                ${revenue?.total.toFixed(2) || '0.00'}
              </div>
              <p className="text-xs text-muted-foreground">
                {revenue?.currency || 'USD'}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Monthly Revenue</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                ${revenue?.monthly.toFixed(2) || '0.00'}
              </div>
              <p className="text-xs text-muted-foreground">
                This month
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Daily Revenue</CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                ${revenue?.daily.toFixed(2) || '0.00'}
              </div>
              <p className="text-xs text-muted-foreground">
                Today
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Goals Section */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="flex items-center space-x-2">
                    <Target className="h-5 w-5" />
                    <span>Active Goals</span>
                  </CardTitle>
                  <CardDescription>
                    Your AI is working on these objectives
                  </CardDescription>
                </div>
                <Button size="sm">Add Goal</Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {goals.length > 0 ? (
                  goals.map((goal) => (
                    <div key={goal.id} className="border rounded-lg p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="font-medium">{goal.title}</h4>
                          <p className="text-sm text-muted-foreground mt-1">
                            {goal.description}
                          </p>
                        </div>
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          goal.status === 'active' 
                            ? 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
                            : goal.status === 'completed'
                            ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400'
                            : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
                        }`}>
                          {goal.status}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <Target className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>No active goals yet</p>
                    <p className="text-sm">Create your first goal to get started</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Memory Logs Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Brain className="h-5 w-5" />
                <span>AI Memory</span>
              </CardTitle>
              <CardDescription>
                Recent decisions and learnings from your AI
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {memoryLogs.length > 0 ? (
                  memoryLogs.map((log) => (
                    <div key={log.id} className="border-l-2 border-primary pl-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="text-sm">{log.content}</p>
                          <p className="text-xs text-muted-foreground mt-1">
                            {new Date(log.timestamp).toLocaleString()}
                          </p>
                        </div>
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          log.type === 'action'
                            ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400'
                            : log.type === 'decision'
                            ? 'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-400'
                            : 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
                        }`}>
                          {log.type}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <Brain className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>No memory logs yet</p>
                    <p className="text-sm">Your AI will start learning soon</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid md:grid-cols-4 gap-4">
          <Button className="h-16 flex-col space-y-2">
            <Target className="h-5 w-5" />
            <span className="text-sm">New Goal</span>
          </Button>
          <Button variant="outline" className="h-16 flex-col space-y-2">
            <TrendingUp className="h-5 w-5" />
            <span className="text-sm">View Analytics</span>
          </Button>
          <Button variant="outline" className="h-16 flex-col space-y-2">
            <Settings className="h-5 w-5" />
            <span className="text-sm">AI Settings</span>
          </Button>
          <Link to="/admin">
            <Button variant="outline" className="h-16 w-full flex-col space-y-2">
              <Brain className="h-5 w-5" />
              <span className="text-sm">Admin Panel</span>
            </Button>
          </Link>
        </div>
      </div>
    </div>
  )
}
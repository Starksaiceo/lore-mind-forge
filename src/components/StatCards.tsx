import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { DollarSign, Package, Target, TrendingUp } from 'lucide-react';

interface StatCardsProps {
  revenue?: {
    today: number;
    month: number;
    total: number;
  };
  products?: number;
  campaigns?: number;
}

export default function StatCards({ revenue, products, campaigns }: StatCardsProps) {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <Card className="glass-card">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Today's Revenue</CardTitle>
          <DollarSign className="h-4 w-4 text-neon-cyan" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-gradient">
            {revenue ? formatCurrency(revenue.today) : '$0'}
          </div>
          <p className="text-xs text-muted-foreground">
            +12% from yesterday
          </p>
        </CardContent>
      </Card>

      <Card className="glass-card">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Monthly Revenue</CardTitle>
          <TrendingUp className="h-4 w-4 text-neon-purple" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-gradient">
            {revenue ? formatCurrency(revenue.month) : '$0'}
          </div>
          <p className="text-xs text-muted-foreground">
            +23% from last month
          </p>
        </CardContent>
      </Card>

      <Card className="glass-card">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Products</CardTitle>
          <Package className="h-4 w-4 text-neon-cyan" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{products || 0}</div>
          <p className="text-xs text-muted-foreground">
            +2 this week
          </p>
        </CardContent>
      </Card>

      <Card className="glass-card">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Active Campaigns</CardTitle>
          <Target className="h-4 w-4 text-neon-purple" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{campaigns || 0}</div>
          <p className="text-xs text-muted-foreground">
            +1 this month
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
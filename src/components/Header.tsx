import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Brain, User, LogOut, Settings, Shield } from 'lucide-react';
import { useAuthStore } from '@/lib/auth';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

export default function Header() {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  return (
    <header className="glass border-b border-white/10 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-2">
            <Brain className="h-8 w-8 text-neon-cyan" />
            <span className="text-2xl font-bold text-gradient">AI CEO</span>
          </Link>

          <nav className="hidden md:flex items-center space-x-6">
            {user ? (
              <>
                <Link to="/dashboard" className="hover:text-neon-cyan transition-colors">
                  Dashboard
                </Link>
                <Link to="/chat" className="hover:text-neon-cyan transition-colors">
                  Chat
                </Link>
                <Link to="/voice" className="hover:text-neon-cyan transition-colors">
                  Voice
                </Link>
                <Link to="/products" className="hover:text-neon-cyan transition-colors">
                  Products
                </Link>
                <Link to="/activity" className="hover:text-neon-cyan transition-colors">
                  Activity
                </Link>
                {user.role === 'admin' && (
                  <Link to="/admin" className="hover:text-neon-purple transition-colors">
                    Admin
                  </Link>
                )}
              </>
            ) : (
              <>
                <Link to="/pricing" className="hover:text-neon-cyan transition-colors">
                  Pricing
                </Link>
              </>
            )}
          </nav>

          <div className="flex items-center space-x-4">
            {user ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="gap-2">
                    <User className="h-4 w-4" />
                    {user.email}
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="glass">
                  <DropdownMenuItem asChild>
                    <Link to="/billing" className="flex items-center gap-2">
                      <Settings className="h-4 w-4" />
                      Billing
                    </Link>
                  </DropdownMenuItem>
                  {user.role === 'admin' && (
                    <DropdownMenuItem asChild>
                      <Link to="/admin" className="flex items-center gap-2">
                        <Shield className="h-4 w-4" />
                        Admin Panel
                      </Link>
                    </DropdownMenuItem>
                  )}
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={handleLogout} className="text-red-400">
                    <LogOut className="h-4 w-4 mr-2" />
                    Logout
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="ghost">Login</Button>
                </Link>
                <Link to="/register">
                  <Button className="neon-border">Get Started</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
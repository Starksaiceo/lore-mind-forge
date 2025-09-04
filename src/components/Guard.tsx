import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/lib/auth';

interface GuardProps {
  children: React.ReactNode;
  role: 'user' | 'admin';
}

export default function Guard({ children, role }: GuardProps) {
  const { user, checkSession } = useAuthStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      checkSession();
    }
  }, [user, checkSession]);

  useEffect(() => {
    if (user === null) {
      navigate('/login');
      return;
    }

    if (role === 'admin' && user?.role !== 'admin') {
      navigate('/dashboard');
      return;
    }
  }, [user, role, navigate]);

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    );
  }

  return <>{children}</>;
}